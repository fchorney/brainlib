#!/usr/bin/env python

import argparse
from sys import exit

from brainlib.bigbrain import bigbrain


def main():
    args = parse_args()

    # Separate messages into a list
    messages = list(map(str.strip, map(str, args.messages.split(","))))

    # Do the big brain
    img_path, imgur_link = bigbrain(
        messages,
        imgdir=args.imgdir,
        bgcolour=args.bgcolour,
        fontpath=args.fontpath,
        fontsize=args.fontsize,
        fontcolour=args.fontcolour,
        wraplength=args.wraplength,
        heightpadding=args.heightpadding,
        client_id=args.client_id,
        client_secret=args.client_secret,
        upload=args.upload,
    )

    print(f"Saved Image To: {img_path}")

    if imgur_link is not None:
        print(f"Uploaded to Imgur: {imgur_link}")

    exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="smallbrain: using this program",
    )

    # Positional Arguments
    parser.add_argument(
        "messages", type=str, help="comma delimited list of messages (no more than 10)"
    )

    # Image Args
    img_args = parser.add_argument_group("image")
    img_args.add_argument(
        "--imgdir", type=str, default="./img/", help="images dir path"
    )
    img_args.add_argument(
        "--bgcolour",
        type=int,
        nargs=4,
        default=[255, 255, 255, 255],
        help="RGBA values for the bg colour (0 - 255)",
    )

    # Font/Text Args
    font_args = parser.add_argument_group("font/text")
    font_args.add_argument(
        "--fontpath",
        type=str,
        default="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        help="font path",
    )
    font_args.add_argument("--fontsize", type=int, default=22, help="font size")
    font_args.add_argument(
        "--fontcolour",
        type=int,
        nargs=4,
        default=[0, 0, 0, 255],
        help="RGBA values for the font colour (0 - 255)",
    )
    font_args.add_argument(
        "--wraplength", type=int, default=20, help="text wrap cutoff length"
    )
    font_args.add_argument(
        "--heightpadding",
        type=int,
        default=5,
        help="height padding between multiple lines of text",
    )

    # Imgur API Group
    imgur_api = parser.add_argument_group("imgur api")
    imgur_api.add_argument("--client_id", type=str, help="Imgur API Client ID")

    imgur_api.add_argument("--client_secret", type=str, help="Imgur API Client Secret")

    imgur_api.add_argument(
        "--upload",
        action="store_true",
        help=("set this flag to upload to imgur [must supply client id and secret]"),
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
