import os
from pystyle import Center

def cls() -> None:

    """
    Clear screen for multi-os
    """

    if os.name == 'nt': _ = os.system('cls')
    elif os.name == 'posix': _ = os.system('clear')
    else: 
        raise ValueError(f"Unsupported Operating System: {os.name} | Supported: 'nt', 'posix'")

def center(text: str) -> None:
    text = Center.XCenter(text)
    text = Center.YCenter(text)
    return(text)