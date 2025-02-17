from prompt_string import P
from prompt_string.string_chain import PromptChain


def test_basic_role():
    sp = P("you're a helpful assistant.", role="system")

    assert sp.role == "system"

    sp.role = "user"
    assert sp.role == "user"


def test_basic_print():
    p = P("you're a helpful assistant.", role="user")
    print(p)

    p2 = P("you're a helpful assistant.", role="assistant")
    assert len(p) == len(p2) == 5
    for i in range(len(p)):
        assert p[i] == p2[i]

    assert p.message() == {
        "role": "user",
        "content": "you're a helpful assistant.",
    }
    p3 = p + p2
    assert p3.message() == {
        "role": "assistant",
        "content": "you're a helpful assistant.you're a helpful assistant.",
    }

    p += p
    print(p, p.role)


def test_basic_chain():
    p = P("you're a helpful assistant.")
    p2 = P("you're a helpful assistant.")
    pc = p / p2 / p
    assert pc.roles == [None, None, None]
    assert len(pc) == 3
    assert pc.infer_roles == ["user", "assistant", "user"]
    assert pc[2] is p


def test_basic_str_methods():
    p = P("you're a helpful assistant. {temp}")
    print(p)
    p1 = p.format(temp="123")
    p2 = p.replace("{temp}", "")
    assert isinstance(p1, P)
    assert isinstance(p2, P)
    assert str(p1) == "you're a helpful assistant. 123"
    assert str(p2) == "you're a helpful assistant. "
