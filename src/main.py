import os, shutil, sys
from nodes.utilities import generate_pages_recursive
from email.mime import base

def main():

    basepath = '/'
    if sys.argv[1] and sys.argv[1]!= "src/main.py":
        basepath = sys.argv[1]

    if os.path.exists("public"):
        shutil.rmtree("public")

    # os.mkdir("public")
    # print (str(os.listdir("static")))
    shutil.copytree("static", "public")

    pages = generate_pages_recursive("content", "template.html", "docs", basepath)
    if pages:
        print(f"There are pages {True}")



main()
