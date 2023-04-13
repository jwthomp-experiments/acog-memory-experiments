import signal
import sys
import torch
#from transformers import AutoTokenizer, AutoModelForCausalLM

import acog.memory as memory
import acog.text as text


def sigint_handler(signal, frame):
    print("\nBye now!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def process_input(input):
   prompt2 = """Amura's Persona: Heyo gang. My name is Hasano Amura and I'm a university student majoring in compsci. I'm currently working with a gamedev team on a Unity game... It's well, uhh, it's a gacha game with poorly drawn card art... But I have to make money to pay the rent you know? Don't judge...
<START>
You: So, why did you get into gamedev?
Amura: I had this idea, and a passion. I did a couple indie things before getting this job, but my solo efforts didn't really pan out.
You: Are you not much of a marketing/sales person?
Amura: Oh my god! Not at all, it's kinda why I gave up on indie as a whole...
"""
   return text.generate(prompt2, input)


def cli_get_input():
    return input("You: ")


def main():
    memory.initialize()
    text.initialize()

    while(True):
        # Get User Input
        input = cli_get_input()

        # Convert input into embeddings and store it
        memory.store(input)
        
        # Turn input into an output message
        output = process_input(input)
        print(f"Miyu: {output}")

        # Dump memory to see what we have (pure debugging)
        payloads = memory.search(input)

        for idx, payload in enumerate(payloads):
            print(f"{idx}: {payload}")


if __name__ == "__main__":
    main()
