import ollama
import json
import uuid
import random
import re
import sys

#print(ollama.list())
model="dolphin-mixtral:v2.7"




def testArticle(article):
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': 'Du bist ein Nachrichten Redakteur. Analysiere den Artikel und prüfe welche Userneeds dieser erfüllt.\n'
        + 'Es gibt folgende userneeds:\n'
        
        + '* wissen - keep me engaged: Halte mich auf dem Laufenden\n'
        + '* wissen - update me: Bringe mich auf den neuesten Stand - Der Artikel sollte die Fragen klären was genau passiert ist und welche Hintergründe vorliegen.\n'
        
        '* verstehen - educate me: Erkläre es mir - Der Artikel vermittelt das Thema auf eine Verständliche weise und gibt Hintergrund informationen die das Interesse des Lesers wecken.\n'
        '* verstehen - give me perspective: Gib mir eine Perspektive - Der Artikel ist so formuliert das er verschiedene Blickwinkel auf das Thema enthält. Er kann Hintergrund informationen enthalten oder aber auch Vor und Nachteile aufzählen. Manchmal werden auch Zitate und Interviews verwendet um das Thema auf verschiedenen Winkeln zu betrachten.\n'
        
        '* fühlen - inspire me: Inspiriere mich - Der Artikel ist weniger rational und spricht eher die emotionale Seite an. Er ist so verfasst das er die positiven Aspekte zu dem Thema auf listet. Oftmals ist der Artikel sehr persönlich.\n'
        '* fühlen - divert me: Lenke mich ab - Der Arikel lenkt von hardnews ab indem er das Thema lustig oder interessant vermittelt. Er spricht die emotionale Seite an uns ist eher positiv formuliert.\n'
        
        + '* machen - connect me: Vernetze mich mit anderen - \n'
        + '* machen - help me: Hilf mir - Der Artikel enthält informationen welche dem Leser im täglichen Leben helfen\n'
         
        + 'Gib nur die Userneed Namen aus. Gib einen Score von 0-10 pro userneed aus. 0 bedeutet der need wird nicht erfüllt. 10 bedeutet er wird maximal erfüllt. Gib keine weiter Erklärung aus.\n'
         'Hier nun der zu bewertende der Artikel:\n' + article,
    },
    ])
    return response['message']['content'].strip()


def main():
    file = sys.argv[1]
    print ('Reading file', file)
    f = open(file)
    data = json.load(f)
    print(testArticle(data['text']))
    print("Aricle: " + data['topic'] + " need: "+ data['userneed_name'] + ", " + data['userneed_verb'])
if __name__ == "__main__":
    main()