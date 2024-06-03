import subprocess
import json


class FileConverter:
    """
    Class for to convert files between Json and Typst using Pandoc library.
    Also compiles Typst file to PDF
    """

    def write_to_json_file(
        self, json_data, output_file="comparison_new.json", indent=4
    ):
        """
        Writes Json data to a file.
        Parameters:
            json_data (dict): The Json data to be written.
            output_file (str): The path to the output file.
            Default is 'comparison_new.json'.
            indent (int): The number of spaces used for indentation.
            Default is 4.
        """
        with open(output_file, "w") as updated_file:
            json.dump(json_data, updated_file, indent=indent)

    def convert_with_pandoc(self, from_format, to_format, input_file, output_file):
        """
        Converts a file using Pandoc library.
        Parameters:
            from_format (str): The input file format (json/typst).
            to_format (str): The output file format (json/typst).
            input_file (str): The path to the input file.
            output_file (str): The path to the output file.
        """
        with open(output_file, "w") as output_new_file:
            subprocess.run(
                ["pandoc", "-f", from_format, "-t", to_format, input_file],
                stdout=output_new_file,
            )
        output_new_file.close()

    def write_lines(self, lines: list, file_path):
        """
        Appends lines to an existing file.
        Parameters:
            lines (list): The list of lines to append.
            file_path (str): The path to the existing file.
        """
        with open(file_path, "r+") as file:
            content = file.read()
            file.seek(0, 0)
            for line in lines:
                file.write(line + "\n")
            file.write(content)
        file.close()

    def compile_to_pdf(self, input_file):
        """
        Compiles a file to PDF format using Typst.
        Uses subprocess library to run bash command.
        Parameters:
            input_file (str): The path to the input file.
        """
        subprocess.run(["typst", "compile", input_file])
