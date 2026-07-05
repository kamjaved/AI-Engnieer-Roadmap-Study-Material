from practice.tokenizer_explorer.tokenizers import tokenize

type MultiLangDict = dict[str, dict[str, str]]


MULTILINGUAL_SAMPLES: MultiLangDict = {
    "greeting": {
        "en": "Hello, how are you?",
        "ja": "こんにちは、お元気ですか？",
        "ar": "مرحبا، كيف حالك؟",
        "ko": "안녕하세요, 어떻게 지내세요?",
        "zh": "你好，你怎么样？",
        "de": "Hallo, wie geht es Ihnen?",
        "hi": "नमस्ते, आप कैसे हैं?",
        "ru": "Здравствуйте, как дела?",
    },
    "code": {
        "python": "def hello():\n    return 'world'",
        "javascript": "const hello = () => 'world';",
        "sql": "SELECT name FROM users WHERE active = true;",
    },
}


def explore_multilingual(samples: MultiLangDict, model: str = "gpt-4o") -> None:
    """
    For each concept in the sample dictionary, tokenize every language/variant
    and print the token count, ratio vs English baseline, and raw token IDs.
    """

    for concept, variants in samples.items():
        print(f"\n{'=' * 60}")
        print(f"CONCEPT: {concept.upper()}")
        print(f"{'=' * 60}")

        # Get English (or first key) as baseline
        baseline_key = "en" if "en" in variants else next(iter(variants))
        baseline = tokenize(variants[baseline_key], model)
        print(f"[baseline: {baseline_key}], [baseline_count: {baseline.token_count}]")

        for lang, text in variants.items():
            result = tokenize(text, model)
            ratio = result.token_count / baseline.token_count
            print(
                f"  {lang:>12}  |  tokens: {result.token_count:>3}  |  ratio: {ratio:.2f}x  |  {text[:40]}"
            )
            print(
                f"              |  IDs: {result.token_ids[:8]}{'...' if len(result.token_ids) > 8 else ''}"
            )


result2 = explore_multilingual(MULTILINGUAL_SAMPLES)
print(result2)
