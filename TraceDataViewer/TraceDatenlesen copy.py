import matplotlib.pyplot as plt
import datetime as dt
from collections import defaultdict
import csv

kurvenDaten = defaultdict(list)
#SpaltenNamen = defaultdict(list)

""" Datei einlesen und bereinigen"""


def DateiBereinigen(Dateiname, ListName, SplitChar=None, oldChar_1=None,
                    oldChar_2=None, oldChar_3=None, oldChar_4=None, replaceByChar_1=None, replaceByChar_2=None):
    #Name = []
    row = 0
    Spalte_main = []

    AnzahlSpalten = 0
    # Datei mit Spaltenangebe öffnen und in eine Liste eintragen
    with open(Dateiname, 'r') as f:
        File = f.read
        # alle nicht benötigten Zeichen entfernen
        for n in range(len(ListName)):
            text = str(ListName[n])
            for char in text:
                text = text.replace(oldChar_1, replaceByChar_1)
                if not oldChar_2 == None:
                    text = text.replace(oldChar_2, replaceByChar_1)
                if not oldChar_3 == None:
                    text = text.replace(oldChar_3, replaceByChar_1)
            ListName[n] = text

        # Liste nocheinmal bereinigen
        if not replaceByChar_2 == None:
            for n2 in range(len(ListName)):
                for n3 in (ListName):
                    text_2 = str(ListName[n3])
                    for char in text_2:
                        text_2 = text.replace(oldChar_4, replaceByChar_2)
            ListName = text_2

        for zeile in f:
            if row == 0:
                Name = f.readline(0)
                for Spalte in zeile:
                    Spalte_main = Spalte.rsplit('\;')
            if row >= 1:
                for item_2 in zeile:
                    Value = item_2.rsplit('\;')
                    ListName[Spalte_main].append(Value)
            row += 1


def csvDateierstellen():
    pass


"""
def TraceDaten(DateinameTrace):
    with open(DateinameTrace, 'r') as f_kurvenDaten:

        for zeile in (3, f_kurvenDaten):
            datumStr = zeile.split('\ ;')
            ZeitStempel = (dt.datetime.strptime(
                datumStr, '%d.%m.%Y %H:%M:%S:%MS')).timestamp()


            for n in range(1, 74):
                value = []
                value[n] = n.split('\;')
            kurvenDaten[ZeitStempel].append(value)
"""

"""
# als erstes die Datei mit den Spaltennamen bereinigen
DateiBereinigen('EigeneProgramme\TraceDaten\spalten.txt', SpaltenNamen,
                SplitChar='\n,', oldChar_1=' ', oldChar_2='\\n', replaceByChar_1='')

"""
# jetzt die eigenliche TraceDatei bereinigen
DateiBereinigen('EigeneProgramme\TraceDaten\WaageA_TestProd.txt', kurvenDaten,
                SplitChar='\;', oldChar_1=' ', oldChar_2='\\x00', oldChar_3='\\n',
                replaceByChar_1='')

"""

# TraceDaten('EigeneProgramme\TraceDaten\WaageA_TestProd.txt')
with open('EigeneProgramme\TraceDaten\spalten.txt', 'r') as File:
    Inhalt = File.read()

"""
print(kurvenDaten)
print(len(kurvenDaten))

"""
print(SpaltenNamen)
print(len(SpaltenNamen))
print(Inhalt)

csv.register_dialect('myDialect',
                     delimiter=',',
                     quoting=csv.QUOTE_NONE,
                     skipinitialspace=True)

NamenZusatz_1 = '_Test_01'

with open('EigeneProgramme\TraceDaten\TraceDaten' + NamenZusatz_1 + '.csv', 'w') as f1:
    writer_1 = csv.writer(f1)  # , dialect='myDialect')
    writer_1.writerow(SpaltenNamen)
"""

NamenZusatz_2 = '_Test_02'

with open('EigeneProgramme\TraceDaten\TraceDaten' + NamenZusatz_2 + '.csv', 'w') as f2:
    writer_2 = csv.writer(f2)  # , dialect='myDialect')
    for lineWrite in range(len(kurvenDaten)):
        writer_2.writerow(kurvenDaten[lineWrite])

"""
print(SpaltenNamen)
print(len(SpaltenNamen))


print(kurvenDaten)
print(len(kurvenDaten))
"""
