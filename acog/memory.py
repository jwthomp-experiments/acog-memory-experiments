from qdrant_client import QdrantClient
from qdrant_client import models
from uuid import uuid4
from sentence_transformers import SentenceTransformer

__all__ = ["initialize", "store", "search"]

QDRANT_CLIENT = None
SENTENCE_MODEL = None


def initialize():
    global QDRANT_CLIENT
    global SENTENCE_MODEL


    # Connect to Qdrant
    QDRANT_CLIENT = QdrantClient(host='localhost', port=6333)
    if does_collection_exist("sentences") is False:
        QDRANT_CLIENT.recreate_collection(
            collection_name='sentences',
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
        )
    
    SENTENCE_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def store(text):
    embeddings = get_sentence_embeddings([text])
    store_embeddings(embeddings, [text])

def search(text):
    embeddings = get_sentence_embeddings([text])
    search_result = QDRANT_CLIENT.search(
        collection_name="sentences",
        query_vector = embeddings[0],
        query_filter = None,
        limit = 5
    )
    return [hit.payload for hit in search_result]

########################################################
# Internal Methods
########################################################

def does_collection_exist(collection_name):
    collections = QDRANT_CLIENT.get_collections()
    print(f"Collections: {collections.collections}")
    for collection in collections.collections:
        print(f"Collection: {collection}")
        if collection.name == collection_name:
            return True
    return False


def get_sentence_embeddings(input):
    embeddings = SENTENCE_MODEL.encode(input)
    #print(embeddings)
    #print(f"Length: {len(embeddings)}")

    return embeddings

def store_embeddings(embeddings, inputs):
    print(f" len emb: {len(embeddings)} len inputs: {len(inputs)}")
    QDRANT_CLIENT.upsert(
        collection_name = 'sentences',
        points = [
            models.PointStruct(
                id = str(uuid4()),
                vector = vector.tolist(),
                payload = {
                    "message": inputs[idx]
                }
            )
            for idx, vector in enumerate(embeddings)
        ]
    )
