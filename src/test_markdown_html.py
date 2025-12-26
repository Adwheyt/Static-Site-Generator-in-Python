import unittest
from markdown_to_htmlnode import markdown_to_html_node

class TestMarkdownFulltohtml(unittest.TestCase):
    def test_paragraph_block_basic(self):
        md = """
This is a simple paragraph
split over
multiple lines

Another paragraph here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><p>This is a simple paragraph split over multiple lines</p><p>Another paragraph here</p></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = "### New Heading"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>New Heading</h3></div>")

    def test_quote(self):
        md = """
>This is a quote.
>I've more to write.
>nvm
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><blockquote>This is a quote. I've more to write. nvm</blockquote></div>")
        
    def test_ulist(self):
        md = """
Paragraph here

- **element1**
- element2
- element3"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><p>Paragraph here</p><ul><li><b>element1</b></li><li>element2</li><li>element3</li></ul></div>")

    def test_olist(self):
        md = """
1. element1
2. element 2
3. element3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><ol><li>element1</li><li>element 2</li><li>element3</li></ol></div>")
        
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_block_quote_2(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><blockquote>\"I am in fact a Hobbit in all but size.\"   -- J.R.R. Tolkien</blockquote></div>")

if __name__ == "__main__":
    unittest.main()