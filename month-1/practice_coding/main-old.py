from practice.tokenizer_explorer.tokenizers import tokenize
from practice.tokenizer_explorer.multilingual import explore_multilingual, MULTILINGUAL_SAMPLES

# def main():
#     print("Hello from python-assignments!")


if __name__ == "__main__":
    print("\n--- PART 2: Tokenizer Wrapper Sanity Check ---")
    result = tokenize("Hello, how are you?", "gpt-4")
    print(f"Model: {result.model_name} | Tokens: {result.token_count}")
    print(f"IDs:     {result.token_ids}")
    print(f"Strings: {result.tokens}")

    print("\n--- PART 3: Multilingual Token Exploration ---")
    explore_multilingual(MULTILINGUAL_SAMPLES)

    # print("\n--- PART 4: Cosine Similarity Exploration ---")
    # explore_similarity(SIMILARITY_SAMPLES)
