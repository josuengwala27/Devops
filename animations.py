import time
import sys
from colorama import Fore, Style
import random

def clear_line():
    """Efface la ligne courante"""
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def magic_sparkle(duration=1.0, color=Fore.CYAN):
    """Animation améliorée pour les sorts magiques"""
    frames = [
        "✨ * . ⋆ ", 
        "* ✨ . ⋆ ", 
        "⋆ * ✨ . ",
        ". ⋆ * ✨ "
    ]
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            sys.stdout.write('\r' + color + frame + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
    clear_line()

def sword_clash(duration=1.0):
    """Animation améliorée pour les attaques physiques"""
    frames = [
        "⚔️     ",
        " ⚔️    ",
        "  ⚔️   ",
        "   ⚔️  ",
        "    ⚔️ ",
        "   ⚔️  ",
        "  ⚔️   ",
        " ⚔️    "
    ]
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(0.1)
    clear_line()

def fire_effect(duration=1.0):
    """Animation pour les effets de feu"""
    frames = [
        "🔥    ",
        " 🔥   ",
        "  🔥  ",
        "   🔥 ",
        "    🔥"
    ]
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(0.1)
    clear_line()

def arrow_shot(duration=1.0):
    """Animation pour les tirs d'archer"""
    frames = [
        "🏹     ",
        "🏹➳    ",
        "🏹 ➳   ",
        "🏹  ➳  ",
        "🏹   ➳ ",
        "🏹    ➳"
    ]
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(0.1)
    clear_line()

def healing_effect(duration=1.0):
    """Animation pour les sorts de soin"""
    frames = [
        "💚 ",
        "💚 ✨",
        "💚 ✨ .",
        "💚 ✨ . *",
        "💚 ✨ . * ⋆"
    ]
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            sys.stdout.write('\r' + Fore.GREEN + frame + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
    clear_line()

def health_bar(percentage, width=20):
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    color = Fore.GREEN if percentage > 50 else Fore.YELLOW if percentage > 25 else Fore.RED
    return f"{color}[{bar}] {percentage}%{Fore.RESET}" 