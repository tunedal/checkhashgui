#!/usr/bin/env python3

# CHECKHASHGUI - Calculates the checksum of file and compares it with user input.
# Version: 0.3

# Copyright (c) 2012-2014 Per Tunedal, Stockholm, Sweden
# Author: Per Tunedal <info@tunedal.nu>

# Minor modifications by Henrik Tunedal (2022).

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

# 0.3 (by Henrik Tunedal)
# Updated for Python 3.
# Minor layout fixes.
# Minor code cleanup.


import hashlib, webbrowser
import tkinter as tk, tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from tkinter import E, W, S, N, INSERT, END
from functools import partial


def main():
    root = tk.Tk()
    app = App(root)
    build_ui(root, partial(MainController, app))
    root.mainloop()


class MainController:
    def __init__(self, app, view):
        self._app = app
        self._view = view

    def clear_text(self):
        self._view.clear_text()

    def browse(self):
        self._view.set_filename(self._view.show_open_file_dialog())

    def check(self):
        view = self._view
        check(view.get_filename(), view.get_text(), view)

    def about(self):
        self._view.set_text(about())

    def help(self):
        webbrowser.open('https://tunedal.nu/nedladdning.htm')

    def quit(self):
        self._app.close()


class App:
    def __init__(self, root):
        self._root = root

    def close(self):
        self._root.destroy()


class MainView:
    def __init__(self, textw, filename_input):
        self._textw = textw
        self._filename_input = filename_input

    def get_text(self):
        return self._textw.get('1.0', 'end')

    def set_text(self, text):
        self._textw.delete('0.0', END)
        self._textw.insert('0.0', text)

    def clear_text(self):
        self._textw.delete('0.0', END)

    def get_filename(self):
        return self._filename_input.get()

    def set_filename(self, filename):
        self._filename_input.set(str(filename))

    def show_open_file_dialog(self):
        return filedialog.askopenfilename(title="Open a file...")


def build_ui(root, controller_factory):
    root.title("CHECK HASH")

    content = ttk.Frame(root)
    content.grid(row=0, column=0, sticky=E + W + S + N)

    c0 = ttk.Label(content, text="Check the HASH of a file",
                  font="georgia 16 bold")
    c0.grid(row=0, column=0, columnspan=3)

    c1 = ttk.Label(content, text="Please enter the FILENAME (full path): ")
    c1.grid(row=1, column=0, sticky=E)

    filename_input = tk.StringVar()
    ttk.Entry(content, width=30, textvariable=filename_input).grid(
        row=1, column=1, sticky=E + W)

    # wrap=word breaks too long lines after a word, not a character.
    textw = tk.Text(content, wrap="word")
    textw.insert(INSERT, "Please enter the hash here ...")
    textw.grid(row=2, columnspan=4, sticky=E + W + S + N)

    controller = controller_factory(MainView(textw, filename_input))

    ttk.Button(content, text=' Browse ... ', command=controller.browse
               ).grid(row=1, column=2, sticky=E)
    ttk.Button(content, text=' Help ', command=controller.help
               ).grid(row=0, column=3, sticky=E)
    ttk.Button(content, text='About', command=controller.about
               ).grid(row=1, column=3, sticky=E)

    button_frame = ttk.Frame(content)
    ttk.Button(button_frame, text='Clear', command=controller.clear_text
               ).grid(row=0, column=0, sticky=W)
    tk.Button(button_frame, text='Check', fg="white", bg="blue",
              command=controller.check
              ).grid(row=0, column=1, ipadx=20)
    ttk.Button(button_frame, text='QUIT', command=controller.quit
               ).grid(row=0, column=2, sticky=E)

    button_frame.columnconfigure(1, weight=1)
    button_frame.grid(row=3, column=0, columnspan=4, sticky=E + W)

    content.rowconfigure(2, weight=1)
    content.columnconfigure(1, weight=1)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


def check(filename, input_hash, view):
    text = ""

    if len(filename) == 0:
        text = text + '=======================\n'
        text = text + 'FEL: ingen fil angiven!\n'
        text = text + '=======================\n'
        print("")
        print(text)

    #removes new line character
    input_hash = input_hash[:-1]

    # removes blank spaces at the ends
    #input_hash = input_hash.trim()

    text = text + 'Fil: ' + filename + '\n\n'

    # ta bort osynliga tecken i början och slutet
    input_hash = input_hash.strip()

    # ta bort blanka
    input_hash = input_hash.replace(" ","")

    # ta bort radbrytningar
    input_hash = input_hash.replace("\n","")

    text = text + 'hash:\n'
    text = text + input_hash + '\n\n'

    # längd på kontrollsumman
    hashlength = len(input_hash)
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
        view.set_text(text)

    else:

        # Skriv ut antagen hash-typ
        text = text + htext + hashtype + "\n\n"

        # Läser en bit i taget, så att man kan kolla även filer som inte ryms i minnet.

        separator = '=' * 73

        try:
            f = open(filename, 'rb')
        except IOError as e:
            text = text + separator + '\n'
            text = text + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            text = text + "!!! I/O error({0}): {1}".format(e.errno, e.strerror) + "!!!\n"
            text = text + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            text = text + separator + '\n\n'
            print(text)
            view.set_text(text)
        except:
            text = text + separator + '\n'
            text = text + "!!! Unknown ERROR !!!"
            text = text + separator + '\n'
            print(text)
            view.set_text(text)

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
        text = text + input_hash + "\n" + "\n"
        #text = text + u'Beräknad kontrollsumma (hash): ' + '\n'
        text = text + 'Calculated checksum (hash): ' + '\n'
        text = text + newhash + '\n'
        text = text + newhash.upper() + '\n\n'

        okmessage = ('OK!\n\nKontrollsumman OK av filen:\n'
                     + filename + '\n\n:-)')

        if input_hash == newhash:
            text = text + okmessage

        elif input_hash == newhash.upper():
            text = text + okmessage
        else:
            text = text + '*** !!! VARNING: Felaktig kontrollsumma. !!! ***' + '\n'
            text = text + separator + '\n'

        view.set_text(text)


def about():
    text = 'CHECKHASHGUI - Calculates the checksum of file and compares it with user input.\n\n'
    text = text + 'Copyright (c) 2012-2014 Per Tunedal, Stockholm, Sweden\n'
    text = text + 'Author: Per Tunedal <info@tunedal.nu>\n'
    text = text + 'www.kryptera.tunedal.nu\n\n'
    text = text + 'Minor modifications by Henrik Tunedal (2022).\n\n'
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

    return text


if __name__ == "__main__":
    main()
