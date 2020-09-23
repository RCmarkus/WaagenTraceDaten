"""
Version: V1.1
    Programm um TraceDaten von der SIEMENS SIWAREX FTA auszuwerten
    als erstes wird eine .txt eingelesen

20.09.2019
copyright Markus Rychlik ©2020
"""

import sys
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd
import datetime as dt
from collections import defaultdict
import csv
import numpy as np
from tkinter import messagebox as msgBox

kurvenDaten = defaultdict(list)


# --------------Datei einlesen und bereinigen--------------


def DateiBereinigen(PathName, FileName, Dict_Name, removeChar=None, replaceByChar=None, removeEmptyLine=None):
    """Mit dieser Funktion wird die Datei eingelesen und bestimmte Zeichen entfernt

    Parameters
    ----------
    PathName : string\n
        Path zur der Datei die geöffnet werden soll\n
    FileName : string\n
        Dateiname von der Datei die geöffnet werden soll\n
    Dict_Name : dict\n
        Dictionary hier werden die bereinigten Daten gespeichert\n
    removeChar : string, optional\n
        die Zeichenfolge die entfernt werden soll, by default None\n
    replaceByChar : string, optional\n
        mit diesem Zeichen soll ersetzt werden, by default None\n
    removeEmptyLine : string, optional\n
        mit diesen Zeichen sind leere Zeilen gekennzeichnet, by default None\n
    """
    # """
    # Mit dieser Function wird die Datei eingelesen und bestimmte
    # Zeichen entfernt.\n
    # 'Dateiname' = die Datei die geöffnet werden soll\n
    # 'Dict_Name' = Dictionary hier werden die bereinigeten Daten geschrieben\n
    # 'removeChat' = 1.Zeichen das entfernt werden sollen\n
    # 'replaceByChar' = mit diesem Zeichen soll das zu entferne Zeichen ersetzt werden\n
    # 'removeEmptyLine' = wie sind leere Zeilen gekenntzeichnet\n
    # """
    ListName = []
    Spalte_main = []
    Dateiname = PathName + FileName
    # Datei öffnen und alle nicht benötigten Zeichen entfernen
    try:
        with open(Dateiname, 'r') as txt_File:
            for line in txt_File:
                # alle nicht benötigten Zeichen entfernen
                textStr = line.replace(removeChar, replaceByChar)
                ListName.append(textStr)
    except:
        msgBox.showerror(
            "WARNING", "not possible to open File\n" + FileNameStr)
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
    """Zeiststempel auslesen

    Args:\n
    \n
        Dict_Name {(string)}: Dictionary aus dem gelesen werden soll\n
        KeyString {(string)}: um den Zeitstempel im Dictionary zu finden\n
        timeList {(list)}: das Ergebnis in eine Liste eintragen\n
    """
    # '''
    # Zeiststempel auslesen\n
    # 'Dict_Name' = Dictionary aus dem gelesen werden soll\n
    # 'KeyString' = um den Zeitstempel im Dictionary zu finden\n
    # 'timeList' = das Ergebnis in eine Liste eintragen\n
    # '''
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
            millisek = int(microsek)//100
            millisek = str(millisek)
            timeList.append(Liste[0] + '.' + millisek)
        except:  # Sonderfall bei 0000 Microsekunden
            timeList.append(Liste[0] + '.00')


def werteAuslesen(Dict_Name, KeyString, ValueList, isSignalStatus=('No', 'Yes')):
    """Werte auslesen

    Arguments: \n
        Dict_Name {dict} -- Dictionary aus dem die Werte gelesen werden sollen\n
        KeyString {string} -- um den Zeitstempel im Dictionary zu fenden\n
        ValueList {list} -- die Ergebnise in eine Liste eintragen\n

    Keyword Arguments:\n
        isSignalStatus {tuple} -- Messwert oder Signal\n
                                    No = Werte werden als float-Werte zurück gegeben\n
                                    Yes = Werte sind binär und werden für den Graph entsprechend skaliert\n
                                    '0' = 0  und '1' = 25 (default: {('No', 'Yes')})\n
    """
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


#
# ---------------------- Path und Dateinamen festlegen ---------------------------------
#

PathNameStr = 'TraceDataViewer\\TraceDaten\\'  # nur zum Test in Python
# PathNameStr = 'TraceDaten\\' #für die .exe Datei
FileNameStr = 'WaageA_TraceData.txt'
#FileNameStr = 'WaageA_TestProd.txt'
# jetzt die eigenliche TraceDatei bereinigen
DateiBereinigen(PathNameStr, FileNameStr, kurvenDaten,
                removeChar='\x00', replaceByChar='', removeEmptyLine='\n')


#
# ---------------------- Kurven auswerten und anlegen ----------------------------------
#

# Listen für Kurven anlegen
Zeitstempel = []
Nettogewicht = []
Nettoprozessgewicht = []
Grobabschaltpunkt = []
Feinabschaltpunkt = []
Entleersignal = []
Grobsignal = []
Feinsignal = []
WartenAufStillstand = []
gefilterter_Digitwert = []
ungefilterterADC_Wert = []


# Zeitstempel auslesen
ZeitstempelAuslesen(kurvenDaten, 'Zeitstempel', Zeitstempel)

werteAuslesen(kurvenDaten, 'Nettoprozessgewicht',
              Nettogewicht, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'Grobabschaltpunkt',
              Grobabschaltpunkt, isSignalStatus='No')

werteAuslesen(kurvenDaten, 'Feinabschaltpunkt',
              Feinabschaltpunkt, isSignalStatus='No')

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
    timeTick += 1


fig, ax1 = plt.subplots()
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.10)
ax1.plot(timeLine, Nettogewicht,
         lw=0.5, label='Nettogewicht', color='red')

# Einstellungen für x/y-Achsen
ax1.set_xticks(np.arange(0, timeLine[-1], 250))
ax1.set_ylim([-2, 30])
ax1.minorticks_on()
cursor = Cursor(ax1, useblit=True, color='k', linewidth=1)

for tick in ax1.get_xticklabels():
    tick.set_rotation(75)

# Weiter Kurven hinzufügen
ax1.plot(timeLine, Nettoprozessgewicht,
         lw=0.5, label='Nettoprozessgewicht', color='purple')

ax1.plot(timeLine, Grobabschaltpunkt,
         lw=0.5, label='Grobabschaltpunkt', color='orange')

ax1.plot(timeLine, Feinabschaltpunkt,
         lw=0.5, label='Feinabschaltpunkt', color='brown')

ax1.plot(timeLine, Entleersignal,
         lw=0.5, label='Entleersignal', color='blue')

ax1.plot(timeLine, Grobsignal,
         lw=0.5, label='Grobsignal', color='green')

ax1.plot(timeLine, Feinsignal,
         lw=0.5, label='Feinsignal', color='black')

ax1.plot(timeLine, WartenAufStillstand,
         lw=0.5, label='WartenAufStillstand', color='yellow')


# Legende oben rechts anzeigen
plt.legend(loc='upper right', borderaxespad=0.)

# Plot beschriften
plt.grid(linestyle='-.', linewidth='0.25', color='green')
plt.title('SIWAREX Trace Daten Viewer', fontstyle='italic', fontsize='large')
plt.xlabel('Zeit in [ms]')
plt.ylabel('Gewicht in [kg]')
plt.yticks(np.arange(0, 32, step=5))

# Alles anzeigen
plt.show()


# csv Datei anlegen und alle Werte speichern

'''
NamenZusatz_2 = '_cleanFile_01'
FileNameStr_csv = 'TraceDaten' + NamenZusatz_2 + '.csv'

with open(PathNameStr + FileNameStr_csv, 'w') as f2:
    for key in kurvenDaten.keys():
        f2.write("%s,%s\n" % (key, kurvenDaten[key]))
'''
