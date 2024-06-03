import json
import copy
from jsondiff import diff
from jsondiff.symbols import Symbol
from typstdiff.errors import (
    CouldNotParseFiles,
    InvalidJsonDiffOutput,
    CouldNotOpenFile,
    UnsupportedParaType,
)


class Comparison:
    """
    Class for comparing and formatting Json files
    based on output from jsondiff.
    In order to create Typst file with marked changes
    """

    def __init__(
        self, new_path, old_path, insert_format="Underline", delete_format="Strikeout"
    ):
        """
        Initializes the Comparison object.
        Parameters:
            new_path (str): Path to the new Json file.
            old_path (str): Path to the old Json file.
            insert_format (str): Typst format for insertions.
            Default is "Underline".
            delete_format (str): Typst format for deletions.
            Default is "Strikeout".
        """

        self.parsed_new_file = self.parse_load_file(new_path)
        self.parsed_old_file = self.parse_load_file(old_path)
        self.parsed_changed_file = self.parse_load_file(new_path)
        self.diffs = diff(
            self.parsed_old_file,
            self.parsed_changed_file,
            syntax="explicit",
            dump=False,
        )
        self.insert_format = insert_format
        self.delete_format = delete_format

        self.PARAGRAPH_TYPES = {
            dict: lambda para: para["c"] if "c" in para.keys() else para,
            list: lambda para: para,
        }

        self.DICT_TYPES = {
            "Str",
            "Emph",
            "Strong",
            "Superscript",
            "Subscript",
            "SmallCaps",
            "Quoted",
            "Cite",
            "Code",
            "Space",
            "SoftBreak",
            "LineBreak",
            "Math",
            "CodeBlock",
        }

        self.LIST_DICT_TYPES = {"Para", "BulletList", "OrderedList", "Div"}

        self.UPDATE_ONLY = {"Link", "Image", "Math"}

    def parse_load_file(self, path):
        """
        Parses and loads a Json file.
        Parameters:
            path (str): Path to the Json file.
        Returns:
            dict: Parsed Json data.
        """
        try:
            with open(path, "rb") as file:
                return json.load(file)
        except Exception as e:
            raise CouldNotOpenFile(e)

    def decorator_format_para(func):
        def wrapper(self, para, underline_strike):
            para_type = type(para)
            if para_type in self.PARAGRAPH_TYPES:
                para = self.PARAGRAPH_TYPES[para_type](para)
                return func(self, para, underline_strike)
            else:
                raise UnsupportedParaType(para)

        return wrapper

    def parse_dict(self, dict, underline_strike):
        """
        Parses and formats a dictionary structure.
        Parameters:
            dict (dict): Dictionary to be parsed and formatted.
            underline_strike (str): Format for underlining/striking out text.
        """
        if dict["t"] in self.DICT_TYPES:
            para_copy = copy.deepcopy(dict)
            dict["t"] = underline_strike
            dict["c"] = [para_copy]
        else:
            self.parse_list_dict(dict, underline_strike)

    @decorator_format_para
    def parse_list_dict(self, para, underline_strike):
        """
        Parses and formats list or dict structure
        Parameters:
            para (list): List or dict to be parsed and formatted.
            underline_strike (str): Underline if text was inserted,
            or Strikeout if text was deleted.
        """
        if isinstance(para, list):
            for i, element in enumerate(para):
                if isinstance(element, dict):
                    self.parse_dict(para[i], underline_strike)
                elif isinstance(element, list):
                    self.parse_list_dict(para[i], underline_strike)
        else:
            if isinstance(para, dict):
                self.parse_dict(para, underline_strike)

    def parse_header(self, target, position, format_action):
        """
        Parses and formats a header in the Json structure.
        Parameters:
            target (dict): The file to change is Json format.
            position (int): The position of the changed header
            in the Json structure.
            format_action (str): The formatting action to apply.
        """
        for i, element in enumerate(target[position]["c"]):
            if isinstance(element, list):
                for k, value in enumerate(element):
                    if isinstance(value, dict):
                        target_copy = copy.deepcopy(value)
                        target[position]["c"][i][k]["t"] = format_action
                        target[position]["c"][i][k]["c"] = [target_copy]

    def format_changes(self, target, position, format_action):
        """
        Formats changes in the JSON structure based on the specified action.
        Parameters:
            target (dict or list): The file to change is Json format.
            position (int or char): The position of the change
            in the Json structure.
            format_action (str): The formatting action to apply.
        Returns:
            dict: Fragment with changes to insert to new file.
        """
        if isinstance(target[position], list):
            for element in target[position]:
                if element["t"] in self.LIST_DICT_TYPES:
                    self.parse_list_dict(element, format_action)
                    to_insert = [element]
        elif isinstance(target[position], dict) and target[position]["t"] == "Header":
            self.parse_header(target, position, format_action)
            to_insert = target[position]

        elif (
            isinstance(target[position], dict)
            and target[position]["t"] in self.LIST_DICT_TYPES
        ):
            self.parse_list_dict(target[position], format_action)
            to_insert = target[position]
        else:
            target_copy = copy.deepcopy(target[position])
            target[position] = {"t": format_action, "c": [target_copy]}
            to_insert = target[position]
        return to_insert

    def dict_depth(self, d, level=1):
        """
        Calculates the depth of a dictionary of differences.
        Parameters:
            d (dict): The dictionary to calculate depth for.
            level (int): The current level of recursion.
        Returns:
            int: The depth of the dictionary.
        """
        if not isinstance(d, dict) or not d:
            return level
        return max(self.dict_depth(v, level + 1) for k, v in d.items())

    def update_index(self, diffs):
        """
        Updates the indices in the differences dictionary
        to account for changes, if they were made before position.
        Parameters:
            diffs: The dictionary of differences.
        Returns:
            dict: The updated differences dictionary.
        """
        if len(list(diffs.values())) > 1 and all(
            isinstance(key, int) for key in diffs.keys()
        ):
            new_diffs = {}
            to_add = 0
            for key, value in diffs.items():
                if not self.dict_depth(value) > 3:
                    new_diffs[(key, key + to_add)] = value
                    to_add += 1
                else:
                    new_diffs[key, key + to_add] = value
            return new_diffs
        return diffs

    def update(self, diffs, target, old_target, index):
        """
        Updates the target Json structure based on the differences dictionary.
        Parameters:
            diffs: The dictionary of differences.
            target: The target JSON structure to update.
            old_target: The original target JSON structure.
            index: The index or index tuple indicating
            the position of the change.
        """
        diffs = self.update_index(diffs)
        index, index_update = self.split_index_tuple(index)
        for key, value in diffs.items():

            if (
                isinstance(target, list)
                and isinstance(target[index], dict)
                and target[index]["t"] in self.UPDATE_ONLY
            ):
                target[index_update] = {
                    "t": self.insert_format,
                    "c": [target[index_update]],
                }
                target.insert(
                    index_update, {"t": self.delete_format, "c": [old_target[index]]}
                )

            elif (
                isinstance(value, list)
                and self.dict_depth(value[0])
                or self.dict_depth(value) == 2
            ):
                target_copy = copy.deepcopy(target[index_update])
                old_target_copy = copy.deepcopy(old_target[index])
                target[index_update] = {"t": self.delete_format, "c": [old_target_copy]}
                target.insert(
                    index_update + 1, {"t": self.insert_format, "c": [target_copy]}
                )

            elif isinstance(key, Symbol):
                if key.label == "update" and isinstance(list(value.values())[0], dict):
                    self.update(value, target, old_target, (index, index_update))

            else:
                self.update(value, target[index_update], old_target[index], key)

    def parse(self):
        """
        Main function to parse and apply the differences between
        the old and new Json structures.
        It is seperated to 3 parts: update, insert, delete.
        """
        try:
            if self.diffs:
                self.apply_diffs_recursive(
                    self.diffs,
                    self.parsed_changed_file,
                    None,
                    self.parsed_old_file,
                    self.parsed_new_file,
                    "insert",
                )
            self.diffs = diff(
                self.parsed_old_file,
                self.parsed_new_file,
                syntax="explicit",
                dump=False,
            )
            if self.diffs:
                self.apply_diffs_recursive(
                    self.diffs,
                    self.parsed_changed_file,
                    None,
                    self.parsed_old_file,
                    self.parsed_new_file,
                    "delete",
                )
            self.diffs = diff(
                self.parsed_old_file,
                self.parsed_new_file,
                syntax="explicit",
                dump=False,
            )
            if self.diffs:
                key = None
                while not isinstance(key, int):
                    for key, value in self.diffs.items():
                        if isinstance(key, int):
                            self.update(
                                value,
                                self.parsed_changed_file["blocks"],
                                self.parsed_old_file["blocks"],
                                key,
                            )
                        else:
                            self.diffs = value
        except (TypeError, IndexError) as e:
            raise InvalidJsonDiffOutput(e)
        except Exception as e:
            raise CouldNotParseFiles(e)

    def split_index_tuple(self, index):
        """
        Splits the index tuple into two values. There is value of basic index and value of index updated after adding elements before current element.
        Parameters:
            index (int or tuple): The index or index tuple.
        Returns:
            tuple: The split index tuple.
        """
        if isinstance(index, tuple):
            return index[0], index[1]
        else:
            return index, index

    def process_insert(self, diffs, target, parsed_old_file):
        """
        Processes insertions in the Json structure
        based on the differences dictionary.
        Parameters:
            diffs: The list of insertions.
            target: The target Json structure.
            parsed_old_file: Json before the insertions.
        """
        for change in diffs:
            position, _ = change
            target_position, position = self.split_index_tuple(position)
            to_insert = self.format_changes(target, target_position, self.insert_format)
            if isinstance(to_insert, list):
                to_insert = [self.remove_formatting(to_insert[0], self.insert_format)]
            else:
                to_insert = self.remove_formatting(to_insert, self.insert_format)
            parsed_old_file.insert(position, to_insert)

    def process_delete(self, diffs, target, parsed_old_file, parsed_new_file):
        """
        Processes deletions in the Json structure
        based on the differences dictionary.
        Parameters:
            diffs: The list of deletions.
            target: The target Json structure.
            parsed_old_file: The original Json structure before the deletions.
            parsed_new_file: The new Json structure after the deletions.
        """
        diffs.reverse()
        for delete_position in diffs:
            to_insert = self.format_changes(
                parsed_old_file, delete_position, self.delete_format
            )
            target.insert(delete_position, to_insert)
            if isinstance(to_insert, list):
                to_insert = [self.remove_formatting(to_insert[0], self.delete_format)]
            else:
                to_insert = self.remove_formatting(to_insert, self.delete_format)
            parsed_old_file[delete_position] = to_insert
            parsed_new_file.insert(delete_position, to_insert)

    def process_update(
        self, diffs, target, parsed_old_file, parsed_new_file, current_action, only
    ):
        """
        Processes inserts and deletes in the JSON structure based on
        the differences dictionary.
        Parameters:
            diffs: The dictionary of differences.
            target: The target Json structure.
            parsed_old_file: The original Json structure before the updates.
            parsed_new_file: The new Json structure after the updates.
            current_action: The current action being processed.
            only: The action type to process.
        """
        sorted_diffs = self.sort_diffs(diffs)
        for key, value in sorted_diffs:
            if isinstance(key, Symbol):
                next_action = key.label
                self.apply_diffs_recursive(
                    value, target, next_action, parsed_old_file, parsed_new_file, only
                )
            elif (
                isinstance(target, dict)
                and "t" in target.keys()
                and target["t"] in self.UPDATE_ONLY
            ):
                continue
            elif isinstance(value, dict):
                if isinstance(parsed_old_file, list) and isinstance(key, int):
                    if len(parsed_old_file) <= key:
                        self.apply_diffs_recursive(
                            value,
                            target[key],
                            current_action,
                            parsed_old_file,
                            parsed_new_file[key],
                            only,
                        )
                    else:
                        self.apply_diffs_recursive(
                            value,
                            target[key],
                            current_action,
                            parsed_old_file[key],
                            parsed_new_file[key],
                            only,
                        )
                else:
                    self.apply_diffs_recursive(
                        value,
                        target[key],
                        current_action,
                        parsed_old_file[key],
                        parsed_new_file[key],
                        only,
                    )
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        self.apply_diffs_recursive(
                            v,
                            target[key][i],
                            current_action,
                            parsed_old_file[key][i],
                            parsed_new_file[key][i],
                            only,
                        )
                    else:
                        target[key][i] = v

    def update_insert_indexes(self, diffs):
        """
        Updates the indexes for insertions in the differences dictionary based on deleted elements in the same structure.
        Parameters:
            diffs (dict): The dictionary of differences.
        Returns:
            dict: The updated differences dictionary
            with adjusted insertion indexes.
        """
        for key, value in diffs.items():
            if isinstance(key, Symbol):
                if key.label == "insert":
                    insert_diffs = value
                if key.label == "delete":
                    delete_diffs = value
        new_insert_diffs = []
        for insert in insert_diffs:
            new_insert_diffs.append(
                (
                    (
                        insert[0],
                        insert[0]
                        + len([num for num in delete_diffs if num < insert[0]]),
                    ),
                    insert[1],
                )
            )
        for key, value in diffs.items():
            if isinstance(key, Symbol) and key.label == "insert":
                diffs[key] = new_insert_diffs
                break
        return diffs

    def sort_diffs(self, diffs):
        """
        Sorts the differences dictionary, so that insert and delete operations are before update operation.
        Parameters:
            diffs (dict): The dictionary of differences.
        Returns:
            list: The sorted list of differences tuples.
        """
        sorted_diffs = []
        for key, value in reversed(list(diffs.items())):
            if key == Symbol("insert"):
                sorted_diffs.insert(0, (key, value))
            else:
                sorted_diffs.append((key, value))
        return sorted_diffs

    def apply_diffs_recursive(
        self, diffs, target, current_action, parsed_old_file, parsed_new_file, only
    ):
        """
        Recursively applies the differences to the Json structure.
        Parameters:
            diffs (dict): The dictionary of differences.
            target (dict): The target Json structure.
            current_action (str): The current action being processed.
            parsed_old_file (dict): The original Json
            structure before the changes.
            parsed_new_file (dict): The new Json structure after the changes.
            only (str): The action type to process.
        """
        if isinstance(diffs, dict):
            if all(
                elem
                in [
                    symbol.label
                    for symbol in list(diffs.keys())
                    if isinstance(symbol, Symbol)
                ]
                for elem in ["insert", "delete"]
            ):
                diffs = self.update_insert_indexes(diffs)

        if current_action is None or current_action == "update":
            self.process_update(
                diffs, target, parsed_old_file, parsed_new_file, current_action, only
            )

        elif current_action == "insert" and only == "insert":
            self.process_insert(diffs, target, parsed_old_file)

        elif current_action == "delete" and only == "delete":
            self.process_delete(diffs, target, parsed_old_file, parsed_new_file)

    def remove_formatting(self, data, formatting):
        """
        Removes formatting from changed structure 
        so that it can be added to opposite operation file handler. 
        The reason is that jsondiff will not find 
        differences after they were processed.
        Parameters:
            data (dict): dictionary with changed element with marked differences
            formatting (str): name of marking to remove
        Returns:
            data (dict): dictionary without marking
        """
        if isinstance(data, dict):
            if data.get("t") == formatting:
                return data.get("c")[0]
            else:
                return {
                    key: self.remove_formatting(value, formatting)
                    for key, value in data.items()
                }
        elif isinstance(data, list):
            return [self.remove_formatting(item, formatting) for item in data]
        else:
            return data
