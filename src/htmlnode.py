class HTMLNode:
    def __init__(self = None, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        htmlAttr = ""

        for attr in self.props:
            htmlAttr += f' {attr}="{self.props[attr]}"'
        
        return htmlAttr
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        result = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"

        return result
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children:{self.children}, {self.porps})"