from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import sys

device = "cuda" # the device to load the model onto

model_path = sys.argv[1]
model_path = "./" + model_path

quantization_config = BitsAndBytesConfig(
    load_in_8bit=False, load_in_4bit=True
)

model = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(model_path)

text = "Erstelle einen Titelvorschlag für den Text.\n"
text += "Albert Einstein (* 14. März 1879 in Ulm; † 18. April 1955 in Princeton, New Jersey) war ein schweizerisch-US-amerikanischer theoretischer Physiker deutscher Herkunft. Der Wissenschaftler jüdischer Abstammung hatte bis 1896 die württembergische Staatsbürgerschaft, ab 1901 die Schweizer Staatsbürgerschaft und ab 1940 zusätzlich die US-amerikanische. Preußischer Staatsangehöriger war er von 1914 bis 1934."

messages = [
    {"role": "user", "content": text},
]

encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

model_inputs = encodeds.to(device)
generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])