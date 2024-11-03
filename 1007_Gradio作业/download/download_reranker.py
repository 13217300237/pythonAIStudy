import os

from dotenv import load_dotenv, find_dotenv
from huggingface_hub import snapshot_download
from sentence_transformers import CrossEncoder


load_dotenv(find_dotenv())
# huggingface token
HUGGING_FACE_ACCESS_TOKEN = os.getenv("HUGGING_FACE_ACCESS_TOKEN")


# https://huggingface.co/BAAI/bge-reranker-large
def download_model(model_name="BAAI/bge-reranker-large"):
    local_dir = f"../{model_name}"

    snapshot_download(
        repo_id=model_name, local_dir=local_dir, token=HUGGING_FACE_ACCESS_TOKEN
    )


def test_model(model_patch="../BAAI/bge-reranker-large"):
    model = CrossEncoder(model_patch, device="cpu")

    pairs = [["孙悟空是谁", "孙悟空是你大爷"], ["孙悟空是谁", "孙悟空是唐僧徒弟"]]
    r = model.predict(pairs)
    print(r)


# download_model()
test_model()
