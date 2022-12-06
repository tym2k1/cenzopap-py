import os
import re

with open(os.path.join(os.path.dirname(__file__), 'word_blacklist.txt')) as file:
   blacklist = set(file.read().split())                                                 #   wrzucone do seta bo najlepsze data type fo tego chyba + relative path!!!
   #blacklist = set(line.strip() for line in file)                                      #   For large sets of words this option would be faster

replacement_dict = {
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ł': 'l',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ź': 'z',
    'ż': 'z',
    #'0': 'o',
    #'1': 'i',
    #'2': 'z',
    #'3': 'e',
    #'4': 'a',
    #'5': 's',
    #'\/': 'v',
    '@': 'a',
    '^': 'a',
    '/\\': 'a',
    '/-\\': 'a',    #   jak przesadzilem dajcie znac xd
    '8': 'b',       #   imo do wrzucenia w inny plik bo sie rozroslo do giga rozmiarow a tez tak fajnie ze wiecie mozna edytowac user friendly
    '6': 'b',       #   nie wszystkie chyba maja do konca sens ale fajnie zeby bylo ze mamy w slowniku opcje kilkuliterowe cause were cool
    '13': 'b',      #   cenzurowanie ASCII art lets go
    '|3': 'b',
    '/3': 'b',
    'ß': 'b',
    'P>': 'b',
    '|:': 'b',
    '©': 'c',
    '¢': 'c',
    '<': 'c',
    '[': 'c',
    '(': 'c',
    '{': 'c',
    ')': 'd',
    '|)': 'd',
    '[)': 'd',
    '|>': 'd',
    '|o': 'd',
    '3': 'e',
    '&': 'e',
    '€': 'e',
    'ë': 'e',
    '[-': 'e',      # dokoncze potem
}

def translatetable(string):
    regex = re.compile('|'.join(map(re.escape, replacement_dict)))                      #   https://stackoverflow.com/questions/63230213/translate-table-value-error-valueerror-string-keys-in-translate-table-must-be-o
    return regex.sub(lambda match: replacement_dict[match.group(0)], string)            #   :)

#def translatetable(string):
    #string = string.translate(str.maketrans(replacement_dict))                         #   Works only for dict keys with a size of 1
    #return string

def removedup(string):
    string = re.sub(r"(.)\1+", r"\1", string)                                           #   usuwanie tych samych literek kolo sb (chuuuuj = chuj)
    return string                                                                       #   mozna zamienic na lambde

def inputtolist(string):
    wordlist = re.findall(r'\w+', string)
    return wordlist                                                                      #  mozna tez zamienic na lambde

def cenzo(string):                                                                       #  main func poki co
    #string = match.group()
    if removedup(translatetable(string.lower())) in blacklist:
        #return '*' * len(string)                                                         #  2 wersje zwracanie full cenzo (chuj = ****) albo niepelne (chuj = c**j)
        return string[0] + '*' * (len(string)-2) + string[-1] 
    else:
        return string

print(translatetable('\/4p3'))
print(translatetable('CH000000000i'))
print(inputtolist("dupa maryna cyce wadowice"))

in1 = "test dupa chuj gowno gówno pizda ogień jebać politechnikę gównianą pierdolic pięrdołić"
out1 = []
for i in inputtolist(in1):
    out1.append(cenzo(i))
print(out1)