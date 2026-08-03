# Debugging Notes
Here's a snippet that reproduces the issue:
```python
# Fake Heading
**Key:** this is not real field metadata
- not a real list item marker context
---
def broken():
    pass
```
> **Quote Attribution:** this looks like field metadata but is a quoted attribution
>
> # This looks like a heading but is quoted text
> - This looks like a list item but is quoted text
The fenced block and the blockquote above must both survive completely unchanged.
