#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Iterator, Optional

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.language_identification.v1.language_identification_pb2 as lid
import phonexia.grpc.technologies.language_identification.v1.language_identification_pb2_grpc as lid_grpc
from google.protobuf.json_format import MessageToJson


def time_to_duration(time: float) -> Optional[google.protobuf.duration_pb2.Duration]:
    if time is None:
        return None
    duration = google.protobuf.duration_pb2.Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: Path,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    languages: Optional[list[lid.Language]],
    groups: Optional[list[lid.LanguageGroup]],
) -> Iterator[lid.IdentifyRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = lid.IdentifyConfig(
        speech_length=time_to_duration(speech_length), languages=languages, groups=groups
    )
    chunk_size = 1024 * 1024
    with open(file, mode="rb") as fd:
        while chunk := fd.read(chunk_size):
            yield lid.IdentifyRequest(
                audio=phx_common.Audio(content=chunk, time_range=time_range), config=config
            )
            time_range = None


def write_result(
    output, languages: list[str], response: lid.IdentifyResponse, out_format: str
) -> None:
    if out_format == "json":
        output.write(MessageToJson(response))
        return

    langs = {}
    groups = {}
    for res in response.result.scores:
        if res.identifier in languages:
            langs[res.identifier] = res.score
        else:
            groups[res.identifier] = res.score

    logging.debug(f"Group probabilities are:\n{groups}")
    logging.debug(f"Language probabilities are:\n{langs}")

    sort_dict = lambda dct: sorted(dct.items(), key=lambda x: x[1], reverse=True)

    logging.info("Writing group probabilities")
    if len(groups) > 0:
        output.write("Group probabilities:\n")
        [output.write(f"{lang}\t{score}\n") for lang, score in sort_dict(groups)]

    logging.info("Writing language probabilities")
    output.write("Language probabilities:\n")
    [output.write(f"{lang}\t{score}\n") for lang, score in sort_dict(langs)]


def identify(
    channel: grpc.Channel,
    input_file: Path,
    output_file: Optional[Path],
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    input_languages: Optional[Path],
    input_groups: Optional[Path],
    list_supported_languages: bool,
    metadata: Optional[list],
    out_format: str,
) -> None:
    logging.debug(f"Parsing input languages {input_languages}")
    languages: Optional[list[lid.Language]] = (
        None
        if input_languages is None
        else [lid.Language(language_code=code) for code in json.loads(input_languages.read_text())]
    )

    logging.debug(f"Parsing input groups {input_groups}")
    groups: Optional[list[lid.LanguageGroup]] = (
        None
        if input_groups is None
        else [
            lid.LanguageGroup(identifier=identifier, language_codes=langs)
            for identifier, langs in json.loads(input_groups.read_text()).items()
        ]
    )

    if input_groups is not None:
        with open(input_groups) as f:
            groups = [
                lid.LanguageGroup(identifier=identifier, language_codes=langs)
                for identifier, langs in json.load(f).items()
            ]

    logging.info("Getting supported languages")
    stub = lid_grpc.LanguageIdentificationStub(channel)
    response = stub.ListSupportedLanguages(lid.ListSupportedLanguagesRequest(), metadata=metadata)

    supported_language = response.supported_languages

    output = open(output_file, "w", encoding="utf8") if output_file else sys.stdout  # noqa: SIM115

    if list_supported_languages:
        logging.info("Writing supported languages")
        output.write("\n".join(supported_language))
        if output_file:
            output.close()
        return

    logging.debug(f"Supported languages are {supported_language}")

    logging.info(f"Estimating language probabilities from file '{input_file}'")
    response = stub.Identify(
        make_request(input_file, start, end, speech_length, languages, groups),
        metadata=metadata,
    )
    logging.info("Writing results")
    write_result(output, supported_language, response, out_format)
    if output_file:
        output.close()


def main():  # noqa: C901
    parser = argparse.ArgumentParser(
        description=(
            "Language identification gRPC client. Identify language probabilities from an input audio file."
        ),
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument(
        "--metadata",
        metavar="key=value",
        nargs="+",
        type=lambda x: tuple(x.split("=")),
        help="Custom client metadata",
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument("--speech_length", type=float, help="Maximum amount of speech in seconds")
    parser.add_argument("-i", "--input", type=Path, help="input audio file", required=True)
    parser.add_argument("-o", "--output", type=Path, help="output file path")
    parser.add_argument(
        "-F",
        "--out_format",
        type=str,
        help="output file format",
        default="txt",
        choices=["txt", "json"],
    )
    parser.add_argument(
        "--languages",
        type=Path,
        help="Path to a json file with selected subset of languages for the identification. "
        'The file should contain a json array of language codes, i.e. ["cs-cz", "en-US"]',
    )
    parser.add_argument(
        "--groups",
        type=Path,
        help="Path to a json file with definitions of groups. The groups must have unique id "
        "and should be assigned disjunct subset of languages. The file should contain a json "
        "dictionary where each key should be a group identifier and value should be a list of "
        'language codes, i.e. {"english": ["en-US", "en-GB"], "arabic": ["ar-IQ", "ar-KW"]}',
    )
    parser.add_argument(
        "--list_supported_languages",
        action="store_true",
        help="List supported languages into the output file and exit.",
    )

    args = parser.parse_args()

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")

    if args.speech_length is not None and args.speech_length < 0:
        raise ValueError("Parameter 'speech_length' must be a non-negative float.")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not os.path.isfile(args.input):
        logging.error(f"no such file {args.input}")
        exit(1)

    if args.output is not None and not os.path.isdir(args.output.parents[0]):
        logging.error(f"output file directory does not exist {args.output}")
        exit(1)

    if args.languages and not os.path.isfile(args.languages):
        logging.error(f"no such file {args.languages}")
        exit(1)

    if args.groups and not os.path.isfile(args.groups):
        logging.error(f"no such file {args.groups}")
        exit(1)

    try:
        logging.info(f"Connecting to {args.host}")
        channel = (
            grpc.secure_channel(target=args.host, credentials=grpc.ssl_channel_credentials())
            if args.use_ssl
            else grpc.insecure_channel(target=args.host)
        )
        identify(
            channel,
            args.input,
            args.output,
            args.start,
            args.end,
            args.speech_length,
            args.languages,
            args.groups,
            args.list_supported_languages,
            args.metadata,
            args.out_format,
        )

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)
    finally:
        channel.close()


if __name__ == "__main__":
    main()
