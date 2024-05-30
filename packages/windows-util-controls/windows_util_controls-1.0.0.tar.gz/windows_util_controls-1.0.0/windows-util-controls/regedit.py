import sys

if sys.platform == "win32":
    import winreg

class WinUtilsException(Exception):
    pass

class RegistryException(WinUtilsException):
    pass

class RegistryError(WinUtilsException):
    pass

def ChangeRegistry(reg_type: str, reg: str, new_value: int) -> None:
    if sys.platform != "win32":
        raise WinUtilsException("This function can only be run on Windows.")

    try:
        root_keys = {
            'CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
            'CURRENT_USER': winreg.HKEY_CURRENT_USER,
            'LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
            'USERS': winreg.HKEY_USERS,
            'CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG
        }

        if reg_type not in root_keys:
            raise RegistryException(f"Invalid root key: {reg_type}")

        with winreg.OpenKey(root_keys[reg_type], reg, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, 'Start', 0, winreg.REG_DWORD, new_value)

    except OSError as e:
        raise RegistryError(f"Error changing registry: {e}")
