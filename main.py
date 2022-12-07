import os
import re
import tkinter


with open(os.path.join(os.path.dirname(__file__), 'word_blacklist.txt')) as file:       #word_blacklist.txt  key_words.txt
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



#GUI

root = tkinter.Tk()
root.title = "Wielka Polska Cenzura"
root.configure(bg ="#242424")
l = tkinter.Label(root, text='Cenzura', font=("BROADWAY", 40), bg="#242424", fg="#1CF020")
l.place(x=250, y=20, width=300, height=80)


def funPrzycisk():
    #wpis.delete(0, END)


#ENTRY BOX
    #print(txbox.get("1.0", tkinter.END))
    global wpisIn
   # wpisIn = wpis.get()
    in1 = txbox.get("1.0", tkinter.END)
    out1 = []
    for i in inputtolist(in1):
        out1.append(cenzo(i))
    toutBox.delete("1.0", tkinter.END)
    toutBox.insert(tkinter.INSERT, out1)



b = tkinter.Button(root, text='Ocenzuruj', width=10, bg='#4D4D4D', fg='white', font=20, command = funPrzycisk)
b.place(x=350, y=500, width=100, height=40)

#wpis = tkinter.Entry(root, width=50)                        #tu wpisujemy rzeczy
#wpis.place(x=450, y=200, width=200, height=300)

#otput = tkinter.Entry(root, width=50)                       #wynik jest wypisywany
#otput.pack()

#Textbox
txbox = tkinter.Text(root, bg="#4D4D4D")          #IN
txbox.place(x=150, y=150, width=200, height=300)

toutBox = tkinter.Text(root, bg="#4D4D4D")
toutBox.place(x=450, y=150, width=200, height=300)

# wpis.insert(0, "Wpisz tekst do ocenzurowania")            #co sie na poczatku wyswietla w Input Panelu

root.geometry('800x600')
root.mainloop()


#GUI END


#in1 = "test dupa chuj gowno gówno pizda ogień jebać politechnikę gównianą pierdolic pięrdołić"
#in1 = wpisIn
#out1 = []
#for i in inputtolist(in1):
#    out1.append(cenzo(i))
#print(out1)


