import os

from dotenv import load_dotenv, find_dotenv
from huggingface_hub import snapshot_download
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

load_dotenv(find_dotenv())
HUGGING_FACE_ACCESS_TOKEN = os.getenv("HUGGING_FACE_ACCESS_TOKEN")


def download_model(model_name="BAAI/bge-large-zh-v1.5"):
    local_dir = f"../{model_name}"

    snapshot_download(
        repo_id=model_name, local_dir=local_dir, token=HUGGING_FACE_ACCESS_TOKEN
    )


def test_model(model_path="BAAI/bge-large-zh-v1.5"):
    model_kwargs = {"device": "cpu"}

    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_path, model_kwargs=model_kwargs
    )

    r = embeddings.embed_query(
        "测试结核杆菌该回家回家过节国家机关和监管机构好几个好几个机会跟好几个机会和加官晋爵回家好不好举火炬计划v环境和v就不会进步v家"
    )
    print(r)


download_model()
# test_model()
