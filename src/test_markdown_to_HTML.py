import unittest
from markdown_to_HTML import markdown_to_HTML

class test_markdown_to_HTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_HTML(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_HTML(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_bigger_paragraphs(self):
        self.maxDiff = None
        md = """
This is a **bold** test with _multiple_ failure points
But I will still write it just because it'll **BREAK**
I have spent _way_ too much time on this
Therefor I will test it too **hell and back**

1. I'm getting real tiered
2. things keep being weird
3. Is there a wrong way to write code?
4. I doubt there is a wrong way to write.

- But who knows
- Probably some gate keeper
- or someone that loves to optimise
- but if the code runs it's fine right?

I do really hope it's fine

> If it looks dumb but works it ain't dumb
> That's life!

```
Code blocks feel wierd
So special little creature
```

"""

        
        self.assertEqual(
            """<div><p>This is a <b>bold</b> test with <i>multiple</i> failure points But I will still write it just because it'll <b>BREAK</b> I have spent <i>way</i> too much time on this Therefor I will test it too <b>hell and back</b></p><ol><li>I'm getting real tiered</li><li>things keep being weird</li><li>Is there a wrong way to write code?</li><li>I doubt there is a wrong way to write.</li></ol><ul><li>But who knows</li><li>Probably some gate keeper</li><li>or someone that loves to optimise</li><li>but if the code runs it's fine right?</li></ul><p>I do really hope it's fine</p><blockquote>If it looks dumb but works it ain't dumb That's life!</blockquote><pre><code>Code blocks feel wierd
So special little creature
</code></pre></div>""",
            markdown_to_HTML(md).to_html()
        )

    def test_headings(self):
        self.maxDiff = None
        md = """
# this is an h1

this is paragraph text

## this is an h2

### this is an h3

#### this is an h4

##### this is an h5

###### this is an h6
"""

        node = markdown_to_HTML(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2><h3>this is an h3</h3><h4>this is an h4</h4><h5>this is an h5</h5><h6>this is an h6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_HTML(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_extra_empty(self):
        md = """


This is a paragraph



# This is a header



**Bold**



"""

        self.assertEqual(
            "<div><p>This is a paragraph</p><h1>This is a header</h1><p><b>Bold</b></p></div>",
            markdown_to_HTML(md).to_html()
        )
