from typing import Optional, Literal
from functools import wraps
from . import token


def to_prompt_string(func):
    @wraps(func)
    def wrapper(self: "PromptString", *args, **kwargs):
        result = func(self, *args, **kwargs)
        return PromptString(result, **self._meta_info)

    return wrapper


class PromptString(str):

    def __new__(
        cls,
        *args,
        role: Optional[Literal["system", "user", "assistant"]] = None,
        **kwargs,
    ):
        instance = str.__new__(cls, *args, **kwargs)
        instance.__prompt_string_tokens = token.get_encoded_tokens(instance)
        instance.__prompt_string_role = role
        instance.__prompt_string_kwargs = {
            "role": role,
        }
        return instance

    @property
    def role(self):
        return self.__prompt_string_role

    @property
    def _meta_info(self):
        return self.__prompt_string_kwargs

    @role.setter
    def role(self, value):
        self.__prompt_string_role = value

    def __len__(self):
        return len(self.__prompt_string_tokens)
        # return len(token.get_encoded_tokens(super().__str__()))

    @to_prompt_string
    def __getitem__(self, index):
        if isinstance(index, slice):
            return token.get_decoded_tokens(self.__prompt_string_tokens[index])
        elif isinstance(index, int):
            return token.get_decoded_tokens([self.__prompt_string_tokens[index]])
        else:
            raise ValueError(f"Invalid index type: {type(index)}")

    def message(self, style="openai"):
        if style == "openai":
            return {
                "role": self.role,
                "content": super().__str__(),
            }
        else:
            raise ValueError(f"Invalid style: {style}")

    def __add__(self, other):
        if isinstance(other, PromptString):
            return PromptString(super().__add__(other), **other._meta_info)
        elif isinstance(other, str):
            return PromptString(super().__add__(other), **self._meta_info)
        else:
            raise ValueError(f"Invalid type for Prompt Concatenation: {type(other)}")

    def __truediv__(self, other):
        from .string_chain import PromptChain

        assert isinstance(other, PromptString)
        return PromptChain([self, other])

    @to_prompt_string
    def replace(self, old, new, count=-1):
        return super().replace(old, new, count)

    @to_prompt_string
    def format(self, *args, **kwargs):
        return super().format(*args, **kwargs)
