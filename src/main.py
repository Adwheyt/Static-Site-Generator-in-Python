from textnode import TextNode, TextType
import shutil, os
from markdown_to_htmlnode import markdown_to_html_node

def copy_contents(src, dest):

    #list out the contents of static directory
    content_list = os.listdir(src)

    # copy all files at root of static
    for item in content_list:
        if os.path.isfile(os.path.join(src,item)):
            shutil.copy(os.path.join(src, item), dest)
        else:
            # when you encouter a directory:
            # first make directory at the dest location
            os.mkdir(os.path.join(dest, item))
            # then copy its contents
            copy_contents(os.path.join(src, item), os.path.join(dest, item))

def extract_title(markdown):
    markdown_list = markdown.split("\n")
    for line in markdown_list:
        if line.startswith("# "):
            return line[2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown = file.read()

        with open(template_path, "r") as file2:
            template = file2.read()
            html = markdown_to_html_node(markdown).to_html()

            final = template.replace("{{ Title }}", extract_title(markdown))
            final = final.replace("{{ Content }}", html)

            with open(dest_path, "w") as file3:
                file3.write(final)
            
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # list out the contents of content directory
    content_list = os.listdir(dir_path_content)

    # convert any markdwon files in the current directory
    for item in content_list:
        if os.path.isfile(os.path.join(dir_path_content, item)):
            generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item[:-2]+"html"))
        else:
            os.mkdir(os.path.join(dest_dir_path, item))
            generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))

def main():
    src = "static"
    dest = "public"

    #delete and recreate public directory
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    os.mkdir(dest)

    copy_contents(src, dest)
    generate_pages_recursive("content", "template.html", "public")

main()