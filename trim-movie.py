#!/usr/bin/env python3

import argparse
import subprocess

def create_movie_segment(input_file, start_time, duration):
    output_file = input_file + "_" + start_time.replace(":", "-") + "_" + duration.replace(":", "-") + ".mp4"
    command = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i", input_file,
        # "-c", "copy",
        "-ss", start_time,
        "-t", duration,
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Movie segment successfully created for {duration} from {start_time}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred for start time: {start_time}, duration: {duration}. Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create copies of a movie file at given start times and durations.")
    parser.add_argument('-i', '--input', dest="input_file", help="Path to the original movie file")
    parser.add_argument('-s', '--segment', action="append", default=[["00:00:00,00:00:10"]], dest="time_pairs", nargs="+", metavar="time_pairs", help="Start time and duration pairs (in format hh:mm:ss)")

    args = parser.parse_args()
    input_file = args.input_file

    for time_pair in args.time_pairs:
        time_pair_string = time_pair[0]
        start_time, duration = time_pair_string.split(',')
        create_movie_segment(input_file, start_time, duration)
