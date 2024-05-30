from ._labeling_tool import gui
from pathlib import Path
import argparse
from argparse import RawTextHelpFormatter


def get_args():
    # Short description
    description = """Labeling tool for micronuclei detection."""

    # Add parser
    parser = argparse.ArgumentParser(description, formatter_class=RawTextHelpFormatter)

    # Tool Input
    input = parser.add_argument_group(title="Input")
    input.add_argument("-i", "--input", dest="input", action="store", required=True, default="../data/image.ome.tif",
                       help="Pathway to input image. [default='../data']")
    input.add_argument("-m", "--mask", dest="mask", action="store", required=True, default="../data/mask.tif",
                       help="Pathway to mask image. [default='../data/mask.tif']")

    # Tool output
    output = parser.add_argument_group(title="Output")
    output.add_argument("-o", "--out", dest="out", action="store", required=True, default="../out/labels.csv",
                        help="Path to the output data folder. [default='../out']")

    # Parse arguments
    args = parser.parse_args()

    # Standardize paths
    args.input = Path(args.input).resolve()
    args.mask = Path(args.mask).resolve()
    args.out = Path(args.out).resolve()

    return args


def main(args):
    # Run GUI
    gui(args)


if __name__ == "__main__":
    # Get arguments
    args = get_args()

    # Run main function
    main(args)
