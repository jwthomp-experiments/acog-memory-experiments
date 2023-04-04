import signal
import sys
import uuid4

import torch
#from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)



TOKENIZER = None
MODEL = None
SENTENCE_MODEL = None

def sigint_handler(signal, frame):
    print("\nBye now!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def initialize():
    global TOKENIZER
    global MODEL
    global SENTENCE_MODEL

    SENTENCE_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    ##TOKENIZER = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-6B")
    #MODEL = AutoModelForCausalLM.from_pretrained(
    #    "PygmalionAI/pygmalion-6B", 
    #    torch_dtype=torch.float16, 
    #    load_in_8bit=True, 
    #    device_map="auto")

    # Connect to Milvus Vector Database
    connections.connect("default", host="localhost", port="19530")

    schema = CollectionSchema(
        fields = [
            FieldSchema(
                name = "id",
                dtype = DataType.VARCHAR,
                is_primary = True,
                max_length = 36
            ),
            FieldSchema(
                name = "speaker",
                dtype = DataType.VARCHAR,
                max_length = 64
            ),
            FieldSchema(
                name = "message",
                dtype = DataType.FLOAT_VECTOR,
                dim=384
            )
        ]
    )

def process_text(input):
    output = "Hi Choom"

    embeddings = SENTENCE_MODEL.encode(input)
    print(embeddings)
    print(f"Length: {len(embeddings[0])}")

    return output

def main():
    initialize()

    while(True):
        text = input("You: ")
        embeddings = get_sentence_embeddings(text)
        unique_id = str(uuid4())
        output = process_text([text])
        print(f"Miyu: {output}")


if __name__ == "__main__":
    main()
