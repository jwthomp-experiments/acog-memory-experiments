import signal
import sys
from uuid import uuid4
import torch
#from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client import models

TOKENIZER = None
MODEL = None
SENTENCE_MODEL = None
QDRANT_CLIENT = None

def sigint_handler(signal, frame):
    print("\nBye now!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def initialize():
    global TOKENIZER
    global MODEL
    global SENTENCE_MODEL
    global QDRANT_CLIENT

    SENTENCE_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    ##TOKENIZER = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-6B")
    #MODEL = AutoModelForCausalLM.from_pretrained(
    #    "PygmalionAI/pygmalion-6B", 
    #    torch_dtype=torch.float16, 
    #    load_in_8bit=True, 
    #    device_map="auto")

    # Connect to Qdrant
    QDRANT_CLIENT = QdrantClient(host='localhost', port=6333)
    if does_collection_exist("sentences") is False:
        QDRANT_CLIENT.recreate_collection(
            collection_name='sentences',
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
        )


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


def search(embeddings):
    search_result = QDRANT_CLIENT.search(
        collection_name="sentences",
        query_vector = embeddings[0],
        query_filter = None,
        limit = 5
    )
    return [hit.payload for hit in search_result]


def process_input(input):
    output = "Hi Choom"
    return output


def cli_get_input():
    return input("You: ")


def main():
    initialize()

    while(True):
        # Get User Input
        input = cli_get_input()

        # Convert input into embeddings and store it
        embeddings = get_sentence_embeddings([input])
        store_embeddings(embeddings, [input])
        output = process_input(input)
        print(f"Miyu: {output}")

        payloads = search(embeddings)

        for idx, payload in enumerate(payloads):
            print(f"{idx}: {payload}")


if __name__ == "__main__":
    main()
