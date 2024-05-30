from pathlib import Path
from typing import Sequence, Optional

from langchain_core.documents import Document

from .embeddings import build_embeddings_provider
from .vectordb_reader import VectorDBReader


def format_documents(docs: Sequence[Document]) -> str:
    """
    Formats document objects to make pass them into a prompt
    :param docs: Documents to format
    :return: a string with the formated documents
    """
    out_docs = "\n".join(doc.page_content for doc in docs)
    return out_docs


def build_retriever(vector_store: str,
                    top_k: int = 4,
                    collection_name: str = "langchain",
                    embeddings_engine: str = "GPT4All",
                    embeddings_model: Optional[str] = None):
    """ Factory function for creating a retriever instance to be used in a chain
        :param embeddings_model: Name of the transformer encoder user to generate sentence embeddings
        :param embeddings_engine: Name of the provider: GPT4All, HuggingFace or OpenAI
        :param vector_store: Path or connection string to the vector database provider. If a path is provided,
            it will be opened as a ChromaDB.
        :param top_k: Number of documents to retrieve. Default is 4.
        :param collection_name: Defaults to "langchain"
    """

    # Create the embeddings provider
    embeddings = build_embeddings_provider(embeddings_engine, embeddings_model)
    # For now, we only support ChromaDB based vector dbs
    if Path(vector_store).is_dir():
        # Use our Chroma wrapper
        vectorstore = VectorDBReader(db_path=vector_store,
                                     top_k=top_k,
                                     collection_name=collection_name,
                                     embeddings=embeddings)

        return vectorstore.as_retriever()
    else:
        raise NotImplementedError(f"Vector store {vector_store} provider is not supported")
