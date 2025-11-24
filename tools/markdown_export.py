import os

def save_markdown(filename, content, folder="./output"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, f"{filename}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath