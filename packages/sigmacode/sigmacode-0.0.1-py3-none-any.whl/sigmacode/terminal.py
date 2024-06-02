from pystyle import Center
import os

def cls() -> None:
    
    """
    Clear screen for multi-os
    """

    if os.name == 'nt': _ = os.system('cls')
    elif os.name == 'posix': _ = os.system('clear')
    else: 
        raise ValueError(f"Unsupported Operating System: {os.name} | Supported: 'nt', 'posix'")
    
def center(text: str):
    text = Center.XCenter(text)
    text = Center.YCenter(text)
    return(text)