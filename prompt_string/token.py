from tiktoken import encoding_for_model


USE_ENCODER = None


def get_encoded_tokens(content: str) -> list[int]:
    return USE_ENCODER.encode(content)


def get_decoded_tokens(tokens: list[int]) -> str:
    return USE_ENCODER.decode(tokens)


def setup_encoder(model: str = "gpt-4o"):
    global USE_ENCODER
    USE_ENCODER = encoding_for_model(model)


setup_encoder()
