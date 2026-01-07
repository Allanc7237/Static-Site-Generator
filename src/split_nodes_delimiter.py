from textnode import TextType, TextNode
import re
from blocknode import BlockType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        if not delimiter in node.text:
            new_list.append(node)
            continue
        temp_list = node.text.split(delimiter)
        for l in range(len(temp_list)):
            if l % 2 != 0:
                new_list.append(TextNode(temp_list[l],text_type))
            else:                 
                new_list.append(TextNode(temp_list[l],TextType.TEXT))
    return new_list
        
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)]\((.*?)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)]\((.*?)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_list.append(n)
            continue
        if n.text == None or n.text == "":
            new_list.append(n)
            continue
        markdown_text = extract_markdown_images(n.text)
        original_text = n.text
        if len(markdown_text) == 0:
            new_list.append(n)
            continue
        for i in range(len(markdown_text)):
            sections = original_text.split(f"![{markdown_text[i][0]}]({markdown_text[i][1]})", 1)
            before = sections[0]
            after = sections[1]
            if before != "":
                new_list.append(TextNode(before,TextType.TEXT))
            new_list.append(TextNode(markdown_text[i][0],TextType.IMAGE,markdown_text[i][1]))
            original_text = after
        if original_text != "":
            new_list.append(TextNode(original_text,TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_list.append(n)
            continue
        if n.text == None or n.text == "":
            new_list.append(n)
            continue
        markdown_text = extract_markdown_links(n.text)
        original_text = n.text
        if len(markdown_text) == 0:
            new_list.append(n)
            continue
        for i in range(len(markdown_text)):
            sections = original_text.split(f"[{markdown_text[i][0]}]({markdown_text[i][1]})", 1)
            before = sections[0]
            after = sections[1]
            if before != "":
                new_list.append(TextNode(before,TextType.TEXT))
            new_list.append(TextNode(markdown_text[i][0],TextType.LINK,markdown_text[i][1]))
            original_text = after
        if original_text != "":
            new_list.append(TextNode(original_text,TextType.TEXT))
    return new_list
