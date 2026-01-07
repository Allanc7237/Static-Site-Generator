from textnode import TextNode, TextType
from enum import Enum
from blocknode import block_to_block_type, markdown_to_blocks, BlockType
from inline_markdown import text_to_textnodes

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None or self.props == {}:
                return ""
        new_string = ""
        for p in self.props:
             new_string += f" {p}={self.props[p]}"
        return new_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
          super().__init__(tag,value,None,props)


    def to_html(self):
        if self.value == None:
            raise ValueError("missing value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
          super().__init__(tag,None,children,props)
        

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None:
            raise ValueError("missing children")
        html_string = f"<{self.tag}>"
        for c in self.children: 
            html_string += c.to_html()
        html_string += f"</{self.tag}>"
        return html_string

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Cannot be 'None' type")

def paragraph_to_html_node(block):
    lines = block.split()
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p",children,None)

def heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    lines = block.split("\n")
    if len(lines) <= 1 or not lines[0].lstrip().startswith("```") or not lines[-1].lstrip().startswith("```"):
        raise ValueError("invalid code block")
    inner_lines = lines[1:-1]
    text = "\n".join(inner_lines)
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    lines = block.split("\n")
    ol_children = []
    for l in lines:
        text = l.split(". ",1)
        children = text_to_children(text[1])
        ol_children.append(ParentNode("li", children))
    return ParentNode("ol", ol_children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    li_children = []
    for l in lines:
        text = l[2:].lstrip()
        children = text_to_children(text)
        li_children.append(ParentNode("li", children))
    return ParentNode("ul",li_children)
    
def quote_to_html_node(block):
    lines = block.split("\n")
    clean_lines = []
    for l in lines:
        if not l.startswith(">"):
            raise Exception("invalid quote block")
        clean_lines.append(l[1:].lstrip())
    text = " ".join(clean_lines)
    children = text_to_children(text)
    return ParentNode("blockquote",children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for b in blocks:
        html_node = block_to_html_node(b)
        children.append(html_node)
    return ParentNode("div", children)

