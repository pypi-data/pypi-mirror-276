import sys
import argparse
import os

from typstdiff.file_converter import FileConverter
from typstdiff.comparison import Comparison

# Define the possible customizations

typst_predefined_colors = {
    ("bl", "black", "luma0"): "black",
    ("ga", "gray", "luma170"): "gray",
    ("si", "silver", "luma221"): "silver",
    ("wh", "white", "luma255"): "white",
    ("na", "navy", "#001f3f"): "navy",
    ("bu", "blue", "#0074d9"): "blue",
    ("aq", "aqua", "#7fdbff"): "aqua",
    ("te", "teal", "#39cccc"): "teal",
    ("ea", "eastern", "#239dad"): "eastern",
    ("pu", "purple", "#b10dc9"): "purple",
    ("fu", "fuchsia", "#f012be"): "fuchsia",
    ("ma", "maroon", "#85144b"): "maroon",
    ("re", "red", "#ff4136"): "red",
    ("or", "orange", "#ff851b"): "orange",
    ("ye", "yellow", "#ffdc00"): "yellow",
    ("ol", "olive", "#3d9970"): "olive",
    ("gr", "green", "#2ecc40"): "green",
    ("li", "lime", "#01ff70"): "lime",
}


def isValidHexaCode(hex_string):
    """
    Check if a given string is a valid hexadecimal color code.
    Parameters:
        hex_string (str): The string to be checked.
    Returns:
        bool: True if the string is a valid hexadecimal color code,
        False otherwise.
    """
    if (
        hex_string.startswith("#")
        and (len(hex_string) in {4, 7})
        and all(c in "0123456789abcdefABCDEF" for c in hex_string[1:])
    ):
        return True
    return False


def parse_color_param(provided_color):
    """
    Parses a provided color parameter and
    returns the corresponding color value.
    Parameters:
        provided_color (str): The color parameter to be parsed.
    Returns:
        str or None: The corresponding color value if it is a predefined color
        or a valid hexadecimal color code. None otherwise.
    """
    for key_tuple in typst_predefined_colors:
        if provided_color in key_tuple:
            return typst_predefined_colors[key_tuple]

    if isValidHexaCode(provided_color):
        return provided_color

    return None


def format_styles(custom_setting):
    """
    Generates a list of format lines based on the provided custom
    settings for highlighting and font styles.
    Parameters:
        custom_setting (CustomSetting): An object containing the custom
        settings for highlighting and font styles.
    Returns:
        List[str]: A list of format lines that can be used to customize
        the appearance of inserted and deleted changes in a Typst file.
    """
    format_lines = []

    insert_highlight = parse_color_param(custom_setting.insert_highlight)
    insert_font = parse_color_param(custom_setting.insert_font)
    delete_highlight = parse_color_param(custom_setting.delete_highlight)
    delete_font = parse_color_param(custom_setting.delete_font)

    if insert_highlight:
        format_lines.append(
            f"#show underline : it => {{highlight(fill: {insert_highlight},"
            f" text({insert_font or 'black'}, it))}}"
        )
    elif insert_font:
        format_lines.append(f"#show underline : it => {{text({insert_font}, it)}}")

    if delete_highlight:
        format_lines.append(
            f"#show strike : it => {{highlight(fill: {delete_highlight},"
            f" text({delete_font or 'black'}, it))}}"
        )
    elif delete_font:
        format_lines.append(f"#show strike : it => {{text({delete_font}, it)}}")

    return format_lines


def check_if_typst_extension(filename):
    """
    Check if the given filename has a .typ extension and if it exists.
    Parameters:
        filename (str): The name of the file to be checked.
    Returns:
        str: The original filename if it has a .typ extension and exists.
    Raises:
        argparse.ArgumentTypeError: If the filename does not have
          a .typ extension or if it does not exist.
    """
    if not filename.lower().endswith(".typ"):
        raise argparse.ArgumentTypeError(
            f"File '{filename}' does not have a .typ extension"
        )
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f"File '{filename}' does not exist")
    return True


def get_file_name_without_extension(filename):
    """
    Extract the file name without its extension.
    Parameters:
        filename (str): The path to the file.
    Returns:
        str: The file name without the extension.
    """
    return os.path.splitext(filename)[0]


def get_file_path_without_extension(filename):
    """
    Extract the file path without its extension.
    Parameters:
        filename (str): The path to the file.
    Returns:
        str: The file path without the extension.
    """
    return os.path.splitext(os.path.basename(filename))[0]


def main():
    """
    Parses command line arguments and performs the main
    functionality of the program.
    Parameters:
        arguments (List[str]): The command line arguments
        passed to the program.
    Returns:
        None
    Raises:
        SystemExit: If the user provides invalid command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="TypstDiff",
        description="Mark differences between two Typst files.",
        epilog="Copyright (c) 2024, Dominika Ferfecka,"
        + " Sara Fojt, Małgorzata Kozłowska",
    )

    parser.add_argument(
        "old_version", type=str, help="Path to an old version of Typst file"
    )
    parser.add_argument(
        "new_version", type=str, help="Path to a new version of Typst file"
    )
    parser.add_argument(
        "diff_output_file", type=str, help="Path to the output diff file"
    )

    parser.add_argument(
        "-ih",
        "--insert-highlight",
        help="Set custom highlight to inserted changes",
        type=str,
        default="",
    )
    parser.add_argument(
        "-if",
        "--insert-font",
        help="Set custom font to inserted changes",
        type=str,
        default="",
    )
    parser.add_argument(
        "-dh",
        "--delete-highlight",
        help="Set custom highlight to deleted changes",
        type=str,
        default="",
    )
    parser.add_argument(
        "-df",
        "--delete-font",
        help="Set custom font to deleted changes",
        type=str,
        default="",
    )

    args = parser.parse_args(sys.argv[1:])

    for arg_name in ["old_version", "new_version", "diff_output_file"]:
        check_if_typst_extension(getattr(args, arg_name))
        setattr(
            args, arg_name, get_file_name_without_extension(getattr(args, arg_name))
        )

    format_lines = format_styles(args)

    file_converter = FileConverter()
    file_converter.convert_with_pandoc(
        "typst", "json", f"{args.new_version}.typ", f"{args.new_version}.json"
    )
    file_converter.convert_with_pandoc(
        "typst", "json", f"{args.old_version}.typ", f"{args.old_version}.json"
    )
    comparison = Comparison(f"{args.new_version}.json", f"{args.old_version}.json")

    comparison.parse()
    file_converter.write_to_json_file(
        comparison.parsed_changed_file, f"{args.diff_output_file}.json"
    )
    file_converter.convert_with_pandoc(
        "json", "typst", f"{args.diff_output_file}.json", f"{args.diff_output_file}.typ"
    )
    file_converter.write_lines(format_lines, f"{args.diff_output_file}.typ")
    file_converter.compile_to_pdf(f"{args.diff_output_file}.typ")


if __name__ == "__main__":
    main(sys.argv)
