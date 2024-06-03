
# ezfileutils

**ezfileutils** is a Python utility script that simplifies common file operations. It provides a set of functions to perform tasks such as file removal, renaming, copying, moving, reading, writing, directory management, and more.

## Installation

To install **ezfileutils**, you can use pip:

```bash
pip install ezfileutils
```

## Usage

Here's how you can use **ezfileutils** in your Python scripts:

```python
from ezfileutils import *

# Example usage
result, error_code = remove_file('file.txt', verbose=True)
if result == 0:
    print("File removed successfully!")
else:
    print(f"Error: {error_code}")
```

## Functions

- `remove_file(file_path, verbose=False)`: Removes a file.
- `rename_file(file_path, new_name, verbose=False)`: Renames a file.
- `copy_file(source, destination, verbose=False)`: Copies a file.
- `move_file(source, destination, verbose=False)`: Moves a file.
- `read_file(file_path, verbose=False)`: Reads the contents of a file.
- `write_file(file_path, contents, verbose=False)`: Writes contents to a file.
- `create_directory(directory_path, verbose=False)`: Creates a directory.
- `list_files_in_directory(directory_path, verbose=False)`: Lists files in a directory.
- `delete_directory(directory_path, verbose=False)`: Deletes a directory.
- `get_file_size(file_path, unit='kilobytes', verbose=False)`: Gets the size of a file.
- `change_file_permissions(file_path, permissions, verbose=False)`: Changes file permissions.
- `compress_file(file_path, archive_path, verbose=False)`: Compresses a file.
- `decompress_file(archive_path, extract_path, verbose=False)`: Decompresses a file.
- `encrypt_file(file_path, key, verbose=False)`: Encrypts a file.
- `decrypt_file(file_path, key, verbose=False)`: Decrypts a file.
- `read_csv_file(file_path, delimiter=',', verbose=False)`: Reads a CSV file.
- `write_csv_file(file_path, data, delimiter=',', verbose=False)`: Writes data to a CSV file.
- `read_json_file(file_path, verbose=False)`: Reads a JSON file.
- `write_json_file(file_path, data, verbose=False)`: Writes data to a JSON file.
- `read_xml_file(file_path, verbose=False)`: Reads an XML file.
- `write_xml_file(file_path, root, verbose=False)`: Writes XML data to a file.
- `read_text_file(file_path, verbose=False)`: Reads a text file.
- `write_text_file(file_path, contents, verbose=False)`: Writes contents to a text file.
- `append_text_to_file(file_path, contents, verbose=False)`: Appends text to a text file.
- `read_binary_file(file_path, verbose=False)`: Reads a binary file.
- `write_binary_file(file_path, contents, verbose=False)`: Writes binary data to a file.
- `append_binary_to_file(file_path, contents, verbose=False)`: Appends binary data to a file.
- `checksum_file(file_path, algorithm='md5', verbose=False)`: Computes the checksum of a file.
- `compare_files(file_path1, file_path2, verbose=False)`: Compares two files.
- `check_file_existence(file_path, verbose=False)`: Checks if a file exists.

## Contributing

Contributions are welcome! If you have any ideas for new features or improvements, please open an issue or submit a pull request.

## Extra Stuff
Im going to try and add all sorts of useful functions to this script and optimize the code as i go. I hope you enjoy! <333

## Author
- [@suzuya](https://suzuyaa.carrd.co)
```
