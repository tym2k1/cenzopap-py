import os
import re
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np

with open(os.path.join(os.path.dirname(__file__), 'word_blacklist.txt')) as file:
   blacklist = set(file.read().split('\n'))                                                 #   wrzucone do seta bo najlepsze data type fo tego chyba + relative path!!!
   #blacklistset = set(line.strip() for line in file)                                          #   For large blacklist this option would provide faster bootup
   blacklist.discard('')
   blacklist.discard(' ')


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
   #    replaces characters imitating letters to letters
    regex = re.compile('|'.join(map(re.escape, replacement_dict)))                      #   https://stackoverflow.com/questions/63230213/translate-table-value-error-valueerror-string-keys-in-translate-table-must-be-o
    return regex.sub(lambda match: replacement_dict[match.group(0)], string)            #   :)

def removedup(string):                                                                  #   usuwanie tych samych literek kolo sb (chuuuuj = chuj)
    #   removes duplicate letters
    return re.sub(r"(.)\1+", r"\1", string)                                             #   mozna zamienic na lambde

def inputtolist(string):
    #   find all words separated by characters [a-zA-Z0-9_]+
    string = re.split(r'(\S+)', string)                                                   #  mozna tez zamienic na lambde
    string1 = []
    string[0 : 1] = [''.join(string[0 : 2])]
    string.pop(1)
    for i in range(0, len(string), 2):
        string1.append(string[i] + string[i+1])                                             #    chcialem uniknac loopow ale tutaj troche zglupialem (moze to sie da zrobic madrym regexem ale nie mam czasu bardziej eksperymentowac)
    return string1


def inputtomatch(string):
    #   find all words separated by characters [a-zA-Z0-9_]+
    string = re.sub(r'[^a-zA-Z\d\s:]', '', string)
    return re.findall(r'\S+', string)

def lower(string):
    return string.lower()



def cenzo(string, match, int):
    #   replaces inner letters in a word with stars if its similarity with blacklist word is greater than treshold
    if int >= threshold and match > 2:
        return re.sub(r'\w', '*', string)
    else:
        return string

def partial_match(x,y):
   #    returns the ratio of similarity between 2 words
    return(fuzz.ratio(x,y))

#def partial_test(x,y):
#    print(fuzz.ratio(x,y))
#    print(fuzz.partial_ratio(x,y))
#    print(fuzz.token_set_ratio(x,y))
#    print(fuzz.token_sort_ratio(x,y))
#    print(fuzz._token_set(x,y))
#    print(fuzz._token_sort(x,y))
#    print(fuzz.partial_token_set_ratio(x,y))
#    print(fuzz.partial_token_sort_ratio(x,y))

#partial_test_vector = np.vectorize(partial_test)





partial_match_vector = np.vectorize(partial_match)                                      #   https://stackoverflow.com/questions/56040817/python-fuzzy-matching-strings-in-list-performance
partial_cenzo_vector = np.vectorize(cenzo)




input = "no i ja się pytam człowieku dumny ty jesteś z siebie zdajesz sobie sprawę z tego co robisz?masz ty wogóle rozum i godnośc człowieka?ja nie wiem ale żałosny typek z ciebie ,chyba nie pomyślałes nawet co robisz i kogo obrażasz ,możesz sobie obrażac tych co na to zasłużyli sobie ale nie naszego papieża polaka naszego rodaka wielką osobę ,i tak wyjątkowa i ważną bo to nie jest ktoś tam taki sobie że możesz go sobie wyśmiać bo tak ci się podoba nie wiem w jakiej ty się wychowałes rodzinie ale chyba ty nie wiem nie rozumiesz co to jest wiara .jeśli myslisz że jestes wspaniały to jestes zwykłym czubkiem którego ktoś nie odizolował jeszcze od społeczeństwa ,nie wiem co w tym jest takie śmieszne ale czepcie się stalina albo hitlera albo innych zwyrodnialców a nie czepiacie się takiej świętej osoby jak papież jan paweł 2 .jak można wogóle publicznie zamieszczac takie zdięcia na forach internetowych?ja się pytam kto powinien za to odpowiedziec bo chyba widac że do koscioła nie chodzi jak jestes nie wiem ateistą albo wierzysz w jakies sekty czy wogóle jestes może ty sługą szatana a nie będziesz z papieża robił takiego ,to ty chyba jestes jakis nie wiem co sie jarasz pomiotami szatana .wez pomyśl sobie ile papież zrobił ,on był kimś a ty kim jestes żeby z niego sobie robić kpiny co? kto dał ci prawo obrażac wogóle papieża naszego ?pomyślałes wogóle nad tym że to nie jest osoba taka sobie że ją wyśmieje i mnie będa wszyscy chwalic? wez dziecko naprawdę jestes jakis psycholek bo w przeciwieństwie do ciebie to papież jest autorytetem dla mnie a ty to nie wiem czyim możesz być autorytetem chyba takich samych jakiś głupków jak ty którzy nie wiedza co to kosciół i religia ,widac że się nie modlisz i nie chodzisz na religie do szkoły ,widac nie szanujesz religii to nie wiem jak chcesz to sobie wez swoje zdięcie wstaw ciekawe czy byś sie odważył .naprawdę wezta się dzieci zastanówcie co wy roicie bo nie macie widac pojęcia o tym kim był papież jan paweł2 jak nie jestescie w pełni rozwinięte umysłowo to się nie zabierajcie za taką osobę jak ojciec swięty bo to świadczy o tym że nie macie chyba w domu krzyża ani jednego obraza świętego nie chodzi tutaj o kosciół mnie ale wogóle ogólnie o zasady wiary żeby mieć jakąs godnosc bo papież nikogo nie obrażał a ty za co go obrażasz co? no powiedz za co obrażasz taką osobę jak ojciec święty ?brak mnie słów ale jakbyś miał pojęcie chociaz i sięgnął po pismo święte i poczytał sobie to może byś się odmienił .nie wiem idz do kościoła bo widac już dawno szatan jest w tobie człowieku ,nie lubisz kościoła to chociaż siedz cicho i nie obrażaj innych ludzi "

output = []
threshold = 75                                                                          #   w jakim procencie musza sie pokrywac by byc ocenzurowane (0-100)
#print(cenzo(input,100))


#print(inputtolist(input))
#print(inputtomatch(input))
dataframecolumn_original = pd.DataFrame(inputtolist(input))
dataframecolumn_original.columns = ['Original']
dataframecolumn_match = pd.DataFrame(inputtomatch(removedup(translatetable(lower(input)))), index = dataframecolumn_original['Original'])
dataframecolumn_match.columns = ['Match']

dataframecolumn_compare = pd.DataFrame(blacklist)
dataframecolumn_compare.columns = ['Compare']                                           #   that was hard ngl
dataframecolumn_compare_trans = dataframecolumn_compare.transpose()

#print(dataframecolumn_match)
#print(dataframecolumn_compare_trans)

score_dataframe = pd.DataFrame(partial_match_vector(dataframecolumn_match, dataframecolumn_compare_trans), columns = dataframecolumn_compare['Compare'] ,index = dataframecolumn_original['Original'])

score_dataframe['Match'] = dataframecolumn_match
score_dataframe['Match_Lenght'] = dataframecolumn_match['Match'].str.len()
score_dataframe['Max_Score'] = score_dataframe.max(axis=1)
score_dataframe['Cenzored']=partial_cenzo_vector(score_dataframe.index, score_dataframe['Match_Lenght'], score_dataframe['Max_Score'])

bad_dataframe = dataframecolumn_match

#print(score_dataframe)
print(score_dataframe.loc[(score_dataframe['Max_Score'] >= threshold)])
output = ''.join(score_dataframe["Cenzored"])
print(output)