import os
import re
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np

with open(os.path.join(os.path.dirname(__file__), 'word_blacklist1.txt')) as file:
   blacklist = set(file.read().split('\n'))                                                 #   wrzucone do seta bo najlepsze data type fo tego chyba + relative path!!!
   blacklist.discard('')
   blacklist.discard(' ')
   #blacklist = set(line.strip() for line in file)                                          #   For large blacklist this option would provide faster bootup

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

def removedup(string):                                                                  #   usuwanie tych samych literek kolo sb (chuuuuj = chuj)
    return re.sub(r"(.)\1+", r"\1", string)                                             #   mozna zamienic na lambde

def inputtolist(string):
    return re.findall(r'\w+', string)                                                   #  mozna tez zamienic na lambde

def lower(string):
    return string.lower()



def cenzo(string, int):                                                                      #  cenzurowanie slowek      (wrzucilem tutaj logike bo nie mam pojecia jak dac IF do zwektoryzowanej funkcji bez iterowania)
    if int >= threshold:
        return string[0] + '*' * (len(string)-2) + string[-1] #and True
    else:
        return string #and False

def partial_match(x,y):
    return(fuzz.ratio(x,y))

partial_match_vector = np.vectorize(partial_match)                                      #   https://stackoverflow.com/questions/56040817/python-fuzzy-matching-strings-in-list-performance
partial_cenzo_vector = np.vectorize(cenzo)




input = "Chuj chuj chuj chój chuja chuuuuuuuja chujek chuju chujem huj huja hujek huju hujem"
output = []
#inputlistvar = inputtolist(input)
threshold = 75                                                                          #   w jakim procencie musza sie pokrywac by byc ocenzurowane (0-100)





dataframecolumn_match = pd.DataFrame(inputtolist(removedup(translatetable(lower(input)))))
dataframecolumn_original = pd.DataFrame(inputtolist(input))
dataframecolumn_original.columns = ['Original']
dataframecolumn_match.columns = ['Match']

dataframecolumn_compare = pd.DataFrame(blacklist)
dataframecolumn_compare.columns = ['Compare']                                           #   nie pytajcie do konca jak to wszystko dziala ale dziala SZYBKO czyli zajebiscie ale sie jebalem z tym fchuj

dataframecolumn_original['Match'] = dataframecolumn_match
dataframecolumn_original['Key'] = 1
dataframecolumn_compare['Key'] = 1

combined_dataframe = dataframecolumn_original.merge(dataframecolumn_compare,on="Key",how="left")

combined_dataframe['Score']=partial_match_vector(combined_dataframe['Match'],combined_dataframe['Compare'])

combined_dataframe['Cenzored']=partial_cenzo_vector(combined_dataframe['Original'], combined_dataframe['Score'])

print(combined_dataframe)