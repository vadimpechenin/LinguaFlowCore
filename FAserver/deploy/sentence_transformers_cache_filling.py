from sentence_transformers import SentenceTransformer
from pathlib import Path


def main():
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    cache_folder = str(Path(__file__).resolve().parent.parent
                       .joinpath("tests").joinpath("resources").joinpath("sentence_transformers_cache").resolve())

    model = SentenceTransformer(model_name)
    model.save(cache_folder)


if __name__ == "__main__":
    main()
