import ollama
import json
import uuid
import random
import re
from pathlib import Path


#model="dolphin-mixtral:v2.7"
model="gemma2:27b-instruct-q8_0"

client = ollama.Client(host='http://127.0.0.1:11435')
print("Ollama models:")
print(client.list())

# Gib 20 Nomen für einen Nachrichten Artikel mit dem Thema Luftverschmutzung aus.
# Gib 20 Adjektive für einen Nachrichten Artikel mit dem Thema Luftverschmutzung aus.

# Topics: zähle mindestens 50 Themen Bereiche auf die in Nachrichten abgebildet werden. Verzichte auf eine Beschreibung.
news_topics = [
    "Politik",
    "Wirtschaft",
    "Gesellschaft",
    "Wissenschaft und Technologie",
    "Umwelt",
    "Gesundheit",
    "Sport",
    "Medien und Unterhaltung",
    "Reisen und Tourismus",
    "Wetter und Naturkatastrophen",
    "Bildung",
    "Religion",
    "Justiz und Recht",
    "Landwirtschaft",
    "Krieg und Frieden",
    "Architektur und Stadtentwicklung",
    "Kunst und Kultur",
    "Arbeitsmarkt",
    "Verkehr und Infrastruktur",
    "Energie und Rohstoffe",
    "Immobilien",
    "Kriminalität",
    "Verbraucherschutz",
    "Raumfahrt",
    "Politische Parteien",
    "Internationale Beziehungen",
    "Lokalnachrichten",
    "Nationalnachrichten",
    "Auslandsnachrichten",
    "Politische Entscheidungen",
    "Steuern und Abgaben",
    "Soziale Medien",
    "Datenschutz",
    "Geopolitik",
    "Menschenrechte",
    "Tierschutz",
    "Bildungspolitik",
    "Wissenschaftspolitik",
    "Forschung und Entwicklung",
    "Innovation und Start-ups",
    "Klimawandel",
    "Nachhaltigkeit",
    "Umweltschutz",
    "Abfallwirtschaft",
    "Wasserwirtschaft",
    "Luftverschmutzung",
    "Arzneimittel",
    "Impfungen",
    "Öffentliche Gesundheit",
    "Sucht und Drogen"
]

def inferArticle(topic):
    prompt = """Du bist ein Nachrichten Redakteur. Schreibe einen Artikel für eine Deutsche Zeitung für das Thema {0}. Verzichte auf eine Einleitung, Titlel Zeile am Beginn des Artikels.
Gib nur den Artikel aus und keine Antwort oder einen Hinweis Ende. Gib nicht den Author aus. Erwähne dich nicht. Keine Überschrift.""".format(topic)
    
    print()
    print(prompt)
    print()
    response = client.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    return response['message']['content'].strip()



def inferTitles(topic, article):
    prompt = """Du bist ein Nachrichten Redakteur. Schreibe einen Artikel für eine Deutsche Zeitung für das Thema {0}. Verzichte auf eine Einleitung, Titlel Zeile am Beginn des Artikels. 
Gib nur den Artikel aus und keine Antwort oder einen Hinweis Ende. 
Gib nicht den Author aus. Erwähne dich nicht. Keine Überschrift.""".format(topic)

    response = client.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    {
        'role': 'assistant',
        'content': article,
    },
    {
        'role': 'user',
        'content': 'Schreibe 20 Titelvorschläge unterschiedlicher Länge für den Aritkel.',
    },
    ])
    
    text = response['message']['content'].strip()
    array = re.split("\n\d+\.", text)
    blacklist=["Titelvorschl", "**"];
    titles = [line.strip().strip('"').strip("1. ") for line in array]
    titles = [s for s in titles if not any(sub in s for sub in blacklist)]
    return titles


def main():
    topic = random.choice(news_topics)
    article = inferArticle(topic)
    titles = inferTitles(topic, article)
    dic = {
        "topic": topic,
        "text": article,
        "titles": titles
    }

    json_object = json.dumps(dic, indent=4)
    article_uuid = str(uuid.uuid4())
    filename = article_uuid + ".json"
    print("""[{0}] => {1}""".format(topic, article_uuid))
#    with open(article_uuid +"_article.txt", "w") as text_file:
#        text_file.write(article)
#
#    with open(article_uuid +"_titles.txt", "w") as text_file:
#        text_file.write(titles)

    Path("json").mkdir(parents=True, exist_ok=True)
    with open("json/" + filename, "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    main()