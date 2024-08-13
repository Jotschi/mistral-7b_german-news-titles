from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch
import sys
from peft import AutoPeftModelForCausalLM
from transformers import GenerationConfig

device = "cuda" # the device to load the model onto

model_path = sys.argv[1]
model_path = "./" + model_path
base_model_id = "mistralai/Mistral-7B-Instruct-v0.3"

################
# Tokenizer
################

tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
#tokenizer.padding_side = 'right'

################
# Base Model
################

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type= "nf4",
    bnb_4bit_compute_dtype= torch.bfloat16,
    bnb_4bit_use_double_quant=False
)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    low_cpu_mem_usage=True,
    quantization_config=bnb_config,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map="cuda")


################
# PEFT Model
################

ft_model = PeftModel.from_pretrained(base_model, model_path)

################
# Inference
################

generation_config = GenerationConfig(
    do_sample=True,
    top_k=1,
    temperature=0.1,
    max_new_tokens=256,
    pad_token_id=tokenizer.pad_token_id
)

text_1 = "Trotz Verzögerungen beim Bau hat das Regierungskabinett in Indonesien heute erstmals in der künftigen Hauptstadt Nusantara auf der Insel Borneo getagt. Auf Wunsch des Präsidenten Joko Widodo reisten für die Sitzung Dutzende indonesische Beamte in die neu gebaute Stadt. „Nicht alle Staaten haben die Möglichkeit und die Fähigkeit, bei null anzufangen und ihre Hauptstadt neu zu bauen“, betonte Widodo."
text_2 = "Die Nachricht vom Tod des Bauunternehmers und Reality-TV-Stars Richard Lugner hat am Montag innerhalb kurzer Zeit österreichweit zahlreiche Reaktionen der Trauer ausgelöst - vom Bundespräsidenten abwärts und durch alle politischen Lager." 
text_3 = "Einstein gilt als einer der bedeutendsten Physiker der Wissenschaftsgeschichte und weltweit als einer der bekanntesten Wissenschaftler der Neuzeit."
text_4 = "Albert Einstein (* 14. März 1879 in Ulm; † 18. April 1955 in Princeton, New Jersey) war ein schweizerisch-US-amerikanischer theoretischer Physiker deutscher Herkunft. Der Wissenschaftler jüdischer Abstammung hatte bis 1896 die württembergische Staatsbürgerschaft, ab 1901 die Schweizer Staatsbürgerschaft und ab 1940 zusätzlich die US-amerikanische. Preußischer Staatsangehöriger war er von 1914 bis 1934."

for text in [ text_1, text_2, text_3, text_4]:
    for count in [ 7, 14, 18, 22]:
        query = "Erstelle einen " + str(count) + " Wörter langen Titelvorschlag für folgenden Artikel:\n" + text

        messages = [
            {"role": "user", "content": query}
        ]

        print("[" + str(count) + "] Generating...")
        model_input = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
        outputs = ft_model.generate(model_input, generation_config=generation_config)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(answer)
        print("[" + str(count) + "] Done")
        print("\n");
