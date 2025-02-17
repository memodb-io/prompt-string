from .string import PromptString

TOTAL_ROLES = {"system", "user", "assistant"}
DEFAULT_ROLE_ORDER = ["user", "assistant"]


class PromptChain:
    def __init__(self, prompts: list[PromptString], default_start_role: str = "user"):
        assert all(isinstance(p, PromptString) for p in prompts)
        self.__prompts = prompts
        self.__start_role = default_start_role

    def __len__(self):
        return len(self.__prompts)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__prompts[index]
        elif isinstance(index, slice):
            return PromptChain(
                self.__prompts[index], default_start_role=self.__start_role
            )
        else:
            raise ValueError(f"Invalid index type: {type(index)}")

    @property
    def infer_roles(self):
        if not len(self.__prompts):
            return []
        results = []
        iter_prompts = self.__prompts
        if self.__start_role in ["system", "assistant"]:
            results.append(self.__start_role)
            iter_prompts = iter_prompts[1:]
        for i, p in enumerate(iter_prompts):
            default_role = DEFAULT_ROLE_ORDER[i % len(DEFAULT_ROLE_ORDER)]
            results.append(p.role or default_role)
        return results

    @property
    def roles(self):
        return [p.role for p in self.__prompts]

    @property
    def prompts(self):
        return self.__prompts

    def __truediv__(self, other):
        if isinstance(other, PromptChain):
            return PromptChain(
                self.prompts + other.prompts, default_start_role=self.__start_role
            )
        elif isinstance(other, PromptString):
            return PromptChain(
                self.prompts + [other], default_start_role=self.__start_role
            )
        else:
            raise ValueError(f"Invalid type for PromptChain Division: {type(other)}")

    def messages(self, style="openai"):
        if style == "openai":
            ms = [p.message() for p in self.__prompts]
            roles = self.infer_roles
            for i in range(len(ms)):
                ms[i]["role"] = roles[i]
            return ms
        else:
            raise ValueError(f"Invalid style: {style}")

    def __str__(self):
        return str(self.messages())
