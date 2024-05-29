# MIT License

# Copyright (c) 2023 Postek Electronics Co., Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# For the functions that only have pass in this file, please refer to the ox script development manual for details
# The functions are marked with pass only because they are meanted to be executed on the printer and will not function
# correctly on your device. Please use the runtime environment on Postek printers for most accurate results

# ===========================================================#
# General purpose functions
# These functions can be executed directly on your device
# and is designed to help you with data parsing, connecting to
# databases, and getting data in the format to be printed
# ===========================================================#
import os
import re
import inspect

def setup():
    calling_frame = inspect.stack()[-1]
    calling_file = os.path.abspath(calling_frame.filename)
    os.chdir(os.path.dirname(calling_file))

setup()

def retrieve_data(item_list: list, index: int, excluding=""):
    """
    retrieve_data is used to retrieve data from a list of items. It can be used to retrieve data from a list
        of items and user can use the excluding parameter to exclude items from the list. the excluding parameter
        should be in the following format "starting_index;ending_index;exclusion_index". 

    Parameters:
        item_list (list): The list of items to be retrieved from   
        index (int): The index of the item to be retrieved
        excluding (str, optional): The string that defines the exclusion of items. Defaults to "".

    Returns:
        str: The data from the item_list at the index specified with the exclusion applied
    """
    if excluding == "":
        return item_list[index]
    else:
        pattern = r'^([\d,-]*;){2}[\d,-]*$'
        if re.match(pattern=pattern, string=excluding):
            return _exclusion(item_list, index, excluding)
        else:
            print(
                "excluding string in wrong format, it should follow starting_index;ending_index;exclusion_index(, and - allowed)")
            return "exclusion string error"

# This is an internal function. Not meant to be used directly


def _exclusion(item_list: list, current_index: int, parameters=";;"):
    parameters = parameters.split(";")
    i = 0
    for items in parameters:
        if items == "":
            if i == 0:
                parameters[0] = "1"
            elif i == 1:
                parameters[1] = str(len(item_list))
            elif i == 2:
                parameters[2] = ""
        i = i + 1
    temp = item_list[:]
    return _get_item_with_exclusion(
        temp, current_index, int(parameters[0]), int(
            parameters[1]), parameters[2]
    )

# This is an internal function. Not meant to be used directly


def _get_item_with_exclusion(
    item_list: list,
    current_index: int,
    starting_index: int,
    ending_index: int,
    exclusion_index: str,
):
    try:
        current_index = current_index + starting_index
        if (current_index > ending_index):
            return "Index Reached Ending Index"
        excluding_rows = []
        if exclusion_index != "":
            if "," in exclusion_index:
                exclusion_index = exclusion_index.split(",")
                for item in exclusion_index:
                    excluding_rows.extend(_get_excluding_row(item))
            else:
                excluding_rows = _get_excluding_row(exclusion_index)
        num_removed = 0
        for item in excluding_rows:
            if (int(item) > ending_index) or int(item) > len(item_list):
                print("exclusion index greater than ending index")
                break
            item_list.remove(item_list[int(item) - num_removed])
            num_removed = num_removed + 1
        return item_list[current_index]
    except IndexError:
        return "Index Error"

# This is an internal function. Not meant to be used directly


def _get_excluding_row(exclusion_index: str):
    if "-" in exclusion_index:
        exclusion_index = exclusion_index.split("-")
        return [
            str(num)
            for num in range(int(exclusion_index[0]), int(exclusion_index[1]) + 1)
        ]
    else:
        return [(exclusion_index)]
    

def PTK_GetAllFormVariable(filepath):
    variable_locations = {}
    if os.access(filepath, os.F_OK):
        with open(filepath, "rb") as fp:
            # read all lines using readline()
            lines = fp.readlines()
            for line in lines:
                # check if string present on a current line
                word = b"OX:"
                if line.find(word) != -1:
                    for item in reversed(line.split(b"#")):
                        if item.find(word) != -1:
                            key = item
                            item = item.replace(word, b"")
                            item = item.replace(b'"', b"")
                            item = item.replace(b"#\n", b"")
                            item = item.replace(b"#\r\n", b"")
                            if item not in variable_locations.keys():
                                variable_locations[item] = [
                                    {
                                        "position": lines.index(line),
                                        "line": line,
                                        "replacement_key": b'#' + key + b'#',
                                    },
                                ]
                            elif item in variable_locations.keys():
                                variable_locations[item].append(
                                    {
                                        "position": lines.index(line),
                                        "line": line,
                                        "replacement_key": b'#' + key + b'#',
                                    }
                                )
        return variable_locations


def PTK_UpdateAllFormVariables(filename, **kwargs):
    filepath = filename
    if os.access(filepath, os.F_OK):
        variable_locations = PTK_GetAllFormVariable(filepath)
        with open(filepath, "rb") as text_file:
            lines = [line for line in text_file]
            for key, value in kwargs.items():
                key = bytes(key, encoding="utf-8")
                value = bytes(value, encoding="utf-8")
                if key in variable_locations.keys():
                    for items in variable_locations[key]:
                        position = items["position"]
                        line = items["line"]
                        line = line.replace(
                            items["replacement_key"], value
                        )
                        lines[position] = line + b"\n"
            return b"".join(lines) + b"\r\n"
    else:
        raise FileNotFoundError(filename + " can't be found")