import os
import re
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from replacement_dictionary import replacement_dict



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
    string.pop(1)
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
    if int >= threshold: #and match > 2:
        return re.sub(r'\w', '*', string)
    else:
        return string



def partial_match(x,y):
   #    returns the ratio of similarity between 2 words
    #fuzziness = fuzz.token_set_ratio(x,y)
    fuzziness = fuzz.QRatio(x,y)
    #if fuzziness >= threshold:
    #    debugls.append([x,y])
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




input = "Nie mam już siły do tej kurwy. Drukarka HP nie drukuje Nie mam już siły do tej kurwy. Drukarka HP nie drukuje Nie mam już siły do tej kurwy. Drukarka HP nie drukujeNie mam już siły do tej kurwy. Drukarka HP nie drukuje"
output = []
threshold = 70                                                                           #   w jakim procencie musza sie pokrywac by byc ocenzurowane (0-100)

dataframecolumn_original = pd.DataFrame(inputtolist(input))
dataframecolumn_original.columns = ['Original']
dataframecolumn_match = pd.DataFrame(inputtomatch(removedup(translatetable(lower(input)))), index = dataframecolumn_original['Original'])
dataframecolumn_match.columns = ['Match']

dataframecolumn_compare = pd.DataFrame(blacklist)
dataframecolumn_compare.columns = ['Compare']
dataframecolumn_compare_trans = dataframecolumn_compare.transpose()

#print(dataframecolumn_match)
#print(dataframecolumn_compare_trans)

score_dataframe = pd.DataFrame(partial_match_vector(dataframecolumn_match, dataframecolumn_compare_trans), columns = dataframecolumn_compare['Compare'] ,index = dataframecolumn_original['Original'])

print(score_dataframe)

#na to checkbox

combined_dataframe = pd.DataFrame.copy(score_dataframe)
combined_dataframe['Match'] = dataframecolumn_match



combined_dataframe['Match_Lenght'] = dataframecolumn_match['Match'].str.len()
combined_dataframe['Max_Score'] = combined_dataframe.max(axis=1)
combined_dataframe['Cenzored']=partial_cenzo_vector(combined_dataframe.index, combined_dataframe['Match_Lenght'], combined_dataframe['Max_Score'])

#print(combined_dataframe)
#print(combined_dataframe.loc[(combined_dataframe['Max_Score'] >= threshold)])

output = ''.join(combined_dataframe["Cenzored"])
print(output)
print(combined_dataframe)

plt.close()
sns.heatmap(score_dataframe, annot=True, xticklabels=True, yticklabels=True, cmap="Blues")
plt.show()