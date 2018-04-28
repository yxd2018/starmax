html = """
Hallo, dies ist eine 
ziemlich lange Zeile, die in Html
aber nicht wird.
<br>
Zwei <br> <br> produzieren zwei Newlines. 
Es gibt auch noch das tag <hr> was einen Trenner darstellt.
Zwei <hr> <hr> produzieren zwei Horizontal Rulers.
Achtung       mehrere Leerzeichen irritieren

Html genauso wenig wie


mehrere Leerzeilen.
"""

def parse(html):
    lines = html.split("\n")
    words = []
    for line in lines:
        temp = line.split(" ")
        for word in temp:
            if word != "" and word != " ":
                words.append(word)
    return words
def print_words(words):
    line = ""
    for word in words:
        if word == "<br>":
            print line
            line = ""
        elif word == "<hr>":
            if len(line) != 0:
                print line
                line = ""
            print("-"*80)
        elif len(word) + len(line) > 80:
            print line[:-1]
            line = word + " "
        else:
            line = line + word + " "
    if len(line) != 0:
        print(line[:-1])

words = parse(html)
print words
print '************'
print_words(words)


