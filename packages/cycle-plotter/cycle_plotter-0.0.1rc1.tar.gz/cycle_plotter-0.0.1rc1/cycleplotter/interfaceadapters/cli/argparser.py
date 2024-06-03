import argparse
import re
from typing import Protocol

from cycleplotter.interfaceadapters.config import Source
from cycleplotter.usecases import plotter


class CliArgs(Protocol):
    input_file: str
    output_file: str
    source: Source
    axis: plotter.DurationAxis
    dimensions: plotter.Size


class SizeParseError(ValueError):
    pass


def parse_size(size_str: str) -> plotter.Size:
    size_str_lower = size_str.lower()
    if size_str_lower == "a4":
        return plotter.SIZE_A4
    if size_str_lower == "letter":
        return plotter.SIZE_LETTER
    pattern = r"^(\d*\.?\d+)x(\d*\.?\d+)(cm|px|in)$"
    match = re.match(pattern, size_str_lower)
    if match:
        width = float(match.group(1))
        height = float(match.group(2))
        unit = match.group(3)
    else:
        raise SizeParseError(f"Unknown size format {size_str}")
    if unit == "in":
        return plotter.Size(width, height)
    if unit == "cm":
        return plotter.Size(width / 2.54, height / 2.54)
    if unit == "px":
        return plotter.Size(width / 100, height / 100)
    raise ValueError(f"Unknown size format {size_str}")


def parse_args() -> CliArgs:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    arg_parser.add_argument(
        "-i",
        "--input-file",
        help="""path to archive exported from
Apple Health or Withings Health Mate""",
        required=True,
    )
    arg_parser.add_argument(
        "-o",
        "--output-file",
        help="path to image file to export",
        required=True,
    )
    arg_parser.add_argument(
        "-s",
        "--source",
        type=Source,
        choices=Source,
        required=True,
    )
    arg_parser.add_argument(
        "-a",
        "--axis",
        type=plotter.DurationAxis,
        choices=plotter.DurationAxis,
        default=plotter.DurationAxis.BOTH,
        help="""Indicate the cycle durations on:

x: the x-axis, by horizontal spacing between points
y: the y-axis, by their values
both: both axes

Default %(default)s.""",
    )
    arg_parser.add_argument(
        "-d",
        "--dimensions",
        type=parse_size,
        default=plotter.SIZE_A4,
        help="""The size of the image to create.

Supported values are:
  a4
  letter
  <width>x<height><unit>

Supported units are in, cm, and px.

Example: 600x400px

Default a4.""",
    )
    return arg_parser.parse_args()
