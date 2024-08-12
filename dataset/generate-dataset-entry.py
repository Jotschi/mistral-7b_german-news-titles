import ollama
import json
import uuid
import random
import re

#print(ollama.list())
model="dolphin-mixtral:v2.7"

# Sources:
# https://konradweber.ch/2023/03/11/tool-nutzerorientierter-journalismus/
# https://smartocto.com/blog/explaining-user-needs/

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

def inferArticle(topic, userneed, userneed_description):
    prompt = """Du bist ein Nachrichten Redakteur. Schreibe einen Artikel für eine Deutsche Zeitung für das Thema {0}. Verzichte auf eine Einleitung, Titlel Zeile am Beginn des Artikels.
Formulieren den Artikel so das er das Userneed {1} erfüllt.
{2}
Gib nur den Arikel aus und keine Antwort oder einen Hinweis Ende. Gib nicht den Author aus. Erwähne dich nicht. Keine Überschrift.""".format(topic, userneed, userneed_description)
    
    print()
    print(prompt)
    print()
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    return response['message']['content'].strip()


# wissen
# Bringe mich auf den neuesten Stand (update me)
def inferUpdateMe(topic):
    
    # Gib 20 Verben aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Update me" erfüllen.
    update_me = [
        "Informieren",
        "Aktualisieren",
        "Berichten",
        "Erneuern",
        "Verändern",
        "Beeinflussen",
        "Modifizieren",
        "Revidieren",
        "Anpassen",
        "Wandeln",
        "Korrigieren",
        "Revisieren",
        "Überarbeiten",
        "Aktualisieren",
        "Erneuern",
        "Verändern",
        "Beeinflussen",
        "Modifizieren",
        "Revidieren",
        "Anpassen"
    ]
    
    verb = random.choice(update_me)
    description="""Achte hierbei darauf einen Artikel zu erstellen welcher Fakten zum Thema {0} beinhaltet und so Wissen vermittelt.
Der Artikel sollte die Fragen klären was genau passiert ist und welche Hintergründe vorliegen.
Wer, Wann, Wo, Was sind Fragen die beantwortet werden müssen.
Nutze das Verb '{1}' als Inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)
    
    info = {}
    info['text'] = inferArticle(topic,'"Bringe mich auf den neuesten Stand" (update me)', description)
    info['verb'] = verb
    info['type'] = 'update_me'
    return info



# verstehen
# Erkläre es mir (educate me)
def inferEducateMe(topic):
    
    
    # Gib 20 Verben auf Deutsch aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Educate me" erfüllen.
    educate_me = [
        "Informieren",
        "Analyse",
        "Erklären",
        "Bewerten",
        "Kommentieren",
        "Hinterfragen",
        "Kritisieren",
        "Erwarten",
        "Debattieren",
        "Hinzufügen",
        "Erinnern",
        "Reflektieren",
        "Erklären",
        "Warnen",
        "Vergleichen",
        "Voraussagen",
        "Erklären",
        "Zusammenfassen",
        "Erklären",
        "Interpretieren"
    ]

    verb = random.choice(educate_me)
    description = """Achte hierbei darauf komplizierte Aspekte leicht verständlich zu formulieren um so leichter Wissen zu vermitteln. 
Versuche den Artikel so zu formulieren das er die Neugier des Lesers auf weitere Hintergrundinformationen zum Thema weckt.
Nutze das Verb '{1}' als Inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)
    
    info = {}
    info['text'] = inferArticle(topic,'"Erkläre es mir" (educate me)', description)
    info['verb'] = verb
    info['type'] = "educate_me"
    return info

# wissen
# Halte mich auf dem Laufenden (keep me engaged)
def inferKeepMeEngaged(topic):
    
    # Gib 20 Verben auf Deutsch aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Halte mich auf dem Laufenden",
    keep_me_on_engaged = [
        "Informieren",
        "Aufklären",
        "Benachrichtigen",
        "Verbreiten",
        "Veröffentlichen",
        "Ankündigen",
        "Bekanntgeben",
        "Kommentieren",
        "Bewerten",
        "Kritisieren",
        "Loben",
        "Interviewen",
        "Fernsehen",
        "Radio hören",
        "Film schauen",
        "Musik genießen",
        "Veranstaltung besuchen",
        "Event teilnehmen",
        "Bloggen",
        "Sozial media aktiv nutzen",
    ]

    verb = random.choice(keep_me_on_engaged)
    description = """Achte hierbei darauf das Thema in einem aktuellen Zeitlichen Kontext zu verorten. 
Lege viel Wert darauf den Artikel zum Thema so zu formulieren das er den Leser dazu einläd über das Thema zu diskutieren.
Nutze das Verb '{1}' als Inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)
    
    info = {}
    info['text'] = inferArticle(topic,'"Halte mich auf dem Laufenden" (keep me engaged)', description)
    info['verb'] = verb
    info['type'] = "keep_me_engaged"
    return info
    

# verstehen
# Gib mir eine Perspektive (give me perspective)
def inferGiveMePerspective(topic):
    
    # Gib 20 Verben auf Deutsch aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Gib mir eine Perspektive (give me perspective)" erfüllen.
    give_me_perspective = [
        "beeinflussen",
        "erwarten",
        "verändern",
        "analysieren",
        "prognostizieren",
        "bewerten",
        "voraussagen",
        "beurteilen",
        "erklären",
        "vergleichen",
        "prüfen",
        "abschätzen",
        "analysieren",
        "erforschen",
        "überdenken",
        "erkennen",
        "überwachen",
        "beobachten",
        "bewerten",
        "prognostizieren"
    ]
    
    verb = random.choice(give_me_perspective)
    description = """Achte hierbei darauf das Thema so zu vermitteln das dem Leser anhand von Zitaten oder Analysen verschiedene Optionen dargelegt werden.
Diese Optionen können in Form von Vor und Nachteil, Hintergrund informationen oder interviews eingearbeitet werden. Der Text sollte so formuliert werden das der Leser seine eigene Meinung zum Thema bilden kann.
Nutze das Verb '{1}' als inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)
    
    info = {}
    info['text'] = inferArticle(topic,'"Gib mir eine Perspektive" (give me perspective)', description)
    info['verb'] = verb
    info['type'] = "give_me_perspective"
    return info

# fühlen
# Inspiriere mich (inspire me)
def inferInspireMe(topic):
    
    # Gib 20 Verben aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Inspire me" erfüllen.
    inspire_me = [
        "Begeistern",
        "Erwecken",
        "Anregen",
        "Ermutigen",
        "Motivieren",
        "Inspirieren",
        "Eingeben",
        "Erleuchten",
        "Beflügeln",
        "Bewegen",
        "Stimulieren",
        "Beleben",
        "Anstiften",
        "Schaffen"
        "Wecken",
        "Erheben",
        "Erhellen",
        "Energisieren"
    ]
    verb = random.choice(inspire_me)
    description="""Achte hierbei darauf den Artikel so zu formulieren das er den Leser positiv inspiriert. Eine Möglichkeit wäre es von positiven Errungenschaften und Aktionen zu berichten.
Alternativ können auch Lösungen zu Problemen presentiert werden. Der Arikel kann z.B. ein postives Licht auf ein ein negatives Thema werfen indem eine Lösung vorgeschlagen wird.
Nutze das Verb '{1}' als Inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)
    
    info = {}
    info['text'] = inferArticle(topic,'"Inspiriere mich" (inspire me)', description)
    info['verb'] = verb
    info['type'] = "inspire_me"
    return info

# fühlen
# Lenke mich ab (divert me)
def inferDivertMe(topic):
    
    # Gib 20 Verben auf Deutsch aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Lenke mich ab" erfüllen.
    divert_me = [
        "Träumen",
        "Phantasieren",
        "Spazieren gehen",
        "Schlendern",
        "Wandeln",
        "Verweilen",
        "Relaxen",
        "Entspannen",
        "Chillen",
        "Musik hören",
        "Fernsehen",
        "Radio hören",
        "Film schauen",
        "Spielen",
        "Malen",
        "Zeichnen",
        "Handarbeit",
        "Hobby betreiben",
        "Sport treiben",
        "Reiten"
    ]

    verb = random.choice(divert_me)    
    description = """Achte hierbei darauf negative Aspekte des Themas zu vermeiden.
Statdessen versuche den Artikel so zu formulieren das der Leser auf etwas lustiges, lockeres, aufregendes oder unterhaltsames zu dem Thema geleitet wird.
Ziel ist es hier den Leser von anderen "hard news" abzulenken.
Nutze das Verb '{1}' als inspiration wenn du den Artikel zum Thema {0} erstellst.
""".format(topic, verb)

    info = {}
    info['text'] = inferArticle(topic,'"Lenke mich ab" (divert me)', description)
    info['verb'] = verb
    info['type'] = "divert_me"
    return info

# machen
# Vernetze mich mit anderen (connect me)
def inferConnectMe(topic):
    
    # Gib 20 Verben auf Deutsch aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Vernetze mich mit anderen" (connect me) erfüllen.
    connect_me = [
        "Verbinden",
        "Zusammenbringen",
        "Integrieren",
        "Verknüpfen",
        "Vernetzen",
        "Kooperieren",
        "Zusammenarbeiten",
        "Gemeinschaft schaffen",
        "Miteinander teilen",
        "Beziehungen aufbauen",
        "Interagieren",
        "Austauschen",
        "Zusammenwirken",
        "Verbindlichkeit schaffen",
        "Zusammenarbeiten",
        "Gemeinschaft bilden",
        "Sich vernetzen",
        "In Verbindung treten",
        "Zusammenwirken",
        "Sich zusammenschließen"
    ]
    
    verb = random.choice(connect_me)
    description = """Achte hierbei darauf den Artikel so zu formulieren das er den Leser dazu auffordert sich für das Thema zu engagieren.
Mögliche Varienten sind: Meinungen, Ankündigungen, Bekanntmachungen, Einladungen
Nutze das Verb '{1}' als Inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)  
    
    info = {}
    info['text'] = inferArticle(topic,'"Vernetze mich mit anderen" (connect me)', description)
    info['verb'] = verb
    info['type'] = "connect_me"
    return info

# machen
# Hilf mir (help me)
def inferHelpMe(topic):

    # Gib 20 Verben auf Deutsch aus welche häufig in Nachrichten Artikeln verwendet werden welche das Userneed "Hilf mir" (help me) erfüllen.
    help_me = [
        "Unterstützen",
        "Beantworten",
        "Erklären",
        "Informieren",
        "Beraten",
        "Helfen",
        "Orientieren",
        "Anweisen",
        "Lehren",
        "Lernen",
        "Schulem",
        "Weisen",
        "Aufklären",
        "Informieren",
        "Anleiten",
        "Erklären",
        "Veranschaulichen",
        "Aufzeigen",
        "Erläutern"
    ]
    
    
    verb = random.choice(help_me)
    description = """Achte hierbei darauf dem Leser Hilfestellung zu geben indem Tips oder Informationen für Thema {0} bereitgestellt werden welches das Leben des Leser betrifft.
Mögliche Hilfen können in Form von Timelines, Checklisten, Frage Antwort Paaren, Schritt für Schritt Anleitungen oder Interviews von Experten vorliegen.
Nutze das Verb '{1}' als Inspiration wenn du den Artikel zum Thema {0} erstellst.""".format(topic, verb)  


    info = {}
    info['text'] = inferArticle(topic,'"Hilf mir" (help me)', description)
    info['verb'] = verb
    info['type'] = "help_me"
    return info


def inferTitles(topic, article):
    prompt = """Du bist ein Nachrichten Redakteur. Schreibe einen Artikel für eine Deutsche Zeitung für das Thema {0}. Verzichte auf eine Einleitung, Titlel Zeile am Beginn des Artikels. 
Gib nur den Arikel aus und keine Antwort oder einen Hinweis Ende. 
Gib nicht den Author aus. Erwähne dich nicht. Keine Überschrift.""".format(topic)

    response = ollama.chat(model=model, messages=[
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
        'content': 'Schreibe 20 Titelvorschläge unterschiedlicher länge für den Aritkel.',
    },
    ])
    
    text = response['message']['content'].strip()
    array = re.split("\n\d+\.", text)
    titles = [line.strip().strip('"').strip("1. ") for line in array]
    return titles


def main():
    topic = random.choice(news_topics)
    
    user_needs = [inferUpdateMe,inferEducateMe,inferKeepMeEngaged,inferGiveMePerspective,inferInspireMe,inferDivertMe,inferConnectMe,inferHelpMe]
    info = random.choice(user_needs)(topic)

    article = info['text']
    need_verb = info['verb']
    need_name = info['type']
    titles = inferTitles(topic, article)
    dic = {
        "topic": topic,
        "userneed_name": need_name,
        "userneed_verb": need_verb,
        "text": article,
        "titles": titles
    }

    json_object = json.dumps(dic, indent=4)
    article_uuid = str(uuid.uuid4())
    filename = article_uuid + ".json"
    print("""[{0}] {1} + {2} => {3}""".format(need_name, topic, need_verb, article_uuid))
#    with open(article_uuid +"_article.txt", "w") as text_file:
#        text_file.write(article)
#
#    with open(article_uuid +"_titles.txt", "w") as text_file:
#        text_file.write(titles)

    with open("json/" + filename, "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    main()