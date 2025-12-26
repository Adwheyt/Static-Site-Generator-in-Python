import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode):
        return self.text == textnode.text and self.text_type == textnode.text_type and self.url == textnode.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        
def text_node_to_html_node(text_node):
    if text_node.text_type is None:
        raise Exception("Invalid text node")
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    
#-----------------------------------------------------------------------------------------------------------------------------------------------
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            if old_node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid markdown: incorrect delimiter pair")
            else:
                temp_list = old_node.text.split(delimiter)

                for i in range(len(temp_list)):
                    if temp_list[i] == "":
                        continue
                    elif i % 2 == 0:
                        new_nodes.append(TextNode(temp_list[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(temp_list[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:    
            image_list = extract_markdown_images(old_node.text)
            if len(image_list) == 0 and old_node.text != "":
                new_nodes.append(old_node)
            else:
                current_text = old_node.text
                for alt_text, image_link in image_list:
                    temp_list = current_text.split(f'![{alt_text}]({image_link})', 1)
                    if len(temp_list[0]) != 0:
                        new_nodes.append(TextNode(temp_list[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_link))

                    current_text = temp_list[1]
                    
                if len(current_text) != 0:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:    
            link_list = extract_markdown_links(old_node.text)
            if len(link_list) == 0 and old_node.text != "":
                new_nodes.append(old_node)
            else:
                current_text = old_node.text
                for alt_text, link in link_list:
                    temp_list = current_text.split(f'[{alt_text}]({link})', 1)
                    if len(temp_list[0]) != 0:
                        new_nodes.append(TextNode(temp_list[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, link))

                    current_text = temp_list[1]
                    
                if len(current_text) != 0:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes