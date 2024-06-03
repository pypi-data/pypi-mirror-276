import os
import platform
from pyvisjs.utils import save_file, open_file, list_of_dicts_to_dict_of_lists, dict_of_lists_to_list_of_dicts
from unittest.mock import patch


@patch("os.makedirs")
@patch("builtins.open")
@patch("os.getcwd")
def test_save_file_with_file_name(mock_getcwd, mock_open, mock_makedirs):
    # init
    FULL_PATH = os.path.join("working_dir", "output.html")
    DIR_PATH, _ = os.path.split(FULL_PATH)

    # mock
    mock_getcwd.return_value = "working_dir"
    mock_write = mock_open.return_value.__enter__().write

    # call
    file_result = save_file("output.html", "<html>hello</html>") # <------------------

    # assert
    mock_getcwd.assert_called_once()
    mock_makedirs.assert_called_once_with(DIR_PATH, exist_ok=True)
    mock_open.assert_called_once_with(FULL_PATH, "w", encoding="utf-8")
    mock_write.assert_called_once_with("<html>hello</html>")
    assert file_result == FULL_PATH


@patch("os.makedirs")
@patch("builtins.open")
@patch("os.getcwd")
def test_save_file_with_relative_path(mock_getcwd, mock_open, mock_makedirs):
    # init
    REL_PATH = os.path.join("relative_dir", "output.html")
    FULL_PATH = os.path.join("working_dir", REL_PATH)
    DIR_PATH, _ = os.path.split(FULL_PATH)

    # mock
    mock_getcwd.return_value = "working_dir"
    mock_write = mock_open.return_value.__enter__().write

    # call
    file_result = save_file(REL_PATH, "<html>hello</html>") # <------------------

    # assert
    mock_getcwd.assert_called_once()
    mock_makedirs.assert_called_once_with(DIR_PATH, exist_ok=True)
    mock_open.assert_called_once_with(FULL_PATH, "w", encoding="utf-8")
    mock_write.assert_called_once_with("<html>hello</html>")
    assert file_result == FULL_PATH


@patch("os.makedirs")
@patch("builtins.open")
@patch("os.getcwd")
def test_save_file_with_absolute_path(mock_getcwd, mock_open, mock_makedirs):
    # init
    if platform.system() == "Windows":
        FULL_PATH = os.path.join("c:" + os.sep, "relative_dir", "output1.html")
    elif platform.system() == "Linux":
        FULL_PATH = os.path.join(os.sep, "relative_dir", "output1.html")
        
    DIR_PATH, _ = os.path.split(FULL_PATH)

    # mock
    mock_write = mock_open.return_value.__enter__().write

    # call
    file_result = save_file(FULL_PATH, "<html>hello</html>") # <------------------

    # assert
    mock_getcwd.assert_not_called()
    mock_makedirs.assert_called_once_with(DIR_PATH, exist_ok=True)
    mock_open.assert_called_once_with(FULL_PATH, "w", encoding="utf-8")
    mock_write.assert_called_once_with("<html>hello</html>")
    assert file_result == FULL_PATH

def test_list_of_dicts_to_dict_of_lists():
    # init
    LST = [
        {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
        {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
        {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
        {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
        {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
    ]

    DCT = {
    "id": [1, 2, 3, 4, 5, 6, 7],
    "from": ["AM", "AM", "AM", "JL", "JL", "AM", "DM"],
    "to":   ["JL", "JL", "DM", "Hypo", "AM", "LMT", "McDnlds"],
    "amount": [100, 100, 20, 150, 50, 33, 5],
    "country": ["LV", "LV", "EE", "GB", "LV", "LV", "US"],
    "class": ["pers", "pers", "pers", "hypo", "pers", "tele", "food"],
}
    # mock
    # call
    result = list_of_dicts_to_dict_of_lists(LST)
    # assert
    assert result == DCT

def test_dict_of_lists_to_list_of_dicts():
    # init
    LST = [
        {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
        {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
        {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
        {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
        {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
    ]

    DCT = {
    "id": [1, 2, 3, 4, 5, 6, 7],
    "from": ["AM", "AM", "AM", "JL", "JL", "AM", "DM"],
    "to":   ["JL", "JL", "DM", "Hypo", "AM", "LMT", "McDnlds"],
    "amount": [100, 100, 20, 150, 50, 33, 5],
    "country": ["LV", "LV", "EE", "GB", "LV", "LV", "US"],
    "class": ["pers", "pers", "pers", "hypo", "pers", "tele", "food"],
}
    # mock
    # call
    result = dict_of_lists_to_list_of_dicts(DCT)
    # assert
    assert result == LST