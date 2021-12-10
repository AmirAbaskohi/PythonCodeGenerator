from numpy import mod
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling, training_args
from datasets import load_dataset
from transformers.data import data_collator
from transformers import Trainer, TrainingArguments
import os

def encode(lines):
    return tokenizer(lines['text'], add_special_tokens=True, truncation=True, max_length=512)

TRAIN_BASE = False
TOKENIZER_DIR = "tokenizer"

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
    bos_token_id = tokenizer.bos_token_id,
    eos_token_id = tokenizer.eos_token_id
)

model = GPT2LMHeadModel()

dataset = load_dataset("text", data_files=paths)

dataset.set_transform(encode)
dataset = dataset['train']

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

if not os.path.exists("../GPyT"):
    os.makedirs("../GPyT")

training_args = TrainingArguments(
    output_dir="../GPyT",
    per_device_train_batch_size=10,
    overwrite_output_dir=True,
    num_train_epochs=1,
    save_steps=100,
    save_total_limit=2,
    prediction_loss_only=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset
)

trainer.train()
trainer.save_model("GPyT")