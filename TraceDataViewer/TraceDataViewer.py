"""
Version: V1.0
    Programm um TraceDaten von der SIEMENS SIWAREX FTA auszuwerten
    als erstes wird eine .txt eingelesen

20.09.2019
copyright Markus Rychlik ©2019
"""
import sys
from matplotlib import pyplot as plt
import pandas as pd
import datetime as dt
from collections import defaultdict
import csv
import numpy as np
from tkinter import messagebox as msgBox 

kurvenDaten = defaultdict(list)


# --------------Datei einlesen und bereinigen--------------


def DateiBereinigen(PathName, FileName, Dict_Name, removeChar=None, replaceByChar=None, removeEmptyLine=None):
    """
    Mit dieser Function wird die Datei eingelesen und bestimmte 
    Zeichen entfernt.\n
    'Dateiname' = die Datei die geöffnet werden soll\n
    'Dict_Name' = Dictionary hier werden die bereinigeten Daten geschrieben\n
    'removeChat' = 1.Zeichen das entfernt werden sollen\n
    'replaceByChar' = mit diesem Zeichen soll das zu entferne Zeichen ersetzt werden\n
    'removeEmptyLine' = wie sind leere Zeilen gekenntzeichnet\n
    """
    ListName = []
    Spalte_main = []
    Dateiname = PathName + FileName
    # Datei öffnen und alle nicht benötigten Zeichen entfernen
    try:
        with open(Dateiname, 'r') as txt_File:
            for n in txt_File:
                # alle nicht benötigten Zeichen entfernen
                textStr = n.replace(removeChar, replaceByChar)
                ListName.append(textStr)
    except:
        msgBox.showerror("WARNING","not possible to open File\n" + FileNameStr)
        sys.exit()




    # aus einer Liste ein dictionary schreiben
    row = 0
    for zeile in ListName:
        test = zeile
        zeile = ListName[row].split('\;')

        # in der ersten Zeile sind die Spaltennamen
        if row == 0:
            Spalte_main = test.split(';')

        # alle nicht benötigen Zeilen entfernen und Werte ins dictionary eintragen
        if row >= 1 and not test == removeEmptyLine:
            Value = test.split(';')
            y = 0
            for x in Value:
                Dict_Name[Spalte_main[y]].append(x)
                y += 1
        row += 1


def csvDateierstellen():
    pass


def ZeitstempelAuslesen(Dict_Name, KeyString, timeList):
    '''
    Zeiststempel auslesen\n
    'Dict_Name' = Dictionary aus dem gelesen werden soll\n
    'KeyString' = um den Zeitstempel im Dictionary zu finden\n
    'timeList' = das Ergebnis in eine Liste eintragen\n
    '''
    DictStringValues = []
    DictStringValues.append(Dict_Name[KeyString])
    ValueString = DictStringValues[0]
    for n in ValueString:
        datumStr = n
        if datumStr == '':
            break
        timeStp = (dt.datetime.strptime(
            datumStr, '%d.%m.%y %H:%M:%S %f %a')).time()
        # print(timeStp)
        timeStp = str(timeStp)
        Liste = timeStp.split('.')
        try:
            microsek = Liste[1]
            millisek = int(microsek)//1000
            millisek = str(millisek)
            timeList.append(Liste[0] + '.' + millisek)
        except:  # Sonderfall bei 0000 Microsekunden
            timeList.append(Liste[0] + '.000')


def werteAuslesen(Dict_Name, KeyString, ValueList, isSignalStatus=('No', 'Yes')):
    '''
    Werte Auslesen\n

    'Dict_Name' = Dictionary aus dem gelesen werden soll\n
    'KeyString' = um den Zeitstempel im Dictionary zu finden\n
    'ValueList' = das Ergebnis in eine Liste eintragen\n
    'isSignalStatus' = No/Yes\n
            No = Werte werden als float-Werte zurückgegeben\n
            Yes = Werte sind binär und werden entsprechend skaliert '0'=0 und '1'=25\n
    '''
    DictStringValues = []
    DictStringValues.append(Dict_Name[KeyString])
    ValueString = DictStringValues[0]
    if isSignalStatus == 'No':
        for n in ValueString:
            ValueStr = n
            if ValueStr == '':
                break
            ValueStr = float(ValueStr)
            ValueList.append(ValueStr)
    if isSignalStatus == 'Yes':
        for n in ValueString:
            ValueStr = n
            if ValueStr == '':
                break
            if ValueStr == '1':
                ValueList.append(25)
            else:
                ValueList.append(0)


"""
# als erstes die Datei mit den Spaltennamen bereinigen
DateiBereinigen('EigeneProgramme\TraceDaten\spalten.txt', SpaltenNamen,
                SplitChar='\n,', oldChar_1=' ', oldChar_2='\\n', replaceByChar_1='')

"""
PathNameStr = 'TraceDataViewer\\TraceDaten\\'
FileNameStr = 'WaageA_nonSlip_03.txt'
# jetzt die eigenliche TraceDatei bereinigen
DateiBereinigen(PathNameStr, FileNameStr, kurvenDaten,
                removeChar='\x00', replaceByChar='', removeEmptyLine='\n')


Zeitstempel = []
Nettogewicht = []
Grobabschaltpunkt = []
Entleersignal = []
gefilterter_Digitwert = []
ungefilterterADC_Wert = []
Grobsignal = []
Feinsignal = []
WartenAufStillstand = []
Nettoprozessgewicht=[]


ZeitstempelAuslesen(kurvenDaten, 'Zeitstempel', Zeitstempel)

werteAuslesen(kurvenDaten, 'Nettoprozessgewicht',
              Nettogewicht, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'Grobabschaltpunkt',
              Grobabschaltpunkt, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'gefilterter Digitwert',
              gefilterter_Digitwert, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'ungefilterter ADC Wert',
              ungefilterterADC_Wert, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'Nettoprozessgewicht',
              Nettoprozessgewicht, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'Entleersignal',
              Entleersignal, isSignalStatus='Yes')

werteAuslesen(kurvenDaten, 'Grobsignal',
              Grobsignal, isSignalStatus='Yes')

werteAuslesen(kurvenDaten, 'Feinsignal',
              Feinsignal, isSignalStatus='Yes')

werteAuslesen(kurvenDaten, 'Warten auf Stillstand',
              WartenAufStillstand, isSignalStatus='Yes')


maxLengthTimeStp = len(Zeitstempel)
timeLine = []
timeTick = 0
for n in range(maxLengthTimeStp):
    timeLine.append(timeTick)
    timeTick += 10

sampel_time = pd.DataFrame(Zeitstempel)
sampel_time
#lastTimeTick = int(timeLine)

fig, ax1 = plt.subplots()
ax2 = ax1.twiny()
ax3 = ax1.twiny()
ax4 = ax1.twiny()
ax5 = ax1.twiny()
ax6 = ax1.twiny()
ax7 = ax1.twiny()

ax1.plot(timeLine, Nettogewicht,
         lw=0.5, label='Nettogewicht', color='red')
ax1.set_xticks(np.arange(0, timeLine[-1], 1000))
ax1.set_ylim([-2, 30])
for tick in ax1.get_xticklabels():
    tick.set_rotation(45)

ax2.plot(Entleersignal,
         lw=0.5, label='Entleersignal', color='blue')

ax3.plot(Grobsignal,
         lw=0.5, label='Grobsignal', color='green')

ax4.plot(Feinsignal,
         lw=0.5, label='Feinsignal', color='black')

ax5.plot(WartenAufStillstand,
         lw=0.5, label='WartenAufStillstand', color='yellow')

ax6.plot(Grobabschaltpunkt,
         lw=0.5, label='Grobabschaltpunkt', color='orange')

ax7.plot(Nettoprozessgewicht,
         lw=0.5, label='Nettoprozessgewicht', color='purple')
#ax2.set_ylim([0, 1])
#ax2.set_yticks([0, 1])

#ax2.set_xticks(np.arange(0, maxLengthTimeStp, 250))


plt.legend()


plt.grid(linestyle='-.', linewidth='0.25', color='green')
plt.yticks([0, 25, 30])
plt.show()


# csv Datei anlegen und alle Werte speichern
''' 
NamenZusatz_2 = '_cleanFile_01'

with open('LearnPaython_Class\EigeneProgramme\TraceDaten\TraceDaten' + NamenZusatz_2 + '.csv', 'w') as f2:
    for key in kurvenDaten.keys():
        f2.write("%s,%s\n" % (key, kurvenDaten[key]))
 '''
