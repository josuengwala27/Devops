import shutil

def get_terminal_size():
    """Récupère la taille du terminal"""
    try:
        columns, _ = shutil.get_terminal_size()
        return columns
    except:
        return 80  # Valeur par défaut si impossible de récupérer la taille

def create_responsive_format(total_width, ratios):
    """Crée un format de tableau responsif basé sur les ratios donnés"""
    available_width = total_width - (len(ratios) + 1) * 3  # Espace pour les bordures
    widths = [max(10, int(available_width * ratio)) for ratio in ratios]
    return widths

def create_border(widths, border_type="middle"):
    """Crée une bordure responsive avec des largeurs fixes"""
    borders = {
        "top": ("╔", "╦", "╗"),
        "middle": ("╠", "╬", "╣"),
        "bottom": ("╚", "╩", "╝"),
        "single": ("┌", "┬", "┐"),
        "single_middle": ("├", "┼", "┤"),
        "single_bottom": ("└", "┴", "┘")
    }
    
    if border_type not in borders:
        border_type = "middle"
        
    start, middle, end = borders[border_type]
    
    parts = []
    for width in widths:
        # Ajout de 2 pour l'espace de chaque côté du contenu
        if border_type.startswith("single"):
            parts.append("─" * (width + 2))
        else:
            parts.append("═" * (width + 2))
    
    return start + middle.join(parts) + end

def create_separator(width, style="double"):
    """Crée une ligne de séparation"""
    if style == "double":
        return "═" * width
    elif style == "single":
        return "─" * width
    elif style == "dots":
        return "· " * (width // 2)
    elif style == "stars":
        return "✧ " * (width // 2)
    else:
        return "-" * width

def center_text(text, width, fill_char=" "):
    """Centre un texte dans une largeur donnée"""
    return text.center(width, fill_char)

def create_box(text, width=None, style="double"):
    """Crée une boîte décorative autour du texte"""
    if width is None:
        width = len(text) + 4
    
    if style == "double":
        top = "╔" + "═" * (width - 2) + "╗"
        bottom = "╚" + "═" * (width - 2) + "╝"
        return f"{top}\n║{text.center(width-2)}║\n{bottom}"
    else:
        top = "┌" + "─" * (width - 2) + "┐"
        bottom = "└" + "─" * (width - 2) + "┘"
        return f"{top}\n│{text.center(width-2)}│\n{bottom}" 