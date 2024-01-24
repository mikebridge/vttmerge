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
    compact: bool
    file: str
    join: bool


def create_file_name(orig_file_name: str, ext: str = 'all') -> str:
    p = pathlib.Path(orig_file_name)
    stem = p.stem
    orig_file_extension = p.suffix
    new_file_name = pathlib.Path(stem).stem
    return f'{new_file_name}.{ext}{orig_file_extension}'

def combine_lines(text):
    lines = text.split('\n')
    combined_lines = []
    buffer = ''

    for line in lines:
        if not line.strip().startswith('-'):
            buffer += ' ' + line.strip()
        else:
            if buffer:
                combined_lines.append(buffer.strip())
            buffer = line.strip()

    # Adding the last buffer if it's not empty
    if buffer:
        combined_lines.append(buffer.strip())

    return '\n'.join(combined_lines)


def main(main_args: MainArgs):
    vtt = webvtt.WebVTT()
    caption_sets: list[WebVTT] = []
    if len(main_args["file"]) == 0 or len(main_args["file"]) > 1:
        sys.stderr.write('there must be only one file')
        exit(1)

    webvtt_file_name = main_args["file"][0]
    webvtt_file = webvtt.read(webvtt_file_name)
    captions: List = webvtt_file.captions

    # combined_captions = zip(*[c.captions for c in caption_sets])
    # # combined_captions = zip(caption_sets[0].captions, caption_sets[1].captions)
    # # print(combined_captions)
    joined_row_text = None
    joined_row_start = None
    joined_row_end = None

    blank_captions = []
    # for caption_set in combined_captions:

    new_captions: List[str] = []
    for caption in captions:
        text: str = caption.text
        if main_args["compact"]:
            text = combine_lines(caption.text)

        if main_args["join"]:
            if text.strip().endswith(('.', '?', '!')):
                if joined_row_text is not None:
                    text = joined_row_text + ' ' + text
                    joined_row_text = None
                else:
                    text = text
            else:
                # the row does not end in punctuation, so cache it
                if joined_row_text is None:
                    # it's the first one in the sentence, so save
                    # the start values
                    joined_row_start = caption.start
                    joined_row_end = caption.end
                    joined_row_text = text
                else:
                    # it's a continuation.
                    joined_row_text = joined_row_text + ' ' + text
                    blank_captions.append(webvtt.Caption(caption.start, caption.end, "[[...]]"))

                continue

        new_captions.append(text)

        if joined_row_start is None:
            caption = webvtt.Caption(caption.start, caption.end, new_captions)
            vtt.captions.append(caption)
        else:
            caption = webvtt.Caption(joined_row_start, joined_row_end, new_captions)
            vtt.captions.append(caption)
            joined_row_start = None
            joined_row_end = None

            # print each blank caption in the array
            for blank_caption in blank_captions:
                vtt.captions.append(blank_caption)
            blank_captions = []
        new_captions = []

    # print out any extra cached
    if joined_row_start is not None:
        caption = webvtt.Caption(joined_row_start, joined_row_end, joined_row_text)
        vtt.captions.append(caption)

    # and any extra blank lines
    for blank_caption in blank_captions:
        vtt.captions.append(blank_caption)


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
    parser.add_argument('-j', '--join',
                        action=argparse.BooleanOptionalAction,
                        help='join subsequent rows',
                        required=False)
    parser.add_argument('-c', '--compact',
                        action=argparse.BooleanOptionalAction,
                        help='compact',
                        required=False)
    parser.set_defaults(join=False)
    args = parser.parse_args()

    mainArgs = MainArgs(file=args.file, join=args.join, abbrev=args.abbrev, compact=args.compact)
    main(mainArgs)
