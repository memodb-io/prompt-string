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



## Features

`prompt-string` provides two types:

- `P` for prompt, inherits from `string`. Length, Slicing and concatenation are modified and support new attributes like `.role`.
  - `p = P("You're a helpful assistant")`
- `PC` for prompt chain, act like `list[P]`. Link a series of prompt and support `.messages(...)`
  - `pc = p1 / p2 / p3`



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

`P` supports some `str` native methods to still return a `P` object:

- `.format`
- `.replace`

```python
prompt = P("you're a helpful assistant. {temp}")

print(len(prompt.format(temp="End of instructions")))
print(len(prompt.replace("{temp}", ""))
```

> 🧐 Raise an issue if you think other methods should be supported



#### Role

```python
from prompt_string import P

sp = P("you're a helpful assistant.", role="system")
up = P("How are you?", role="user")

print(sp.role, up.role, (sp+up).roles)
print(sp + up)

print(sp.message())
```

- role can be `None`, `str` for `P`
- For single prompt, like `sp`, the role is `str`(*e.g.* `system`) or `None`
- `sp+up` will concatenate two prompt string and generate a new `P`, whose role will be updated if the latter one has one.
  - For example, `sp+up`'s role is `user`, `sp+P('Hi')`'s role is `system`


- `.message(...)` return a JSON object of this prompt.



#### Concatenation

```python
pc = sp / up
print(pc.roles)
print(pc.messages())
```

For concatenated prompts, like `sp / up`, the type will be converted to `PC` (prompt chain), `PC` has below things:

- `.roles`, a list of roles. For example, `(sp|up).roles` is `['system', 'user']`
- `.messages(...)` pack prompts into OpenAI-Compatible messages JSON, where you can directly pass it to `client.chat.completions.create(messages=...)`.
  - `messages` will assume the first role is `user`, then proceed in the order of user-assistant. When a prompt has a role, it will use that role. check `pc.infer_role` for final roles in messages.



## Few promises in `prompt-string`

- `P` inherits from `string`. Therefore, aside from the mentioned features, its other behaviors are just like those of a `string` in Python.
- `prompt-string` won't add OpenAI and other AI SDKs as dependencies; it is simply a toolkit for prompts.
- `prompt-string` will be super light and fast, with no heavy processes running behind the scenes.

