#!/usr/bin/env python3

# CHECKHASHGUI - Calculates the checksum of file and compares it with user input.
# Version: 0.2

# Copyright (c) 2012-2014 Per Tunedal, Stockholm, Sweden
# Author: Per Tunedal <info@tunedal.nu>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Changes:
# 0.1
# GUI for checking hashes of files.

# 0.2
# Added handling of exceptions e.g. file not found.
# Added handling of errors in input.
# Fixed problems with unicode characters in text and file names
# NB Always save this file as unicode (UTF-8).
# Minor improvements. Cleaning of code and comments.


import sys, hashlib, time
#import sys, hashlib, string, time
from tkinter import *
import tkinter.filedialog
import webbrowser

root = Tk()

root.title("CHECK HASH")

c0 = Label(root, text="Check the HASH of a file", font="georgia 16 bold")
c0.grid(row=0, column=0, columnspan=3)

c1 = Label(root, text="Please enter the FILENAME (full path): ")
c1.grid(row=1, column=0, sticky=E)

InputString1 = StringVar()
Entry(root, width=30, textvariable=InputString1).grid(row=1, column=1, columnspan=3, sticky=W)

# wrap=word breaks too long lines after a word, not a character.
textw = Text(root, wrap="word")
textw.insert(INSERT, "Please enter the hash here ...")
textw.grid(row=2, columnspan=4)


def GetString():
    # Browse button
    Button(root, text=' Browse ... ', command=browse).grid(row=1, column=2, sticky=E)
    Button(root, text=' Help ', command=help).grid(row=0, column=3, sticky=E)
    Button(root, text='About', command=about).grid(row=1, column=3, sticky=E)
    Button(root, text='Clear', command=ClearText).grid(row=3, column=0, sticky=W)
    Button(root, text='Check', fg="white", bg="blue", command=Check).grid(row=3, column=1, sticky=W)
    Button(root, text='QUIT', command=quit).grid(row=3, column=3, sticky=E)
    root.mainloop()

def ClearText():
    textw.delete('0.0', END)

def browse():
    file = tkinter.filedialog.askopenfilename(title="Open a file...")
    InputString1.set(file)

def Check():
    text = ""
    # gets the the file to check
    file = InputString1.get()

    if len(file) == 0:
        text = text + '=======================\n'
        text = text + 'FEL: ingen fil angiven!\n'
        text = text + '=======================\n'
        print("")
        print(text)

    # gets the hash to check against
    hash = textw.get('1.0', 'end')

    #removes new line character
    hash = hash[:-1]

    # removes blank spaces at the ends
    #hash = hash.trim()

    text = text + 'Fil: ' + file + '\n\n'

    # ta bort osynliga tecken i början och slutet
    hash = hash.strip()

    # ta bort blanka
    hash = hash.replace(" ","")

    # ta bort radbrytningar
    hash = hash.replace("\n","")

    text = text + 'hash:\n'
    text = text + hash + '\n\n'

    # längd på kontrollsumman
    hashlength = len(hash)
    htext = 'Antar kontrollsummealgoritmen (HASH): '

    # HEX-format
    text = text + 'Kontrollsummans längd (bitar): '
    #text = text + 'hash length: '
    text = text + str(hashlength * 4) + '\n\n'

    hashtype = ""

    if hashlength == 32:
        hashtype = 'md5'
        hasher  = hashlib.md5()

    elif hashlength == 40:
        hashtype =  'sha1'
        hasher  = hashlib.sha1()

    elif hashlength == 64:
        hashtype = 'sha256'
        hasher  = hashlib.sha256()

    elif hashlength == 128:
        hashtype =  'sha512'
        hasher  = hashlib.sha512()

    else:
        text = text + 'Längden ska vara 128, 160, 256 eller 512 bitar' + '\n\n'
        text = text + 'ERROR: !!!!!!!!!!!!!!!!!!!!!!\n'
        text = text + 'ERROR: Unknown hash algorithm\n'
        text = text + 'ERROR: !!!!!!!!!!!!!!!!!!!!!!'

    if len(hashtype) == 0:
        # Deletes text in the text window
        textw.delete('0.0', END)
        # Inserts message
        textw.insert('0.0', text)

    else:

        # Skriv ut antagen hash-typ
        text = text + htext + hashtype + "\n\n"

        # Läser en bit i taget, så att man kan kolla även filer som inte ryms i minnet.

        try:
            f = open(file, 'rb')
        except IOError as e:
            text = text + '=========================================================================' + '\n'
            text = text + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            text = text + "!!! I/O error({0}): {1}".format(e.errno, e.strerror) + "!!!\n"
            text = text + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            text = text + '=========================================================================' + '\n\n'
            print(text)
            textw.delete('0.0', END)
            textw.insert('0.0', text)
        except:
            text = text + '=========================================================================' + '\n'
            text = text + "!!! Unknown ERROR !!!"
            text = text + '=========================================================================' + '\n'
            print(text)
            textw.delete('0.0', END)
            textw.insert('0.0', text)

        else:
            try:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    hasher.update(chunk)
            finally:
                f.close()

        newhash = hasher.hexdigest()

        text = text + 'Angiven kontrollsumma (hash):' + '\n'
        text = text + hash + "\n" + "\n"
        #text = text + u'Beräknad kontrollsumma (hash): ' + '\n'
        text = text + 'Calculated checksum (hash): ' + '\n'
        text = text + newhash + '\n'
        text = text + newhash.upper() + '\n\n'

        okmessage = 'OK!\n\nKontrollsumman OK av filen:\n' + file + '\n\n:-)'

        if hash == newhash:
            text = text + okmessage

        elif hash == newhash.upper():
            text = text + okmessage
        else:
            text = text + '*** !!! VARNING: Felaktig kontrollsumma. !!! ***' + '\n'
            text = text + '=========================================================================' + '\n'

        # Deletes text in the text window
        textw.delete('0.0', END)
        # Inserts decrypted text
        textw.insert('0.0', text)

def about():

    text = 'CHECKHASHGUI - Calculates the checksum of file and compares it with user input.\n\n'
    text = text + 'Copyright (c) 2012-2014 Per Tunedal, Stockholm, Sweden\n'
    text = text + 'Author: Per Tunedal <info@tunedal.nu>\n'
    text = text + 'www.kryptera.tunedal.nu\n\n'
    text = text + 'This program is free software: you can redistribute it and/or modify '
    text = text + 'it under the terms of the GNU General Public License as published by '
    text = text + 'the Free Software Foundation, either version 3 of the License, or '
    text = text + '(at your option) any later version.\n\n'
    text = text + 'This program is distributed in the hope that it will be useful, '
    text = text + 'but WITHOUT ANY WARRANTY; without even the implied warranty of '
    text = text + 'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the '
    text = text + 'GNU General Public License for more details.\n'
    text = text + 'You should have received a copy of the GNU General Public License '
    text = text + 'along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'

    # Deletes text in the text window
    textw.delete('0.0', END)
    # Inserts new text
    textw.insert('0.0', text)

def help():
    webbrowser.open('http://kryptera.tunedal.nu')

def quit():
    root.withdraw()
    root.quit()

GetString()
