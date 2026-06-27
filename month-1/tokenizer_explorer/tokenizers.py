from dataclasses import dataclass

import tiktoken


@dataclass
class TokenResult:
    model_name: str
    tokens: list[str]
    token_ids: list[int]
    token_count: int


def _tokenize_with_tiktoken(text: str, model: str) -> TokenResult:
    enc = tiktoken.encoding_for_model(model)

    token_ids = enc.encode(text)
    tokens = [enc.decode([token_id]) for token_id in token_ids]

    # print(tokens)
    # print(token_ids)
    # print(model)
    # print(len(token_ids))

    return TokenResult(
        model_name=model,
        tokens=tokens,
        token_ids=token_ids,
        token_count=len(token_ids),
    )


encoder = tiktoken.encoding_for_model("gpt-4o")  # GPT-4 tokenizer


def tokenize(text: str, model: str) -> TokenResult:
    model_aliases = {
        "gpt-3": "gpt-3.5-turbo",
    }
    resolved_model = model_aliases.get(model, model)

    if resolved_model in {"gpt-4", "gpt-3.5-turbo", "gpt-4o"}:
        return _tokenize_with_tiktoken(text, resolved_model)

    raise ValueError(f"Unsupported model: {model}")


# result = tokenize("The capital of France is Paris.", "gpt-4")
# print(result)
# print(f"\n{'=' * 60}")

# result2 = tokenize("My Name is Kamran Javed", "gpt-3")
# print(result2)
# print(f"\n{'=' * 60}")

result3 = tokenize("Hello, how are you?", "gpt-4")
print(result3)
print(f"\n{'=' * 60}")

# result4 = tokenize("こんにちは、お元気ですか？", "gpt-4")
# print(result4)
