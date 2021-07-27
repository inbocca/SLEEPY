# PYTHON 3!!
# Author        Alepunx
# Date          15/06/2021
#
# first working draft

import tkinter as tk
from smartcard.System import readers
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.scard import *
import smartcard.util
import time
import sys

################################################################################
### INTRO
################################################################################

print('''
#####################################################################
#######               Software sviluppato da Alepunx              ###
#######     Test eseguiti con lettore smartcard bit4id/ACR38U     ###
#######         Ringraziamenti a Faccetta per il supporto         ###
#######            e l\'hardware di cattura della PSC              ###
#####################################################################''')
time.sleep(2.5)
print('\n')
print('''
           ███████╗██╗     ███████╗███████╗██████╗ ██╗   ██╗
           ██╔════╝██║     ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝
           ███████╗██║     █████╗  █████╗  ██████╔╝ ╚████╔╝
           ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═══╝   ╚██╔╝
           ███████║███████╗███████╗███████╗██║        ██║
           ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝        ╚═╝   v1.3
''')
time.sleep(1.0)


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
0x66,0xa6,0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xb5,0x47,
0xfd,0x50,0xb2,0x34,0x59,0xfc,0x44,0x34,0xa9,0x66,0x3a,0xf0,
0x47,0x0f,0xb6,0x57,0x85,0x00,0xc6,0x1f,0x66,0xa6,
0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xb5,0x47,
0xfd,0x50,0xb2,0x34,0x59,0xfc,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

QUARANTA  = [36,128,0x0e,0xf0,0x65,0x66,0xf0,0x41,
0x75,0x7b,0x6d,0x6f,0x6a,0x44,0x06,0x83,0x6e,0xfe,
0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xe2,0x4c,
0x45,0xd2,0xc4,0x78,0xd9,0x29,0x0e,0xf0,0x65,0x66,0xf0,0x41,
0x75,0x7b,0x6d,0x6f,0x6a,0x44,0x06,0x83,0x6e,0xfe,
0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xe2,0x4c,
0x45,0xd2,0xc4,0x78,0xd9,0x29,0x0e,0xf0,0x65,0x66,0xf0,0x41,
0x75,0x7b,0x6d,0x6f,0x6a,0x44,0x06,0x83,0x6e,0xfe,
0xc8,0xe9,0x28,0x68,0xb1,0x03,0x4f,0x2f,0xe2,0x4c,
0x45,0xd2,0xc4,0x78,0xd9,0x29,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

TRENTA    = [36,128,0x37,0x99,0x6E,0xC0,0x4D,0x9B,
0x95,0x99,0xB0,0x41,0xA6,0x56,0xA4,0x41,0x75,0x83,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0xEF,0xFD,
0xA7,0x14,0x9C,0x99,0xCF,0xD2,0x37,0x99,0x6E,0xC0,0x4D,0x9B,
0x95,0x99,0xB0,0x41,0xA6,0x56,0xA4,0x41,0x75,0x83,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0xEF,0xFD,
0xA7,0x14,0x9C,0x99,0xCF,0xD2,0x37,0x99,0x6E,0xC0,0x4D,0x9B,
0x95,0x99,0xB0,0x41,0xA6,0x56,0xA4,0x41,0x75,0x83,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0xEF,0xFD,
0xA7,0x14,0x9C,0x99,0xCF,0xD2,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

VENTI     = [36,128,0x90,0xD2,0xD4,0xB6,0xA3,0x39,
0x80,0xD0,0x32,0x28,0x8C,0xC5,0xAA,0x67,0xF2,0xDB,
0x7D,0x4A,0x6D,0xA9,0xC2,0x4A,0xBF,0xC1,0x1F,0xE5,
0xB9,0xF8,0xB1,0x4F,0xCF,0xED,0x90,0xD2,0xD4,0xB6,0xA3,0x39,
0x80,0xD0,0x32,0x28,0x8C,0xC5,0xAA,0x67,0xF2,0xDB,
0x7D,0x4A,0x6D,0xA9,0xC2,0x4A,0xBF,0xC1,0x1F,0xE5,
0xB9,0xF8,0xB1,0x4F,0xCF,0xED,0x90,0xD2,0xD4,0xB6,0xA3,0x39,
0x80,0xD0,0x32,0x28,0x8C,0xC5,0xAA,0x67,0xF2,0xDB,
0x7D,0x4A,0x6D,0xA9,0xC2,0x4A,0xBF,0xC1,0x1F,0xE5,
0xB9,0xF8,0xB1,0x4F,0xCF,0xED,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]

DIECI     = [36,128,0x13,0x44,0x5D,0x6D,0x7B,0xD8,
0x32,0x8E,0xB5,0x57,0x85,0x00,0xC6,0x1F,0x66,0xA6,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0x59,0xC2,
0x14,0x69,0x78,0xA6,0x8D,0x48,0x13,0x44,0x5D,0x6D,0x7B,0xD8,
0x32,0x8E,0xB5,0x57,0x85,0x00,0xC6,0x1F,0x66,0xA6,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0x59,0xC2,
0x14,0x69,0x78,0xA6,0x8D,0x48,0x13,0x44,0x5D,0x6D,0x7B,0xD8,
0x32,0x8E,0xB5,0x57,0x85,0x00,0xC6,0x1F,0x66,0xA6,
0xC8,0xE9,0x28,0x68,0xB1,0x03,0x4F,0x2F,0x59,0xC2,
0x14,0x69,0x78,0xA6,0x8D,0x48,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
0xff,0xff]


################################################################################
### COLLEGAMENTO LETTORE
################################################################################

print('\t\t@@@ PROGRAMMA RICARICA SLE4442 @@@\n\n')
print('Lettori testati:\n- Bit4id\n- ACR38U\n- ACR39U\n')
print('Ricerca lettore SmartCard ..\n')
try:
    r=readers()
    print('Lettore trovato: ' + str(r).replace('[','').replace(']',''))
    print('\nCollegamento al lettore ed alla card in corso ..\n')
except:
    print('ERRORE: Nessun lettore trovato')
    END = input('Premi INVIO per terminare..')
    sys.exit("")
try:
    connection = r[0].createConnection()
    connection.connect()
    print('Lettore ' + str(r).replace('[','').replace(']','') + ' collegato!\n')
except:
    print('ERROE: Impossibile stabilire connessione con il lettore')
    END = input('Premi INVIO per terminare..')
    sys.exit("")

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
          sys.exit("")
      if len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          sys.exit("")

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
          sys.exit("")
      if len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          sys.exit("")

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
          sys.exit("")
      if len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          sys.exit("")

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
          sys.exit("")
      if len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          sys.exit("")

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
          sys.exit("")
      if len(str(txt.get()).strip().replace(' ','')) == 0:
          print('ERRORE: Non hai inserito la PSC')
          time.sleep(3.0)
          sys.exit("")

window = tk.Tk()
window.geometry("330x200")
window.title("SLEEPY")

label = tk.Label(text="Inserisci la PSC e premi sul credito da caricare", font=('Helvetica', 10))
label.grid(row=0, column=0, columnspan = 5, pady=10,)

txt = tk.Entry(window,width=50)
txt.grid(column=0, row=1, columnspan = 5, sticky = 'WE', pady=10, padx=10)

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


if __name__ == "__main__":
    window.mainloop()

PIN = (str(txt.get()).strip().replace(' ',''))
if len(PIN) != 6:
      print('ERRORE: Lunghezza PSC errata')
      END = input('Premi INVIO per terminare..')
      sys.exit("")

################################################################################
### CHECK CONNESSIONE CARD
################################################################################

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=1, cardType=cardtype )
cardservice = cardrequest.waitforcard()
cardservice.connection.connect(CardConnection.T0_protocol)
connessione = connection.connect(CardConnection.T0_protocol)
cardservice.connection.transmit(SELECT, connessione)


################################################################################
### TRASFORMAZIONE PSC
################################################################################

pin = []
PSC = []
pin = PIN[:2],PIN[2:4],PIN[4:6]
for i in pin:
    i = '0x'+i
    i = int(i,16)
    PSC.append(i)


################################################################################
### CICLO LETTURA/SCRITTURA/RILETTURA
################################################################################

print('\nLETTURA ..')
cardservice = cardrequest.waitforcard()
cardservice.connection.connect(connessione)
cardservice.connection.transmit(SELECT, connessione)
risposta,sw1,sw2 = cardservice.connection.transmit(READ + [36, 128], connessione)

print('\nSBLOCCO E SCRITTURA ..')
cardservice = cardrequest.waitforcard()
cardservice.connection.connect(connessione)
cardservice.connection.transmit(SELECT, connessione)
risposta,sw1,sw2 = cardservice.connection.transmit(CK_PSC + PSC, connessione)
risposta,sw1,sw2 = cardservice.connection.transmit(WRITE + IMPORTO, connessione)
test = (sw2)
#print(test)

if test != 0:
    print('ERRORE: PSC errata!')
    time.sleep(3.0)
    sys.exit("")

print('\nVERIFICA DATI ..\n')
cardservice = cardrequest.waitforcard()
cardservice.connection.connect(connessione)
cardservice.connection.transmit(SELECT, connessione)
risposta,sw1,sw2 = cardservice.connection.transmit(READ + [36, 128], connessione)
print('\nRICARICA DI ' + OP + ' COMPLETATA!\n')
time.sleep(2.0)
sys.exit("")
