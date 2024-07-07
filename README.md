# French Constitution - Update as suggested by LLM

A fun experiment where a LLM (gpt-4o) is used to propose updates to the French Constitution.

**Note:** This is not intented as a serious work!

## Explanations

The original Constitution can be found [here](docs/constitution.md). It was given as an input, article by article, to a LLM (gpt-4o) with instructions to rewrite it (the prompt can be found in `main.py`).

The resulting Constitution can be found [here](docs/new_constitution.md).

The LLM was instructed to provide explanations about its reasoning before actually updating each article. If you want to see it, click on "Raisonnement" under any article to display it.

## Usage / How to reproduce

1. Put your OpenAI API Key in a `.env` file following this format:

```conf
OPENAI_API_KEY=<your key>
```

2. Create a virtual environment and install requirements like this:

```bash
python3 -m venv venv

source venv/bin/activate 

pip install -r requirements.txt
```

3. Run the main script as follows:

```bash
python main.py --input_file_path docs/constitution.md --output_file_path docs/new_constitution.md
```
