import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Set random seed for reproducibility
torch.random.manual_seed(0)

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "./model",
    device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained("./model/Phi-3-mini-4k-instruct")

# Create the pipeline for text generation
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

def generate_text(messages, max_new_tokens=500, temperature=0.0):
    generation_args = {
        "max_new_tokens": max_new_tokens,
        "return_full_text": False,
        "temperature": temperature,
        "do_sample": False,
    }
    response = pipe(messages, **generation_args)
    return response[0]['generated_text']
