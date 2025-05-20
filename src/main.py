import os, shutil
from nodes.utilities import extract_title, generate_page

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    # os.mkdir("public")
    # print (str(os.listdir("static")))
    shutil.copytree("static", "public")

    file = generate_page("content/index.md", "template.html", "")
    print (file)


main()
