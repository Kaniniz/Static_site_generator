import os
import shutil
import sys

from copy_static import copy_files_recursive, generate_pages_recursive

dir_path_public = "./docs"
dir_path_static = "./static"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive("./content", "./template.html", dir_path_public, basepath)

main()
