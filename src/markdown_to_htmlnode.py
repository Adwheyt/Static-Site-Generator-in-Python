from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes
from markdownblocks import BlockType, markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    html_nodes_list = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            # PARAGRAPH
            case BlockType.PARAGRAPH:
                para_split_list = block.split("\n")
                block = " ".join(para_split_list)

                children_list = text_to_children(block)

                if len(children_list) == 0:
                    node = LeafNode("p", block)
                else:
                    node = ParentNode("p", children_list)

                html_nodes_list.append(node)

            # HEADING
            case BlockType.HEADING:
                # You'll need to know the heading tag to use based on the number of #s
                # Then get rid of the #s from the block string
                # Simply run this through text_to_children and follow the usual procedure
                count = 0
                for i in range(6):
                    if block[i] == "#":
                        count += 1

                heading_tag = f"h{count}"

                block = block[count:].strip()

                children_list = text_to_children(block)

                if len(children_list) == 0:
                    node = LeafNode(heading_tag, block)
                else:
                    node = ParentNode(heading_tag, children_list)

                html_nodes_list.append(node)

            # QUOTE
            case BlockType.QUOTE:
                # QUOTE starts with >.
                # imo we should first split on newline. Then join with " ". Then replace >s with ""
                # I'd say now follow the usual procedure
                para_split_list = block.split("\n")
                block = " ".join(para_split_list)
                block = block.replace(">", "")
                block = block.strip()

                children_list = text_to_children(block)

                if len(children_list) == 0:
                    node = LeafNode("blockquote", block)
                else:
                    node = ParentNode("blockquote", children_list)

                html_nodes_list.append(node)

            # ULIST
            case BlockType.ULIST:
                # ULIST starts with - .
                # We'll split on newline.
                para_split_list = block.split("\n")

                # let's go over the list and create nodes
                # these nodes will fall under a ul ParentNode
                # so we'll go over each item (line of text)
                # if the item has inline elements, we'll use text_to_children
                # remember, we need to create a list of nodes (made from items)
                # then assign the list as children to a new parentnode of ul type
                li_list = []

                for item in para_split_list:
                    item = item[2:]
                    children_list = text_to_children(item)

                    if len(children_list) == 0:
                        node = LeafNode("li", item)
                    else:
                        node = ParentNode("li", children_list)
                    
                    li_list.append(node)

                ul_node = ParentNode("ul", li_list)

                html_nodes_list.append(ul_node)

            #OLIST
            case BlockType.OLIST:
                para_split_list = block.split("\n")

                # let's go over the list and create nodes
                # these nodes will fall under a ol ParentNode
                # so we'll go over each item (line of text)
                # if the item has inline elements, we'll use text_to_children
                # remember, we need to create a list of nodes (made from items)
                # then assign the list as children to a new parentnode of ol type
                li_list = []

                for item in para_split_list:
                    item = item[3:]
                    children_list = text_to_children(item)

                    if len(children_list) == 0:
                        node = LeafNode("li", item)
                    else:
                        node = ParentNode("li", children_list)
                    
                    li_list.append(node)

                ul_node = ParentNode("ol", li_list)

                html_nodes_list.append(ul_node)

            #CODE
            case BlockType.CODE:
                lines = block.split("\n")
                content_lines = lines[1:-1]
                block_content = "\n".join(content_lines) + "\n"  # keep trailing newline

                node = ParentNode("pre", [LeafNode("code", block_content)])
                html_nodes_list.append(node)

    daddy_node = ParentNode("div", html_nodes_list)

    return daddy_node


        
    # You'll get a markdown text
    # Split the text into blocks
    # get a list of all HTMLnodes and put the list as children for a ParentNode of div tag
    # you gotta decide whether a node is LeafNode or HTMLNode
    # let the block go through text_to_children function first
    # if children is empty, then make it a LeafNode, else make it a HTMLNode
    # good now append the list of nodes to the daddy_node (div) and return this node


def text_to_children(text):
    # parse the text inside the block
    # create a list of TextNode (inline elements)
    # convert them to LeafNodes
    text_nodes = text_to_textnodes(text)

    leaf_nodes = []

    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))

    return leaf_nodes