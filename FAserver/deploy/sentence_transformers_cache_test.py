from sentence_transformers import SentenceTransformer
from pathlib import Path
import os


def main():
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    cache_folder = str(Path(__file__).resolve().parent.parent
                       .joinpath("tests").joinpath("resources").joinpath("sentence_transformers_cache").resolve())
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ['SENTENCE_TRANSFORMERS_HOME'] = cache_folder

    model = SentenceTransformer(model_name)


if __name__ == "__main__":
    main()
