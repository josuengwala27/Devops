import time
import sys
from colorama import Fore

def sword_clash():
    frames = [
        """
    ⚔️
        """,
        """
   ⚔️ 
        """,
        """
  ⚔️  
        """,
        """
 ⚔️   
        """,
        """
⚔️    
        """
    ]
    
    for frame in frames:
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
        time.sleep(0.1)

def magic_sparkle():
    frames = [
        "✨ ", " ✨", "  ✨", "   ✨", "    ✨"
    ]
    
    for frame in frames:
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
        time.sleep(0.1)

def health_bar(percentage, width=20):
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    color = Fore.GREEN if percentage > 50 else Fore.YELLOW if percentage > 25 else Fore.RED
    return f"{color}[{bar}] {percentage}%{Fore.RESET}" 