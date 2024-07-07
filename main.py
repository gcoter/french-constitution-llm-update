import re
import json

from tqdm import tqdm
from fire import Fire
from dotenv import load_dotenv
from openai import OpenAI


client = OpenAI()


def read_constitution(path):
    print(f"Read constitution from '{path}'")
    with open(path, 'r') as f:
        constitution_text = f.read()
    return constitution_text


def call_llm_json(messages, model="gpt-4o"):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)


def update_one_article(article_text: str) -> str:
    prompt = f"""Tu es un expert en science politique et en particulier de la constitution française. Voici ci-dessous un article de la constitution. Tu as pour tâche de suggérer des mises à jour visant à améliorer les institutions. Pour cela, commence par établir un raisonnement dans la section 'reasoning' de ta réponse puis propose une version réécrite de l'article dans la section 'updated_article' de ta réponse (essaie de respecter la mise en page d'origine).

Formule ta réponse comme un JSON avec la structure suivante :

json
{{
    'reasoning': "...",
    'updated_article': "..."
}}

===== ARTICLE =====

{article_text}"""

    output_json = call_llm_json(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    output_text = f"""{output_json['updated_article']}

<details>

<summary>Raisonnement</summary>

{output_json['reasoning']}

</details>"""
    
    return output_text


def rewrite_constitution(constitution_text: str, output_file_path: str) -> str:
    print("Start rewriting the constitution")
    rewritten_constitution = ""
    chunks = re.split("(#+)", constitution_text)
    buffer = ""
    for chunk in tqdm(chunks):
        if chunk.strip() == "":
            continue
        if re.match("#+", chunk):
            buffer += chunk
            continue
        if len(chunk) < 50:  # Title
            buffer += chunk
            continue
        rewritten_constitution += buffer + " " + update_one_article(article_text=chunk) + "\n\n"
        buffer = ""
        save_constitution(rewritten_constitution, path=output_file_path)
    return rewritten_constitution


def save_constitution(constitution_text: str, path: str):
    print(f"Write constitution to '{path}'")

    constitution_text = constitution_text.replace("# \n", "# ")
    constitution_text = constitution_text.replace("  ", " ")
    constitution_text = constitution_text.replace("\n\n\n", "\n\n")

    with open(path, "w") as f:
        f.write(constitution_text)


def main(input_file_path: str, output_file_path: str):
    load_dotenv()
    constitution_text = read_constitution(path=input_file_path)
    rewrite_constitution(constitution_text, output_file_path=output_file_path)


if __name__ == "__main__":
    Fire(main)
