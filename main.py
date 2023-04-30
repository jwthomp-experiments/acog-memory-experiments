import logging
import os  # if you have not already done this
import readline
import signal
import sys

import torch

import acog.prompt as prompt
#import acog.memory as memory
import acog.text as text
from acog.util import log as acog_log

#from transformers import AutoTokenizer, AutoModelForCausalLM


#fd = os.open('/dev/null',os.O_WRONLY)
#os.dup2(fd,2)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def sigint_handler(signal, frame):
    print("\nBye now!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

CHARACTER_NAME = "Amura"
CHARACTER_PERSONA = "Heyo gang. My name is Hasano Amura and I'm a university student majoring in compsci. I'm currently working with a gamedev team on a Unity game... It's well, uhh, it's a gacha game with poorly drawn card art... But I have to make money to pay the rent you know? Don't judge..."


def process_prompt(p):
    return text.generate(p)


def cli_get_input():
    return input("You: ")


def main():
    #memory.initialize()
    text.initialize()

    history = prompt.create_history([
        {
            "you": "So, why did you get into gamedev?", 
            "bot": "I had this idea, and a passion. I did a couple indie things before getting this job, but my solo efforts didn't really pan out."
        },
        {
            "you": "Are you not much of a marketing/sales person?",
            "bot": "Oh my god! Not at all, it's kinda why I gave up on indie as a whole..."
        }
    ])


    while(True):
        acog_log("history", history)

        # Get User Input
        input = cli_get_input()

        # acog_log("input", input)
        
        # Convert input into embeddings and store it
        #memory.store(input)

        # Generate a prompt
        p = prompt.create(CHARACTER_NAME, CHARACTER_PERSONA, history, input)

        acog_log("prompt", p)

        # Turn prompt into an output message
        output = process_prompt(p)
        print(f"Amura: {output}")

        prompt.update_history(history, {"you": input, "bot": output})

        # Dump memory to see what we have (pure debugging)
        #payloads = memory.search(input)

        #for idx, payload in enumerate(payloads):
        #    print(f"{idx}: {payload}")


if __name__ == "__main__":
    main()
