import argparse
import logging
from typing import Iterator, Optional

import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.gender_identification.v1.gender_identification_pb2 as gid
import phonexia.grpc.technologies.gender_identification.v1.gender_identification_pb2_grpc as gid_grpc
from google.protobuf.json_format import MessageToJson

MAX_BATCH_SIZE = 1024


def parse_vp(path: str) -> phx_common.Voiceprint:
    with open(path, mode="rb") as file:
        return phx_common.Voiceprint(content=file.read())


def make_batch_request(vp_list: Iterator[str]) -> Iterator[gid.IdentifyRequest]:
    batch_size = 0
    request = gid.IdentifyRequest()
    for vp_file in vp_list:
        if batch_size >= MAX_BATCH_SIZE:
            yield request
            batch_size = 0
            request = gid.IdentifyRequest()
        if vp_file:
            vp = parse_vp(vp_file)
            request.voiceprints.append(vp)
            batch_size += 1
    if len(request.voiceprints):
        yield request


def identify_gender(voiceprint_file: str, channel: grpc.Channel, metadata: Optional[list]):
    stub = gid_grpc.GenderIdentificationStub(channel)
    batch_request = make_batch_request(iter([voiceprint_file]))
    for result in stub.Identify(batch_request, metadata=metadata):
        print(MessageToJson(result))


def main():
    parser = argparse.ArgumentParser(
        description="Gender Identification gRPC client. Identifies gender from input voiceprint.",
    )
    parser.add_argument("-f", "--file", type=str, help="Voiceprint from which to identify gender")
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
    args = parser.parse_args()

    if not args.file:
        raise ValueError("Parameter --file must not be empty string")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {args.host}")
        channel = (
            grpc.secure_channel(target=args.host, credentials=grpc.ssl_channel_credentials())
            if args.use_ssl
            else grpc.insecure_channel(target=args.host)
        )
        identify_gender(args.file, channel, args.metadata)

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
