import os
from . import reset
from shutil import get_terminal_size

def cls() -> None:

    """
    Clear screen for multi-os
    """

    print(reset)
    if os.name == 'nt': _ = os.system('cls')
    elif os.name == 'posix': _ = os.system('clear')
    else: raise ValueError(f"Unsupported Operating System: {os.name} | Supported: 'nt', 'posix'")