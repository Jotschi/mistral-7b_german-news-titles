from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,HfArgumentParser, TrainingArguments, pipeline, logging, TextStreamer
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training, get_peft_model
import os, torch, wandb, platform, warnings
from datasets import load_dataset, DatasetDict
from trl import SFTTrainer
import re

max_seq_length=128
base_model = "mistralai/Mistral-7B-Instruct-v0.3"
dataset_name = "Jotschi/german-news-titles"
new_model = "Jotschi/Mistral-7B-v0.3-german-news-titles"

wandb.init(project="mistral7b-instruct-news-title")


training_arguments = TrainingArguments(
    output_dir= "./results",
    num_train_epochs= 18,
    per_device_train_batch_size= 4,
    gradient_accumulation_steps= 2,
    optim = "paged_adamw_8bit",
    save_steps=200,
    logging_steps= 100,
    learning_rate= 2e-4,
    weight_decay= 0.001,
    fp16= False,
    bf16= True,
    max_grad_norm= 0.3,
    max_steps= -1,
    warmup_ratio= 0.3,
    group_by_length= True,
    lr_scheduler_type= "constant",
    report_to="wandb"
)

################
# Tokenizer
################

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
#tokenizer.padding_side = "left"

################
# Dataset
################

def prepare_dialogue(text, title):
  
  #text  = "Einstein gilt als einer der bedeutendsten Physiker der Wissenschaftsgeschichte und weltweit als einer der bekanntesten Wissenschaftler der Neuzeit."
  #title = "Albert Einstein war ein Genie!"
  count=count_words(title)
  prompt="Erstelle einen " + str(count) + " Wörter langen Titelvorschlag für folgenden Artikel:\n" + text
  #print(str(count))
  chat = [
       {"role": "user", "content": prompt},
       {"role": "assistant", "content": "Titelvorschlag: " + title},
    ]
  
  return tokenizer.apply_chat_template(chat, tokenize=False) + tokenizer.eos_token

def count_words(text):
    # Remove punctuation using a regular expression
    clean_text = re.sub(r'[^\w\s]', '', text)
    # Split the text into words
    words = clean_text.split()
    # Return the number of words
    return len(words)

def chunk_examples(batch):
    all_samples = []
    batched_text = batch["text"]
    batched_titles = batch["titles"]
    for i in range(len(batched_text)):
        text = batched_text[i]
        titles = batched_titles[i]
        for title in titles:
            #print("Title: " + title)
            all_samples += [ prepare_dialogue(text, title) ]
    return {"text": all_samples}

dataset = load_dataset(dataset_name)
print(dataset['train'])

train_dataset = dataset['train'].map(chunk_examples, batched=True, num_proc=4, remove_columns=["titles", "text"])
test_dataset = dataset['test'].map(chunk_examples, batched=True, num_proc=4, remove_columns=["titles", "text"])

################
# Model
################

torch_dtype = torch.bfloat16
quant_storage_dtype = torch.bfloat16

bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch_dtype,
        bnb_4bit_quant_storage=quant_storage_dtype,
    )
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    attn_implementation="sdpa", # use sdpa, alternatively use "flash_attention_2"
    torch_dtype=quant_storage_dtype,
    use_cache=False if training_arguments.gradient_checkpointing else True,  # this is needed for gradient checkpointing
    #device_map={"": 0}
)

if training_arguments.gradient_checkpointing:
    model.gradient_checkpointing_enable()

################
# PEFT
################

peft_config = LoraConfig(
        r=64,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        #target_modules="all-linear")
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj","gate_proj", "up_proj", "down_proj", "lm_head"])
model = get_peft_model(model, peft_config)

################
# Training
################

# Setting sft parameters
trainer = SFTTrainer(
    model=model,
    args=training_arguments,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    peft_config=peft_config,
    max_seq_length=max_seq_length,
    dataset_text_field="text",
    tokenizer=tokenizer,
    packing=True,
)

if trainer.accelerator.is_main_process:
    trainer.model.print_trainable_parameters()

trainer.train()
# Save the fine-tuned model
trainer.model.save_pretrained(new_model)
wandb.finish()
model.config.use_cache = True
model.eval()
