"""
This module is used to interact with the Windows operating system. 
It provides classes and functions to perform various operations such as: 
# file operations, 
# directory operations, 
# process management, 
# and more.


"""



import subprocess
import winreg
import input
from __windows__ import FileOperations, DirectoryOperations, ProcessManagement, OS
class SysRoot:
    def __init__(self):
        res = subprocess.run("echo %SystemRoot%", shell=True, stdout=subprocess.PIPE)
        self.path = res.stdout.decode().strip()  # Get the output and remove any trailing whitespace

    def __str__(self):
        return f"SystemRoot: {self.path}"

class chnReg:
    def __init__(self, key, sub_key, value_name, value, value_type):
        self.key = key
        self.sub_key = sub_key
        self.value_name = value_name
        self.value = value
        self.value_type = value_type

    def change_registry(self):
        try:
            registry_key = winreg.OpenKey(self.key, self.sub_key, 0, winreg.KEY_WRITE)
            if self.value_type == 'REG_SZ':
                winreg.SetValueEx(registry_key, self.value_name, 0, winreg.REG_SZ, self.value)
            elif self.value_type == 'REG_DWORD':
                winreg.SetValueEx(registry_key, self.value_name, 0, winreg.REG_DWORD, self.value)
            elif self.value_type == 'REG_BINARY':
                winreg.SetValueEx(registry_key, self.value_name, 0, winreg.REG_BINARY, self.value)
            elif self.value_type == 'REG_QWORD':
                winreg.SetValueEx(registry_key, self.value_name, 0, winreg.REG_QWORD, self.value)
            else:
                raise ValueError("Unsupported registry value type")
            winreg.CloseKey(registry_key)
            print(f"Registry value {self.value_name} set to {self.value}")
        except WindowsError as e:
            print(f"Error changing registry: {e}")

if __name__ == "__main__":
    # Get SystemRoot path
    system_root = SysRoot()
    print(system_root)

    # Example of changing a registry value
    # Change these values to match your specific need
    key = winreg.HKEY_CURRENT_USER
    sub_key = r'Software\MyApp'
    value_name = 'MyValue'
    value = 'NewValue'  # Change to desired value
    value_type = 'REG_SZ'  # Can be 'REG_SZ', 'REG_DWORD', 'REG_BINARY', 'REG_QWORD'


    reg_changer = chnReg(key, sub_key, value_name, value, value_type)
    reg_changer.change_registry()