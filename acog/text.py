from pyllamacpp.model import Model

__all__ = ["initialize", "genrate"]

MODEL = None
TOKENIZER = None


def initialize():
    global MODEL
    global TOKENIZER

    MODEL = Model(ggml_model="models/gpt4all-lora-unfiltered-quantized-converted.bin", n_ctx=512)

    #TOKENIZER = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-6B")
    #MODEL = AutoModelForCausalLM.from_pretrained(
    #    "PygmalionAI/pygmalion-6B", 
    #    torch_dtype=torch.float16, 
    #    load_in_8bit=True, 
    #    device_map="auto")
    #

def generate(prompt, input):
    text = f"{prompt}You: {input}\nAmura:"
    generated_text = MODEL.generate(text, n_predict=128, n_threads=6)
    return generated_text
