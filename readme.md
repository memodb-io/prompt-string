<div align="center">
  <h1><code>prompt-string</code></h1>
  <p><strong>Treat prompt as a data type in Python</strong></p>
  <p>
    <img src="https://img.shields.io/badge/python->=3.11-blue">
    <a href="https://pypi.org/project/prompt-string/">
      <img src="https://img.shields.io/pypi/v/prompt-string.svg">
    </a>
</div>



Prompt is essentially a string, but it should behave somewhat differently from a standard string:

📏 **Length & Slicing**: A prompt string should consider the length in terms of tokens, not characters, and slicing should be done accordingly.

👨 **Role & Concatenation**: Prompt strings should have designated roles (e.g., `system`, `user`, `assistant`) and should be concatenated in a specific manner.

🦆 **Binding Functions**: A prompt string contains logic and instructions, so having some binding functions for AI-related stuff is beneficial and necessary (e.g.,  convert to OpenAI Message Format).



**Few promises in `prompt-string`:**

- `prompt-string` inherits from `string`. Therefore, aside from the mentioned features, its other behaviors are just like those of a `string` in Python.
- `prompt-string` won't add OpenAI and other AI SDKs as dependencies; it is simply a toolkit for prompts.
- `prompt-string` will be super light and fast, with no heavy processes running behind the scenes.



## Install

```bash
pip install prompt-string
```



## Quick Start

#### Length & Slicing 

```python
from prompt_string import P

prompt = P("you're a helpful assistant.")

print("Total token size", len(prompt))
print("Decoded result of the second token", prompt[2])
print("The decoded result of first five tokens", prompt[:5])
```



#### Role & Concatenation

```python
from prompt_string import P

sp = P("you're a helpful assistant.", "system")
up = P("How are you?", "user")

print(sp.role, up.role, (sp+up).role)
print(sp + up)
```

- role can be `None`, `str`, `list[str]`
- For single prompt, like `sp`, the role is `str`(*e.g.* `system`) or `None`
- For concatenated prompts, like `sp+up`, the role is `list[str]`(*e.g.* `['system', 'user']`)



#### Binding Functions

```python
from prompt_string import P

sp = P("you're a helpful assistant.")
up = P("How are you?")

print((sp+up).messages())
```

- `messages` will return the OpenAI-Compatible messages format, where you can directly pass it to `client.chat.completions.create(messages=...)`
