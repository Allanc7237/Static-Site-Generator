from split_nodes_delimiter import split_nodes_delimiter, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType

def text_to_textnodes(text):
    split_bold = split_nodes_delimiter([TextNode(text,TextType.TEXT)],"**",TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold,"_",TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic,"`",TextType.CODE)
    split_image = split_nodes_image(split_code)
    split_link = split_nodes_link(split_image)
    return split_link

