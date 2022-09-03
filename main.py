#!/usr/bin/env python3

import io
#import os
import argparse
#import pathlib
import webvtt
from webvtt import WebVTT


#from datetime import datetime
#from functools import partial
#from typing import Callable, List, Optional, TypedDict, Union
#from webvtt import WebVTT, Caption

#import orjson.orjson
# from dotenv import load_dotenv

# load_dotenv()

# SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
#
#
# def verify_env_or_exit() -> None:
#     if not FOLDER:
#         exit('Please set GOOGLE_DRIVE_FOLDER in your .env file')
#     if not FOLDER_ID:
#         exit('Please set GOOGLE_DRIVE_FOLDER_ID in your .env file')
#     if not RAW_FILES_FOLDER:
#         exit('Please set RAW_FILES_FOLDER in your .env file')
#     if not RAW_PATH.exists():
#         exit(f"could not find RAW_FILES_FOLDER: {RAW_FILES_FOLDER}")


def main(files):
    vtt = webvtt.WebVTT();
    caption_sets: list[WebVTT] = []
    for file in files:
        print(f'reading {file}')
        caption_sets.append(webvtt.read(file))
    # caption_sets = [webvtt.read(file) for file in files]
    print(f'there are {len(caption_sets)} sets')
    combined_captions = zip(*[c.captions for c in caption_sets])
    # combined_captions = zip(caption_sets[0].captions, caption_sets[1].captions)
    print(combined_captions)
    for caption_set in combined_captions:
        print('found set')
        print(caption_set)
        # for caption_pair in caption_set:
        #      print(caption_pair)
        # print(caption_set[0].start)
        # print(caption_set[0].end)
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
    # open('new_captions.vtt', 'w', encoding='utf8') as fd:
    with io.open('new_captions.vtt', 'w', encoding='utf8') as fd:
        vtt.write(fd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Files from Google Drive')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                 help='an integer for the accumulator')
    # parser.add_argument('-m', '--max-files',
    #                     type=int,
    #                     help='max number of files to download',
    #                     required=False)
#     parser.add_argument('-d', '--days',
#                         type=int,
#                         default=GOOGLE_DRIVE_DAYS_AGO,
#                         help='download files uploaded in last N days',
#                         required=False)

    parser.add_argument('-f','--file', nargs='+', help='vtt file', required=True)

    args = parser.parse_args()
    # print type of args.max_files
    # print(f'max-files is        {args.max_files}')
    #print(f'days-ago is        {args.file}')
    # files_to_download = prune_tree(all_files, partial(is_file_newer_than, since_time))
    # print(f'== TOTAL: {count_files(files_to_download)}')
    # all_files_downloaded = []
    #     for file_or_dir in files_to_download:
    #         # print(f'== DOWNLOADING DIR {file_or_dir["name"]}')
    #         # download_tree(file, DOWNLOAD_DIR)
    #         downloaded_files = download_tree(file_or_dir, RAW_PATH, partial(download_file, google_drive))
    #         for file in downloaded_files:
    #             all_files_downloaded.append(file)
    #             print(f'== DOWNLOADED {file["full_path"]}')
    #     print(f"  FILES DOWNLOADED:{len(all_files_downloaded)}")
    main(args.file)

#parser.print_help()

#print(args.accumulate(args.integers))
