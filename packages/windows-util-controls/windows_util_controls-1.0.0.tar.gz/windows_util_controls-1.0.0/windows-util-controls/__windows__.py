import os as builtin_os
import sys

class FileOperations:
    @staticmethod
    def remove(file_path):
        try:
            builtin_os.remove(file_path)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")

    @staticmethod
    def rename(src, dst):
        try:
            builtin_os.rename(src, dst)
        except FileNotFoundError:
            print(f"File {src} not found.")
        except Exception as e:
            print(f"Error renaming file from {src} to {dst}: {e}")

class DirectoryOperations:
    @staticmethod
    def mkdir(directory_path):
        try:
            builtin_os.mkdir(directory_path)
        except FileExistsError:
            print(f"Directory {directory_path} already exists.")
        except Exception as e:
            print(f"Error creating directory {directory_path}: {e}")

    @staticmethod
    def listdir(directory_path="."):
        try:
            return builtin_os.listdir(directory_path)
        except FileNotFoundError:
            print(f"Directory {directory_path} not found.")
        except Exception as e:
            print(f"Error listing directory {directory_path}: {e}")
            return []

    @staticmethod
    def rmdir(directory_path):
        try:
            builtin_os.rmdir(directory_path)
        except FileNotFoundError:
            print(f"Directory {directory_path} not found.")
        except Exception as e:
            print(f"Error removing directory {directory_path}: {e}")

class ProcessManagement:
    @staticmethod
    def getpid():
        return builtin_os.getpid()

    @staticmethod
    def exit(code=0):
        sys.exit(code)

class OS:
    file = FileOperations
    directory = DirectoryOperations
    process = ProcessManagement