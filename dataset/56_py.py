import os


def open_file(path_str: str, file_to_open) -> bool:
  file_path = path_str

  if not os.path.exists(file_path):
    return False

  if not os.path.isfile(file_path):
    return False

  if not file_to_open.closed:
    file_to_open.close()

  file_to_open = open(file_path)

  return not file_to_open.closed