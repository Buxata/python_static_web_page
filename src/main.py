import os, shutil
from nodes.utilities import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    # os.mkdir("public")
    # print (str(os.listdir("static")))
    shutil.copytree("static", "public")

    pages = generate_pages_recursive("content", "template.html", "public")
    if pages:
        print(f"There are pages {True}")



main()
