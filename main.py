import os
import re
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
from tkinter import *
import customtkinter

with open(os.path.join(os.path.dirname(__file__), 'word_blacklist1.txt')) as file:
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
   #replaces characters imitating letters to letters
    regex = re.compile('|'.join(map(re.escape, replacement_dict)))                      #   https://stackoverflow.com/questions/63230213/translate-table-value-error-valueerror-string-keys-in-translate-table-must-be-o
    return regex.sub(lambda match: replacement_dict[match.group(0)], string)            #   :)

def removedup(string):                                                                  #   usuwanie tych samych literek kolo sb (chuuuuj = chuj)
    #removes duplicate letters
    return re.sub(r"(.)\1+", r"\1", string)                                             #   mozna zamienic na lambde

def inputtolist(string):
    #find all words separated by characters [a-zA-Z0-9_]+
    return re.findall(r'\w+', string)                                                   #  mozna tez zamienic na lambde

def lower(string):
    return string.lower()



def cenzo(string, int):                                                                      #  cenzurowanie slowek
    #"""replaces inner letters in a word with stars if its similarity with blacklist word is greater than treshold"""
    if int >= threshold:
        return string[0] + '*' * (len(string)-2) + string[-1]
    else:
        return string

def partial_match(x,y):
   #"""returns the ratio of similarity between 2 words"""
    return(fuzz.partial_ratio(x,y))

partial_match_vector = np.vectorize(partial_match)                                      #   https://stackoverflow.com/questions/56040817/python-fuzzy-matching-strings-in-list-performance
partial_cenzo_vector = np.vectorize(cenzo)

global inDoc
inDoc = 1
global wyjscie  #ocenzurowane zdanie

def funCenz():
    inDoc=inBox.get("1.0", END)
    print(inDoc)
    outBox.delete("1.0", END)
    outBox.insert(INSERT, wyjscie)

#Input do GUI
#outBox.input(0,"Wazaaaaaa")
input = inDoc
input = "Hrabia cHujnica z żónął hunją"

output = []
print(inDoc)
#inputlistvar = inputtolist(input)
threshold = 75                                                                          #   w jakim procencie musza sie pokrywac by byc ocenzurowane (0-100)




dataframecolumn_original = pd.DataFrame(inputtolist(input))
dataframecolumn_original.columns = ['Original']
dataframecolumn_match = pd.DataFrame(inputtolist(removedup(translatetable(lower(input)))), index = dataframecolumn_original['Original'])
dataframecolumn_match.columns = ['Match']

dataframecolumn_compare = pd.DataFrame(blacklist)
dataframecolumn_compare.columns = ['Compare']                                           #   that was hard ngl
dataframecolumn_compare_trans = dataframecolumn_compare.transpose()

print(dataframecolumn_match)
print(dataframecolumn_compare_trans)

score_dataframe = pd.DataFrame(partial_match_vector(dataframecolumn_match, dataframecolumn_compare_trans), columns = dataframecolumn_compare['Compare'] ,index = dataframecolumn_original['Original'])

score_dataframe['Match'] = dataframecolumn_match
score_dataframe['Max_Score'] = score_dataframe.max(axis=1)
score_dataframe['Cenzored']=partial_cenzo_vector(score_dataframe.index, score_dataframe['Max_Score'])

print(score_dataframe)

print(score_dataframe['Cenzored'])

wyjscie = "555"
#outBox.insert(0, "Wazaaaaaa")


#GUI
root = customtkinter.CTk()
root.geometry("800x600")
root.configure(fg_color="#212121")
customtkinter.set_appearance_mode("dark")

frame = customtkinter.CTkFrame(master=root,
                               width=750,
                               height=525,
                               corner_radius=10)
frame.place(x=25, y=25)


bCenz = customtkinter.CTkButton(master=root, text="Cenzuruj",
                                bg_color="#323232", fg_color="#14FFEC", text_color="#212121", hover_color="#0D7377", border_width=2, border_color="#323232", font=('Seaford', 20),
                                height=50,
                                width=200,
                                command=funCenz)
bCenz.place(relx=0.5, rely=0.5, anchor=CENTER)

#inBox = customtkinter.CTkEntry(master=root,
#                               placeholder_text="Input",
#                               width=400,
#                               height=40,
#                               border_width=2,
#                               corner_radius=10,
#                               text_color="#14FFEC",
#                               font=('Seaford', 20))
#inBox.place(relx=0.5, rely=0.25, anchor=CENTER)

inBox = Text(root, bg="#323232", fg="#14FFEC", font=('Seaford', 14))          #IN
inBox.place(x=50, y=150, width=200, height=300)


#inBox.configure()

#outBox = customtkinter.CTkEntry(master=root,
#                               placeholder_text="Output",
#                               width=400,
#                               height=40,
#                               border_width=2,
#                               corner_radius=10,
#                               text_color="#14FFEC",
#                                font=('Seaford', 20)) #state="disabled"
#outBox.place(relx=0.5, rely=0.75, anchor=CENTER)

outBox = Text(root, bg="#323232", fg="#14FFEC", font=('Seaford', 14))          #OUT
outBox.place(x=550, y=150, width=200, height=300)


root.mainloop()
#GUI-END
