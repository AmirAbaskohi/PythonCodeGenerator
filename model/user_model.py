from numpy import mod
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling, training_args
from datasets import load_dataset
from transformers.data import data_collator
from transformers import Trainer, TrainingArguments
import os

os.environ["WANDB_DISABLED"] = "true"

def encode(lines):
    return tokenizer(lines['text'], add_special_tokens=True, truncation=True, max_length=512)

TRAIN_BASE = False
TOKENIZER_DIR = "../tokenizer"

paths = ["../data.txt"]

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(files=paths, vocab_size=52000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    tokenizer.save_model(TOKENIZER_DIR)

inp = "print('hello world!')"

tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER_DIR)
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

t = tokenizer.encode(inp)
print(t)
print(tokenizer.decode(t))

config = GPT2Config(
    vocab_size = tokenizer.vocab_size,
    bos_token = tokenizer.bos_token_id,
    eos_token = tokenizer.eos_token_id
)

model = GPT2LMHeadModel.from_pretrained("GPyT").to("cuda")

while True:
    inp = input(">>> ")
    input_ids = tokenizer.encode(inp, return_tensors="pt").to("cuda")
    beam_output = model.generate(
        input_ids,
        max_length = 512,
        num_beams=10,
        temperature=0.7,
        no_repeat_ngram_size=5,
        num_return_sequences=1
    )

    for beam in beam_output:
        out = tokenizer.decode()
        fout = out.replace("<N>", "\n")

        print(green(str(fout)))