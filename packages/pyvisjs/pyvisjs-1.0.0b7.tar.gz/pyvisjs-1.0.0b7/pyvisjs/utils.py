import subprocess
import os


def open_file(url):
    """
    Parameters
    ---------
    url : str
        Web url or a file path on your computer
    >>> open_file("https://stackoverflow.com")
    >>> open_file("\\\\pyvisjs\\\\templates\\\\basic.html")  
    """

    try: # should work on Windows
        os.startfile(url)
    except AttributeError:
        try: # should work on MacOS and most linux versions
            subprocess.call(['open', url])
        except:
            raise

def save_file(file_path: str, file_content: str) -> str:
    """
    if file_path is absolute then output_dir will be ignored
    """
    if os.path.isabs(file_path):
        output_dir, file_name = os.path.split(file_path)
    else:
        relative_path = os.path.join(os.getcwd(), file_path)
        output_dir, file_name = os.path.split(relative_path)

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

    return file_path

def list_of_dicts_to_dict_of_lists(data):
    if not data:
        return {}
    keys = data[0].keys()
    dict_of_lists = {key: [] for key in keys}
    for entry in data:
        for key in keys:
            dict_of_lists[key].append(entry[key])
    return dict_of_lists

def dict_of_lists_to_list_of_dicts(data):
    keys = data.keys()
    list_of_dicts = []
    for i in range(len(next(iter(data.values())))):
        entry = {key: data[key][i] for key in keys}
        list_of_dicts.append(entry)
    return list_of_dicts
