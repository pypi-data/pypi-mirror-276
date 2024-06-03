class CouldNotParseFiles(Exception):
    """Exception raised when a file could not be parsed by Pandoc."""

    def __init__(self, e):
        super().__init__(f"Used type unsupported by pandoc: [{e}]")


class InvalidJsonDiffOutput(Exception):
    """Exception raised when the output of jsondiff cannot be parsed."""

    def __init__(self, e):
        super().__init__(f"Could not parse jsondiff output: [{e}]")


class CouldNotOpenFile(Exception):
    """Exception raised when a file could not be opened."""

    def __init__(self, e):
        super().__init__(f"Could not file: [{e}]")


class UnsupportedParaType(Exception):
    """Exception raised when an unsupported type is
    encountered for a paragraph."""

    def __init__(self, para):
        super().__init__(f"Unsupported type for para: {type(para)}")
