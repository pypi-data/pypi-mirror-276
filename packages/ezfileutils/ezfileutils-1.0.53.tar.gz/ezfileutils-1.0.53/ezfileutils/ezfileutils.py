import os
import json
import csv
import xml.etree.ElementTree as ET
import shutil


def remove_file(file_path, verbose=False):
    try:
        os.remove(file_path)
        if verbose:
            print(f"File '{file_path}' removed successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to remove file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def rename_file(file_path, new_name, verbose=False):
    try:
        os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))
        if verbose:
            print(f"File '{file_path}' renamed to '{new_name}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to rename file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def copy_file(source, destination, verbose=False):
    try:
        shutil.copy(source, destination)
        if verbose:
            print(f"File '{source}' copied to '{destination}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{source}' not found.")
        return 1  # Source file not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to copy file '{source}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def move_file(source, destination, verbose=False):
    try:
        shutil.move(source, destination)
        if verbose:
            print(f"File '{source}' moved to '{destination}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{source}' not found.")
        return 1  # Source file not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to move file '{source}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def read_file(file_path, verbose=False):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        if verbose:
            print(f"File '{file_path}' read successfully.")
        return contents, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error

def write_file(file_path, contents, verbose=False):
    try:
        with open(file_path, 'w') as file:
            file.write(contents)
        if verbose:
            print(f"Contents written to file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to write to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def create_directory(directory_path, verbose=False):
    try:
        os.makedirs(directory_path)
        if verbose:
            print(f"Directory '{directory_path}' created successfully.")
        return 0  # Success
    except FileExistsError:
        if verbose:
            print(f"Directory '{directory_path}' already exists.")
        return 1  # Directory already exists
    except PermissionError:
        if verbose:
            print(f"Permission denied to create directory '{directory_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def list_files_in_directory(directory_path, verbose=False):
    try:
        file_list = os.listdir(directory_path)
        if verbose:
            print(f"Files in directory '{directory_path}':")
            for file_name in file_list:
                print(file_name)
        return file_list, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"Directory '{directory_path}' not found.")
        return None, 1  # Directory not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to list files in directory '{directory_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error

def delete_directory(directory_path, verbose=False):
    try:
        shutil.rmtree(directory_path)
        if verbose:
            print(f"Directory '{directory_path}' and its contents deleted successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"Directory '{directory_path}' not found.")
        return 1  # Directory not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to delete directory '{directory_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error

def get_file_size(file_path, unit='kilobytes', verbose=False):
    try:
        file_size = os.path.getsize(file_path)

        if unit == 'bytes':
            converted_size = file_size
        elif unit == 'kilobytes':
            converted_size = file_size / 1024
        elif unit == 'megabytes':
            converted_size = file_size / (1024 * 1024)
        elif unit == 'gigabytes':
            converted_size = file_size / (1024 * 1024 * 1024)
        else:
            raise ValueError(f"Invalid unit '{unit}'. Valid units are 'bytes', 'kilobytes', 'megabytes', 'gigabytes'.")

        if verbose:
            print(f"File size of '{file_path}': {converted_size:.2f} {unit}")

        return converted_size, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to get file size of '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error





# 1. Change File Permissions
def change_file_permissions(file_path, permissions, verbose=False):
    try:
        os.chmod(file_path, permissions)
        if verbose:
            print(f"Permissions of file '{file_path}' changed successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to change permissions of file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 2. Compress File
def compress_file(file_path, archive_path, verbose=False):
    try:
        shutil.make_archive(archive_path, 'zip', os.path.dirname(file_path), os.path.basename(file_path))
        if verbose:
            print(f"File '{file_path}' compressed to '{archive_path}.zip' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to compress file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 3. Decompress File
def decompress_file(archive_path, extract_path, verbose=False):
    try:
        shutil.unpack_archive(archive_path, extract_path)
        if verbose:
            print(f"File '{archive_path}' decompressed to '{extract_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{archive_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to decompress file '{archive_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 4. Encrypt File
def encrypt_file(file_path, key, verbose=False):
    try:
        # Implement encryption logic here
        if verbose:
            print(f"File '{file_path}' encrypted successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to encrypt file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 5. Decrypt File
def decrypt_file(file_path, key, verbose=False):
    try:
        # Implement decryption logic here
        if verbose:
            print(f"File '{file_path}' decrypted successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to decrypt file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 6. Read CSV File
def read_csv_file(file_path, delimiter=',', verbose=False):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            data = [row for row in reader]
        if verbose:
            print(f"CSV file '{file_path}' read successfully.")
        return data, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 7. Write CSV File
def write_csv_file(file_path, data, delimiter=',', verbose=False):
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerows(data)
        if verbose:
            print(f"Data written to CSV file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to write to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 8. Read JSON File
def read_json_file(file_path, verbose=False):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if verbose:
            print(f"JSON file '{file_path}' read successfully.")
        return data, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 9. Write JSON File
def write_json_file(file_path, data, verbose=False):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        if verbose:
            print(f"Data written to JSON file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to write to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 10. Read XML File
def read_xml_file(file_path, verbose=False):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        if verbose:
            print(f"XML file '{file_path}' read successfully.")
        return root, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 11. Write XML File
def write_xml_file(file_path, root, verbose=False):
    try:
        tree = ET.ElementTree(root)
        tree.write(file_path)
        if verbose:
            print(f"XML file '{file_path}' written successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to write to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 12. Read Text File
def read_text_file(file_path, verbose=False):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        if verbose:
            print(f"Text file '{file_path}' read successfully.")
        return contents, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 13. Write Text File
def write_text_file(file_path, contents, verbose=False):
    try:
        with open(file_path, 'w') as file:
            file.write(contents)
        if verbose:
            print(f"Contents written to text file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to write to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 14. Append Text to File
def append_text_to_file(file_path, contents, verbose=False):
    try:
        with open(file_path, 'a') as file:
            file.write(contents)
        if verbose:
            print(f"Contents appended to text file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to append to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 15. Read Binary File
def read_binary_file(file_path, verbose=False):
    try:
        with open(file_path, 'rb') as file:
            contents = file.read()
        if verbose:
            print(f"Binary file '{file_path}' read successfully.")
        return contents, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 16. Write Binary File
def write_binary_file(file_path, contents, verbose=False):
    try:
        with open(file_path, 'wb') as file:
            file.write(contents)
        if verbose:
            print(f"Contents written to binary file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to write to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 17. Append Binary to File
def append_binary_to_file(file_path, contents, verbose=False):
    try:
        with open(file_path, 'ab') as file:
            file.write(contents)
        if verbose:
            print(f"Contents appended to binary file '{file_path}' successfully.")
        return 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to append to file '{file_path}'.")
        return 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return 3  # Other error


# 18. Checksum File
def checksum_file(file_path, algorithm='md5', verbose=False):
    try:
        import hashlib
        hash_algorithm = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                hash_algorithm.update(chunk)
        checksum = hash_algorithm.hexdigest()
        if verbose:
            print(f"Checksum of file '{file_path}' (algorithm: {algorithm}): {checksum}")
        return checksum, 0  # Success
    except FileNotFoundError:
        if verbose:
            print(f"File '{file_path}' not found.")
        return None, 1  # File not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file '{file_path}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 19. Compare Files
def compare_files(file_path1, file_path2, verbose=False):
    try:
        with open(file_path1, 'rb') as file1, open(file_path2, 'rb') as file2:
            content1 = file1.read()
            content2 = file2.read()
        if content1 == content2:
            if verbose:
                print(f"Files '{file_path1}' and '{file_path2}' are identical.")
            return True, 0  # Files are identical
        else:
            if verbose:
                print(f"Files '{file_path1}' and '{file_path2}' are different.")
            return False, 0  # Files are different
    except FileNotFoundError:
        if verbose:
            print(f"File(s) not found: '{file_path1}' or '{file_path2}'.")
        return None, 1  # File(s) not found
    except PermissionError:
        if verbose:
            print(f"Permission denied to read file(s) '{file_path1}' or '{file_path2}'.")
        return None, 2  # Permission denied
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 3  # Other error


# 20. Check File Existence
def check_file_existence(file_path, verbose=False):
    try:
        if os.path.exists(file_path):
            if verbose:
                print(f"File '{file_path}' exists.")
            return True, 0  # File exists
        else:
            if verbose:
                print(f"File '{file_path}' does not exist.")
            return False, 0  # File does not exist
    except Exception as e:
        if verbose:
            print(f"An error occurred: {e}")
        return None, 1  # Other error
