# PYTHON 3
# Author        Alepunx
# Date          26/06/2021
# Rework        18/03/2022


from genericpath import exists
import tkinter as tk
from smartcard.System import readers
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.scard import *
import time
from tkinter.filedialog import asksaveasfile
import os
import json

################################################################################
### SPLASH
################################################################################

print('\n')
print('''
           ███████╗██╗     ███████╗███████╗██████╗ ██╗   ██╗
           ██╔════╝██║     ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝
           ███████╗██║     █████╗  █████╗  ██████╔╝ ╚████╔╝
           ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═══╝   ╚██╔╝
           ███████║███████╗███████╗███████╗██║        ██║
           ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝        ╚═╝   v2.0
''')
time.sleep(2.0)


################################################################################
### OPERAZIONI
################################################################################

SELECT = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]
READ = [0xFF, 0xB0, 0x00] # + indice e lunghezza
WRITE = [0xFF, 0xD0, 0x00] # + indice, lunghezza e bytes
CK_PSC = [0xFF, 0x20, 0x00, 0x00, 0x03] # + psc

################################################################################
### CREDITI
################################################################################

IMPORTO = []
END = ''
#PSC = [115, 68, 189]

CINQUANTA = [36,128,0x44,0x34,0xa9,0x66,0x3a,0xf0,
0x47,0x0f,0xb6,0x57,0x85,0x00,0xc6,0x1f,0x66,0xa6,
0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xb5,0x47,
0xfd,0x50,0xb2,0x34,0x59,0xfc,0x44,0x34,0xa9,0x66,
0x3a,0xf0,0x47,0x0f,0xb6,0x57,0x85,0x00,0xc6,0x1f,
0x66,0xa6,0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,
0xb5,0x47,0xfd,0x50,0xb2,0x34,0x59,0xfc,0x44,0x34,
0xa9,0x66,0x3a,0xf0,0x47,0x0f,0xb6,0x57,0x85,0x00,
0xc6,0x1f,0x66,0xa6,0xc8,0xe9,0x28,0x68,0xb1,0x03,
0x4f,0x2f,0xb5,0x47,0xfd,0x50,0xb2,0x34,0x59,0xfc,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

QUARANTA  = [36,128,0x0e,0xf0,0x65,0x66,0xf0,0x41,
0x75,0x7b,0x6d,0x6f,0x6a,0x44,0x06,0x83,0x6e,0xfe,
0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xe2,0x4c,
0x45,0xd2,0xc4,0x78,0xd9,0x29,0x0e,0xf0,0x65,0x66,
0xf0,0x41,0x75,0x7b,0x6d,0x6f,0x6a,0x44,0x06,0x83,
0x6e,0xfe,0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,
0xe2,0x4c,0x45,0xd2,0xc4,0x78,0xd9,0x29,0x0e,0xf0,
0x65,0x66,0xf0,0x41,0x75,0x7b,0x6d,0x6f,0x6a,0x44,
0x06,0x83,0x6e,0xfe,0xc8,0xe9,0x28,0x68,0xb1,0x03,
0x4f,0x2f,0xe2,0x4c,0x45,0xd2,0xc4,0x78,0xd9,0x29,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

TRENTA    = [36,128,0x37,0x99,0x6E,0xC0,0x4D,0x9B,
0x95,0x99,0xB0,0x41,0xA6,0x56,0xA4,0x41,0x75,0x83,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0xEF,0xFD,
0xA7,0x14,0x9C,0x99,0xCF,0xD2,0x37,0x99,0x6E,0xC0,
0x4D,0x9B,0x95,0x99,0xB0,0x41,0xA6,0x56,0xA4,0x41,
0x75,0x83,0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,
0xEF,0xFD,0xA7,0x14,0x9C,0x99,0xCF,0xD2,0x37,0x99,
0x6E,0xC0,0x4D,0x9B,0x95,0x99,0xB0,0x41,0xA6,0x56,
0xA4,0x41,0x75,0x83,0xC8,0xE9,0x28,0x68,0xB1,0x03,
0x4F,0x2F,0xEF,0xFD,0xA7,0x14,0x9C,0x99,0xCF,0xD2,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

VENTI     = [36,128,0x90,0xD2,0xD4,0xB6,0xA3,0x39,
0x80,0xD0,0x32,0x28,0x8C,0xC5,0xAA,0x67,0xF2,0xDB,
0x7D,0x4A,0x6D,0xA9,0xC2,0x4A,0xBF,0xC1,0x1F,0xE5,
0xB9,0xF8,0xB1,0x4F,0xCF,0xED,0x90,0xD2,0xD4,0xB6,
0xA3,0x39,0x80,0xD0,0x32,0x28,0x8C,0xC5,0xAA,0x67,
0xF2,0xDB,0x7D,0x4A,0x6D,0xA9,0xC2,0x4A,0xBF,0xC1,
0x1F,0xE5,0xB9,0xF8,0xB1,0x4F,0xCF,0xED,0x90,0xD2,
0xD4,0xB6,0xA3,0x39,0x80,0xD0,0x32,0x28,0x8C,0xC5,
0xAA,0x67,0xF2,0xDB,0x7D,0x4A,0x6D,0xA9,0xC2,0x4A,
0xBF,0xC1,0x1F,0xE5,0xB9,0xF8,0xB1,0x4F,0xCF,0xED,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

DIECI     = [36,128,0x13,0x44,0x5D,0x6D,0x7B,0xD8,
0x32,0x8E,0xB5,0x57,0x85,0x00,0xC6,0x1F,0x66,0xA6,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0x59,0xC2,
0x14,0x69,0x78,0xA6,0x8D,0x48,0x13,0x44,0x5D,0x6D,
0x7B,0xD8,0x32,0x8E,0xB5,0x57,0x85,0x00,0xC6,0x1F,
0x66,0xA6,0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,
0x59,0xC2,0x14,0x69,0x78,0xA6,0x8D,0x48,0x13,0x44,
0x5D,0x6D,0x7B,0xD8,0x32,0x8E,0xB5,0x57,0x85,0x00,
0xC6,0x1F,0x66,0xA6,0xC8,0xE9,0x28,0x68,0xB1,0x03,
0x4F,0x2F,0x59,0xC2,0x14,0x69,0x78,0xA6,0x8D,0x48,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]


################################################################################
### COLLEGAMENTO LETTORE
################################################################################

print('\t\t@@@ PROGRAMMA DI RICARICA SLE4442 @@@\n\n')
print('In attesa della SmartCard ..\n')

global con
con = False

def start():
    try:
        r=readers()
        global connection
        connection = r[0].createConnection()
        connection.connect()
        if con == False:
            print('\nCollegamento al lettore ed alla card in corso ..\n')
            print('Lettore ' + str(r).replace('[','').replace(']','').replace("'","") + ' collegato!\n')
    except:
        print('entra qui')
        time.sleep(1.0)
        start()

start()


################################################################################
### CHECK CONNESSIONE CARD
################################################################################

def check():
    global cardtype
    global cardrequest
    global connessione
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=1, cardType=cardtype )
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect(CardConnection.T0_protocol)
    connessione = connection.connect(CardConnection.T0_protocol)
    cardservice.connection.transmit(SELECT, connessione)


################################################################################
### TRASFORMAZIONE PSC
################################################################################
def psw():
    global PSC
    PIN = (str(txt.get()).strip().replace(' ',''))
    if len(PIN) != 6:
        print('ERRORE: Lunghezza PSC errata')
        END = input('Premi INVIO per terminare..')
        start()

    pin = []
    PSC = []
    pin = PIN[:2],PIN[2:4],PIN[4:6]
    for i in pin:
        i = '0x'+i
        i = int(i,16)
        PSC.append(i)


################################################################################
### SCRITTURA
################################################################################

def scrivi():
    global sw1
    global sw2
    global risposta
    print('\nSBLOCCO E SCRITTURA ..\n')
    check()
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect(connessione)
    cardservice.connection.transmit(SELECT, connessione)
    risposta,sw1,sw2 = cardservice.connection.transmit(CK_PSC + PSC, connessione)
    if sw2 == 3:
        print('ERRORE: PSC errata!\nTi rimangono 2 tentativi')
        time.sleep(3.0)
        start()
    elif sw2 == 1:
        print('ERRORE: PSC errata!\nTi rimane 1 tentativo')
        time.sleep(3.0)
        start()
    elif sw2 == 7:
        print('PSC CORRETTA!')
    else:
        print('CARD BLOCCATA, TENTATIVI DI INSERIMENTO PSC ESAURITI!')
        time.sleep(3.0)
        start()

    risposta,sw1,sw2 = cardservice.connection.transmit(WRITE + IMPORTO, connessione)
    if sw2 != 0:
        print('ERRORE: PSC errata!')
        time.sleep(3.0)
        start()

    print('\nVERIFICA DATI ..\n')
    check()
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect(connessione)
    cardservice.connection.transmit(SELECT, connessione)
    risposta,sw1,sw2 = cardservice.connection.transmit(READ + [36, 128], connessione)
    print('\nRICARICA DI ' + OP + ' COMPLETATA!\n')
    time.sleep(2.0)
    print('\nScegli quale operazione vuoi eseguire..\n')
    start()


################################################################################
### FINESTRA TKINTER
################################################################################

def finestra1():
      textwidget = tk.Text()
      for i in CINQUANTA:
          IMPORTO.append(i)
      global OP
      OP = '50€'
      textwidget.quit()
      if len(str(txt.get()).strip().replace(' ','')) != 6:
          print('ERRORE: Lunghezza PSC errata!')
          time.sleep(3.0)
          start()
      elif len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          start()
      else:
        psw()
        scrivi()

def finestra2():
      textwidget = tk.Text()
      for i in QUARANTA:
          IMPORTO.append(i)
      global OP
      OP = '40€'
      textwidget.quit()
      if len(str(txt.get()).strip().replace(' ','')) != 6:
          print('ERRORE: Lunghezza PSC errata!')
          time.sleep(3.0)
          start()
      elif len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          start()
      else:
        psw()
        scrivi()

def finestra3():
      textwidget = tk.Text()
      for i in TRENTA:
          IMPORTO.append(i)
      global OP
      OP = '30€'
      textwidget.quit()
      if len(str(txt.get()).strip().replace(' ','')) != 6:
          print('ERRORE: Lunghezza PSC errata!')
          time.sleep(3.0)
          start()
      elif len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          start()
      else:
        psw()
        scrivi()

def finestra4():
      textwidget = tk.Text()
      for i in VENTI:
          IMPORTO.append(i)
      global OP
      OP = '20€'
      textwidget.quit()
      if len(str(txt.get()).strip().replace(' ','')) != 6:
          print('ERRORE: Lunghezza PSC errata!')
          time.sleep(3.0)
          start()
      elif len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          start()
      else:
        psw()
        scrivi()

def finestra5():
      textwidget = tk.Text()
      for i in DIECI:
          IMPORTO.append(i)
      global OP
      OP = '10€'
      textwidget.quit()
      if len(str(txt.get()).strip().replace(' ','')) != 6:
          print('ERRORE: Lunghezza PSC errata!')
          time.sleep(3.0)
          start()
      elif len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          start()
      else:
        psw()
        scrivi()

def salva():
    global risposta
    path = os.path.dirname(os.path.abspath(__file__))
    obj = path + '\\credits.json'
    if os.path.isfile(obj):
        print ("file trovato\n")
    else:
        print("file inesistente, ne sto creando uno ..\n")
        try:
            f = open(path + "\\credits.json", 'w')
            data = {}
            s = json.dumps(data)
            f.write(s)
            f.close()
        except:
            print('impossibile creare un nuovo file\n\n')
            time.sleep(2.0)
            start()
    try:
        check()
        cardservice = cardrequest.waitforcard()
        cardservice.connection.connect(connessione)
        cardservice.connection.transmit(SELECT, connessione)
        risposta = cardservice.connection.transmit(READ + [36, 128], connessione)
        r = str(risposta)
        nome = input('Dai un nome a questo salvataggio:  ')

        JsonFile = open(path + "\\credits.json")
        f = json.load(JsonFile)
        
        try:
            f[nome] = r[2:-10]
        except:
            print('nome salvataggio già esistente\n')
            time.sleep(2.0)
            start()
        JsonFile.close()

        file = open(path + "\\credits.json", "w")
        json.dump(f, file, indent=3)
        file.close()

        print('\nSalvataggio "'+ nome + '" creato\n')
        time.sleep(2.0)
        print('\n\nScegli quale operazione vuoi eseguire..\n')
        start()
    except:
        print('ERRORE: impossibile aprire o creare il file di salvataggio')
        time.sleep(2.0)
        start()

def carica():
    path = os.path.dirname(os.path.abspath(__file__))
    obj = path + '\\credits.json'
    if os.path.isfile(obj):
        print ("file trovato\n")
    else:
        print("devi prima creare il file dei salvataggi\n")
        time.sleep(2.0)
        start()
    try:
        JsonFile = open(path + "\\credits.json")
        f = json.load(JsonFile)

        print('\nSALVATAGGI:')
        for i in f:
            print(i)
        print('\n')
        p = input('digita il nome del salvataggio da caricare..   ')

        try:
            IMP = f[p]
            IMPORTO = '36, 128, ' + IMP
        except:
            print('hai inserito un nome non valido\n')
            time.sleep(2.0)
            start()
        try:
            scrivi()
        except:
            print('non hai inserito la PSC\n')
            time.sleep(2.0)
            start()
    except:
        print('impossibile aprire il file dei salvataggi\n\n')
        time.sleep(2.0)
        start()

def salvataggi():
    path = os.path.dirname(os.path.abspath(__file__))
    obj = path + '\\credits.json'
    if os.path.isfile(obj):
        print ("file trovato\n")
        try:
            JsonFile = open(path + "\\credits.json")
            f = json.load(JsonFile)

            print('\nSALVATAGGI:')
            for i in f:
                print(i)
            print('\n')
        except:
            print('impossibile aprire il file dei salvataggi\n\n')
            time.sleep(2.0)
            start()
    else:
        print("devi prima creare il file dei salvataggi\n")
        time.sleep(2.0)
        start()
    
    
def info():
    print('''
    #####################################################################
    #######               Software sviluppato da Alepunx              ###
    #######     Test eseguiti con lettore smartcard bit4id/ACR38U     ###
    #######         Ringraziamenti a Faccetta per il supporto         ###
    #######            e l\'hardware di cattura della PSC              ###
    #####################################################################''')
    time.sleep(2.0)
    print('\n\nScegli quale operazione vuoi eseguire..\n')
    start()

con = True    

window = tk.Tk()
window.geometry("330x220")
window.title("SLEEPY v2.0")
window.resizable(False, False)

label = tk.Label(text="Inserisci la PSC ed esegui un'operazione", font=('Helvetica', 10))
label.grid(row=0, column=0, columnspan = 5, pady=10,)

txt = tk.Entry(window,width=50)
txt.grid(row=1, column=0, columnspan = 5, sticky = 'WE', pady=10, padx=10)


button1 = tk.Button(text="50€", fg="green", width = 5, command=finestra1)
button1.grid(row=2, column=0, pady=10,)

button2 = tk.Button(text="40€", fg="green", width = 5, command=finestra2)
button2.grid(row=2, column=1, pady=10,)

button3 = tk.Button(text="30€", fg="green", width = 5, command=finestra3)
button3.grid(row=2, column=2, pady=10,)

button4 = tk.Button(text="20€", fg="green", width = 5, command=finestra4)
button4.grid(row=2, column=3, pady=10,)

button5 = tk.Button(text="10€", fg="green", width = 5, command=finestra5)
button5.grid(row=2, column=4, pady=10,)

button6 = tk.Button(text="Salvataggi", fg="black", width = 14, command=salvataggi)
button6.grid(row=3, column=0, columnspan=2, pady=10,)

button7 = tk.Button(text="Salva Importo", fg="black", width = 14, command=salva)
button7.grid(row=4, column=0, columnspan=2, pady=10,)

button8 = tk.Button(text="Canc. Salvataggio", fg="black", width = 14, command=carica)
button8.grid(row=3, column=2, columnspan=2, pady=10,)

button9 = tk.Button(text="Carica Importo", fg="black", width = 14, command=carica)
button9.grid(row=4, column=2, columnspan=2, pady=10,)

button10 = tk.Button(text="𝓲", fg="red", width = 5, command=info)
button10.grid(row=4, column=4, pady=10,)


if __name__ == "__main__":
    window.mainloop()
