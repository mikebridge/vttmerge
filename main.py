#!/usr/bin/env python3

import io
import argparse
import pathlib
import sys

import webvtt
from webvtt import WebVTT

from typing import TypedDict, List


class MainArgs(TypedDict):
    abbrev: str
    file: str


def create_file_name(orig_file_name: str, ext: str = 'all') -> str:
    p = pathlib.Path(orig_file_name)
    stem = p.stem
    orig_file_extension = p.suffix
    new_file_name = pathlib.Path(stem).stem
    return f'{new_file_name}.{ext}{orig_file_extension}'


def main(main_args: MainArgs):
    vtt = webvtt.WebVTT();
    caption_sets: list[WebVTT] = []
    if len(main_args["file"]) == 0:
        sys.stderr.write('there must be at least one file')
        exit(1)
    for file in main_args["file"]:
        print(f'reading {file}')
        caption_sets.append(webvtt.read(file))
    # caption_sets = [webvtt.read(file) for file in files]
    print(f'there are {len(caption_sets)} sets')

    combined_captions = zip(*[c.captions for c in caption_sets])
    # combined_captions = zip(caption_sets[0].captions, caption_sets[1].captions)
    # print(combined_captions)
    for caption_set in combined_captions:
        row = 0
        new_captions = []
        for caption in caption_set:
            row += 1
            if row > 1:
                new_captions.append(f"<c.yellow>{caption.text}</c>")
            else:
                new_captions.append(caption.text)
        caption = webvtt.Caption(caption_set[0].start, caption_set[0].end, new_captions)
        vtt.captions.append(caption)
    new_file_name = create_file_name(main_args["file"][0], main_args["abbrev"]) or 'new_captions.vtt'
    print(f'writing to {new_file_name}')
    with io.open(new_file_name, 'w', encoding='utf8') as fd:
        vtt.write(fd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Files from Google Drive')
    parser.add_argument('-f', '--file', nargs='+', help='vtt file', required=True)
    parser.add_argument('-a', '--abbrev',
                        help='2-letter language abbreviation',
                        default='all',
                        required=False)
    parser.set_defaults(join=False)
    args = parser.parse_args()

    mainArgs = MainArgs(file=args.file, abbrev=args.abbrev)
    main(mainArgs)
