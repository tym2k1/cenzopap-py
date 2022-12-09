import os
import re
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from tkinter import *
import customtkinter

from replacement_dictionary import replacement_dict

root = customtkinter.CTk()
root.geometry("800x600")
root.withdraw()
root.configure(fg_color="#212121")
customtkinter.set_appearance_mode("dark")


with open(os.path.join(os.path.dirname(__file__), 'word_blacklist.txt')) as file:
    #   import words to be censored
    blacklist = set(file.read().split('\n'))
    #blacklistset = set(line.strip() for line in file)                                          #   For large blacklist this option would provide faster bootup
    blacklist.discard('')
    blacklist.discard(' ')



def inputtolist(string):
    #   seperate the words but include the whitespaces for later remerging of the text
    string = re.split(r'(\S+)', string)                                                   #  mozna tez zamienic na lambde
    string1 = []
    string[0 : 1] = [''.join(string[0 : 2])]
    try:
        string.pop(1)
    except:
        return string
    for i in range(0, len(string), 2):
        string1.append(string[i] + string[i+1])                                             #    chcialem uniknac loopow ale tutaj troche zglupialem (moze to sie da zrobic madrym regexem ale nie mam czasu bardziej eksperymentowac)
    return string1

def inputtomatch(string):
    #   find all words without whitespaces+
    string = re.sub(r'[^a-zA-Z\d\s:]', '', string)
    return re.findall(r'\S+', string)



def translatetable(string):
    #    replaces characters imitating letters to letters
    regex = re.compile('|'.join(map(re.escape, replacement_dict)))                      #   https://stackoverflow.com/questions/63230213/translate-table-value-error-valueerror-string-keys-in-translate-table-must-be-o
    return regex.sub(lambda match: replacement_dict[match.group(0)], string)            #   :)

def removedup(string):                                                                  #   usuwanie tych samych literek kolo sb (chuuuuj = chuj)
    #   removes duplicate letters
    return re.sub(r"(.)\1+", r"\1", string)                                             #   mozna zamienic na lambde

def lower(string):
    #   made just for convenience
    return string.lower()

def cenzo(string, match, int):
    #   replaces inner letters in a word with stars if its similarity with blacklist word is greater than treshold
    if int >= threshold and match > 2:
        return re.sub(r'\w', '*', string)
    else:
        return string



def partial_match(x,y):
   #    returns the ratio of similarity between 2 words
    fuzziness = fuzz.QRatio(x,y)
    return fuzziness

def partial_test(x,y):
    #   usefull for debuging
    print(fuzz.ratio(x,y))
    print(fuzz.partial_ratio(x,y))
    print(fuzz.token_set_ratio(x,y))
    print(fuzz.token_sort_ratio(x,y))
    print(fuzz._token_set(x,y))
    print(fuzz._token_sort(x,y))
    print(fuzz.partial_token_set_ratio(x,y))
    print(fuzz.partial_token_sort_ratio(x,y))
    print(fuzz.QRatio(x,y))
    print(fuzz.WRatio(x,y))
    print(fuzz.platform(x,y))

partial_test_vector = np.vectorize(partial_test)

partial_match_vector = np.vectorize(partial_match)                                      #   https://stackoverflow.com/questions/56040817/python-fuzzy-matching-strings-in-list-performance
partial_cenzo_vector = np.vectorize(cenzo)

inDoc = ""
wyjscie = ""

threshold = 70  # w jakim procencie musza sie pokrywac by byc ocenzurowane (0-100)

def funCenz():
    inDoc=inBox.get("1.0", END)
    outBox.delete("1.0", END)

    input = inDoc
    output = []

    dataframecolumn_original = pd.DataFrame(inputtolist(input))
    dataframecolumn_original.columns = ['Original']
    dataframecolumn_match = pd.DataFrame(inputtomatch(removedup(translatetable(lower(input)))),
                                         index=dataframecolumn_original['Original'])
    try:
        dataframecolumn_match.columns = ['Match']
    except:
        return None
    dataframecolumn_compare = pd.DataFrame(blacklist)
    dataframecolumn_compare.columns = ['Compare']
    dataframecolumn_compare_trans = dataframecolumn_compare.transpose()

    global score_dataframe

    score_dataframe = pd.DataFrame(partial_match_vector(dataframecolumn_match, dataframecolumn_compare_trans),
                                   columns=dataframecolumn_compare['Compare'],
                                   index=dataframecolumn_original['Original'])


    combined_dataframe = pd.DataFrame.copy(score_dataframe)
    combined_dataframe['Match'] = dataframecolumn_match

    combined_dataframe['Match_Lenght'] = dataframecolumn_match['Match'].str.len()
    combined_dataframe['Max_Score'] = combined_dataframe.max(axis=1)
    combined_dataframe['Cenzored'] = partial_cenzo_vector(combined_dataframe.index, combined_dataframe['Match_Lenght'], combined_dataframe['Max_Score'])

    print(combined_dataframe.loc[(combined_dataframe['Max_Score'] >= threshold) & (combined_dataframe['Match_Lenght'] > 2)])

    output = ''.join(combined_dataframe["Cenzored"])
    outBox.insert(INSERT, output)
    if plotflag.get() == True: funPlot()


def funPlot():
    plt.close()
    sns.heatmap(score_dataframe, annot=True, xticklabels=True, yticklabels=True, cmap="Blues")
    plt.show()



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


bCenz = customtkinter.CTkButton(master=root, text="c e n z o",
                                bg_color="#323232", fg_color="#14FFEC", text_color="#212121", hover_color="#0D7377", border_width=2, border_color="#323232", font=('Seaford', 20),
                                height=50,
                                width=200,
                                command=funCenz)
bCenz.place(relx=0.5, rely=0.5, anchor=CENTER)

plotflag = BooleanVar()
CPlot = customtkinter.CTkCheckBox(master = root, text = "Calculate Heatmap (might take a while)", variable = plotflag).grid(row=0, sticky=S)

inBox = Text(root, bg="#323232", fg="#14FFEC", font=('Seaford', 14))          #IN
inBox.place(x=50, y=150, width=200, height=300)


outBox = Text(root, bg="#323232", fg="#14FFEC", font=('Seaford', 14))          #OUT
outBox.place(x=550, y=150, width=200, height=300)


root.mainloop()
#GUI-END

