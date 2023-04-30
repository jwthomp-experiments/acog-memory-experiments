import logging

from pyllamacpp.model import Model

from acog.util import log as acog_log

__all__ = ["initialize", "genrate"]

MODEL = None
TOKENIZER = None


def initialize():
    global MODEL
    global TOKENIZER

    MODEL = Model(
        ggml_model="models/gpt4all-lora-unfiltered-quantized-converted.bin",
        log_level=logging.NOTSET,
        n_ctx=512)

    #TOKENIZER = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-6B")
    #MODEL = AutoModelForCausalLM.from_pretrained(
    #    "PygmalionAI/pygmalion-6B", 
    #    torch_dtype=torch.float16, 
    #    load_in_8bit=True, 
    #    device_map="auto")
    #

def generate(prompt):
    generated_text = MODEL.generate(
        prompt,
        n_predict=50,
        n_threads=6,
        verbose=False)
        #top_k = 0,
        #repeat_penalty = 1.05,
        # temp = 0.6,
        #top_p = 0.9)

    acog_log("generated text", generated_text)

    filtered_text = generated_text[len(prompt) + 1:]

    # Strip any extra \nYou: or \n<BOT>: out
    idx = filtered_text.find("\nYou:")
    if idx > -1:
        filtered_text = filtered_text[0:idx]
    idx = filtered_text.find("\nYou :")
    if idx > -1:
        filtered_text = filtered_text[0:idx]
    idx = filtered_text.find("\n<BOT>:")
    if idx > -1:
        filtered_text = filtered_text[0:idx]

    return filtered_text
