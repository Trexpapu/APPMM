import os
import re

emoji_map = {
    '📅': '<i class="fa-regular fa-calendar"></i>',
    '🔭': '<i class="fa-solid fa-eye"></i>',
    '📋': '<i class="fa-solid fa-clipboard-list"></i>',
    '🔍': '<i class="fa-solid fa-magnifying-glass"></i>',
    '🗑️': '<i class="fa-solid fa-trash"></i>',
    '👁️': '<i class="fa-solid fa-eye"></i>',
    '✏️': '<i class="fa-solid fa-pen"></i>',
    '👤': '<i class="fa-solid fa-user"></i>',
    '📧': '<i class="fa-solid fa-envelope"></i>',
    '📞': '<i class="fa-solid fa-phone"></i>',
    '🏠': '<i class="fa-solid fa-house"></i>',
    '⚡': '<i class="fa-solid fa-bolt"></i>',
    '📊': '<i class="fa-solid fa-chart-bar"></i>',
    '📝': '<i class="fa-solid fa-file-pen"></i>',
    '❌': '<i class="fa-solid fa-xmark"></i>',
    '💾': '<i class="fa-solid fa-floppy-disk"></i>',
    '🐾': '<i class="fa-solid fa-paw"></i>',
    '🩺': '<i class="fa-solid fa-stethoscope"></i>',
    '💉': '<i class="fa-solid fa-syringe"></i>',
    '🐶': '<i class="fa-solid fa-dog"></i>',
    '🐱': '<i class="fa-solid fa-cat"></i>',
    '🛏️': '<i class="fa-solid fa-bed"></i>',
    '✂️': '<i class="fa-solid fa-scissors"></i>',
    '✅': '<i class="fa-solid fa-check"></i>',
    '⚠️': '<i class="fa-solid fa-triangle-exclamation"></i>',
    '💡': '<i class="fa-solid fa-lightbulb"></i>',
    'ℹ️': '<i class="fa-solid fa-circle-info"></i>',
    '📄': '<i class="fa-solid fa-file"></i>',
    '📷': '<i class="fa-solid fa-camera"></i>',
    '➕': '<i class="fa-solid fa-plus"></i>'
}

def replace_emojis_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for emoji, icon in emoji_map.items():
        if emoji in content:
            content = content.replace(emoji, icon)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    templates_dir = r"c:\Users\emman\Desktop\Mascotas Morelia\APPSMascotasMorelia\templates"
    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".html"):
                replace_emojis_in_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
