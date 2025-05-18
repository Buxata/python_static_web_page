import os, shutil

def main():
    if os.path.exists("public"):
        print ("yes this exists")
        shutil.rmtree("public")

    os.mkdir("public")
    print (str(os.listdir("static")))
    for member in os.listdir("static"):
        shutil.copy(f"static/{member}", "public")
main()
