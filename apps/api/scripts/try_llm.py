import sys

from openai import OpenAI

from app.core.config import settings


def main() -> None:
    api_key = settings.llm_api_key.get_secret_value()
    if not api_key:
        sys.exit("LLM_API_KEY is not set in apps/api/.env")

    client = OpenAI(api_key=api_key, base_url=settings.llm_base_url)
    response = client.chat.completions.create(
        model=settings.llm_model,
        max_tokens=400,
        messages=[
            {"role": "system", "content": "You are a prompt-engineering coach. Be brief."},
            {
                "role": "user",
                "content": "Give me two tips to improve this prompt: 'write a blog'",
            },
        ],
    )

    print(response.choices[0].message.content)
    if response.usage:
        print(
            f"\ntokens in: {response.usage.prompt_tokens}, "
            f"tokens out: {response.usage.completion_tokens}"
        )


if __name__ == "__main__":
    main()
