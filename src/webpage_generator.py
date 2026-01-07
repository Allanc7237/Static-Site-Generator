from htmlnode import markdown_to_html_node
import os
def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for l in lines:
        if l.startswith("#"):
            title = l.split("#")
            break
    if title == "":
        raise Exception("No Title Header")
    return title[1].lstrip()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_text = open(from_path,"r").read()
    template_text = open(template_path,"r").read()
    from_node = markdown_to_html_node(from_text)
    from_html = from_node.to_html()
    title = extract_title(from_text)
    new_text = template_text.replace("{{ Title }}", title)
    final_text = new_text.replace("{{ Content }}", from_html)
    open(dest_path, "w").write(f"{final_text}\n")

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    os.makedirs(dest_dir_path, exist_ok=True)
    source_contents = os.listdir(dir_path_content)
    src = dir_path_content
    dest = dest_dir_path
    for f in source_contents:
        new_src = os.path.join(src, f)
        if not os.path.isfile(new_src):
            new_dest = os.path.join(dest,f)
            generate_page_recursive(new_src,template_path,new_dest,basepath)
        else:
            new_dest = os.path.join(dest,f)
            temp_dest = os.path.splitext(new_dest)
            final_dest = f"{temp_dest[0]}.html"
            from_text = open(new_src,"r").read()
            template_text = open(template_path,"r").read()
            from_node = markdown_to_html_node(from_text)
            from_html = from_node.to_html()
            title = extract_title(from_text)
            new_text = template_text.replace("{{ Title }}", title)
            final_text = new_text.replace("{{ Content }}", from_html)
            href_text = final_text.replace('href="/', f'href="{basepath}')
            end_text = href_text.replace('src="/', f'src="{basepath}')
            open(final_dest, "w").write(f"{end_text}\n")