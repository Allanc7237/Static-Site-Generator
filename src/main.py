from textnode import TextNode, TextType
import os
import shutil
from webpage_generator import generate_page_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    source = "/home/allanc777/workspace/Static-Site-Generator/static"
    destination = "/home/allanc777/workspace/Static-Site-Generator/docs"
    from_text = "/home/allanc777/workspace/Static-Site-Generator/content"
    template_text = "/home/allanc777/workspace/Static-Site-Generator/template.html"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_from_source(source,destination)
    generate_page_recursive(from_text,template_text,destination, basepath)

def copy_from_source(source,destination):
    if not os.path.exists(source):
        raise Exception("Invalid source path")
    if not os.path.exists(destination):
        os.mkdir(destination)
    source_contents = os.listdir(source)
    src = source
    dest = destination
    for f in source_contents:
        new_src = os.path.join(src, f)
        if not os.path.isfile(new_src):
            print(new_src)
            new_dest = os.path.join(dest,f)
            print(new_dest)
            copy_from_source(new_src,new_dest)
        else:
            shutil.copy(new_src,destination)
       
main()   



