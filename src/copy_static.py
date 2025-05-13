import os
import shutil
from markdown_to_HTML import markdown_to_HTML
from markdown_blocks import markdown_to_blocks, block_to_block_type


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("# ")
    raise Exception("No valid h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generation page from {from_path} to {dest_path} using {template_path}")
    markdown = get_file_content(from_path)
    template = get_file_content(template_path)
    HTML = markdown_to_HTML(markdown).to_html()
    title = extract_title(markdown)
    full_HTML = template.replace("{{ Title }}", title).replace("{{ Content }}", HTML)
    if  not os.path.lexists(os.path.dirname(dest_path)):
        os.makedirs(dest_path)
    with open(dest_path, mode="w") as file:
        file.write(full_HTML)

def get_file_content(file_path):
    with open(file_path) as file:
        book = file.read()
        return book
