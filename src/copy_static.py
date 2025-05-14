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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generation page from {from_path} to {dest_path} using {template_path}")

    markdown = get_file_content(from_path)
    template = get_file_content(template_path)
    HTML = markdown_to_HTML(markdown).to_html()
    title = extract_title(markdown)
    full_HTML = template.replace("{{ Title }}", title).replace("{{ Content }}", HTML).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    
    if not os.path.lexists(os.path.dirname(dest_path)):
        directory = dest_path.rsplit("/", maxsplit=1)
        os.makedirs(directory[0])
    to_file = open(dest_path, "w")
    to_file.write(full_HTML)

def get_file_content(file_path):
    with open(file_path) as file:
        book = file.read()
        return book

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, "index.html"), basepath)
            continue
        generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), basepath)