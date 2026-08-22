def open_file(path: str, file_to_open) -> bool:
  if not file_to_open.closed:
    file_to_open.close()

  file_to_open = open(path)

  return not file_to_open.closed