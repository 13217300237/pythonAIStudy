from langchain_community.embeddings import HuggingFaceBgeEmbeddings

def test_model(model_path="BAAI/bge-large-zh-v1.5"):
    model_kwargs = {"device": "cpu"}

    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_path, model_kwargs=model_kwargs
    )

    r = embeddings.embed_query(
        "测试结核杆菌该回家回家过节国家机关和监管机构好几个好几个机会跟好几个机会和加官晋爵回家好不好举火炬计划v环境和v就不会进步v家"
    )
    print(r)
    
test_model()