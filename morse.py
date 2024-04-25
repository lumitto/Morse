import json


def load_alphabet_json(file_path: str):
    with open(file_path) as alphabet:
        return json.load(alphabet)


def create_alpha_dict(file_path: str):  # Alternative
    """ Uses certain .txt file as a data to create a dictionary with corresponding characters (English: Morse).
     Data was taken from 'https://morsedecoder.com/morse-code-alphabet/'. """
    with open(file_path) as alphabet:
        lines = alphabet.readlines()
        text_values = [line.replace('\n', '').split('\t')[0] for line in lines]
        morse_values = [line.replace('\n', '').split('\t')[1] for line in lines]

        morse_dict = {}
        i = 0
        if len(text_values) == len(morse_values):
            for text_value in text_values:
                morse_dict[text_value] = morse_values[i]
                i += 1
            return morse_dict
        else:
            raise ValueError


class Morse:
    """ Responsible for processing and storing text and morse values for one string. """
    morse_alphabet = load_alphabet_json("morse-alphabet.json")

    def __init__(self):
        self.morse_val_bp = ""  # TODO Remove. Add single converting method.
        self.morse_val = ""
        self.text_val = ""
        self.morse_separator = " "

    def set_morse(self, morse):
        if self.morse_val != morse:
            self.morse_val = morse
            self.to_text()

    def set_text(self, text):
        if self.text_val != text:
            self.text_val = text
            self.to_morse()

    def get_morse_bp(self):
        return self.morse_val_bp

    def get_morse(self):
        return self.morse_val

    def get_text(self):
        return self.text_val

    def to_morse(self):
        morse = self.get_text().split(" ")
        morse = [word for word in morse if word != ""]
        text = ""

        for word in morse:
            word_ = word
            for letter in list(word_):
                if letter.upper() in list(self.morse_alphabet.keys()):
                    to_add = self.morse_alphabet[letter.upper()]
                else:
                    to_add = "#"
                word_ = word_.replace(letter, to_add + self.morse_separator)
            word_ += "/ "
            text += word_

        self.morse_val = text[:-3]
        self.morse_val_bp = self.morse_val.replace(".", "•")

    def to_text(self):
        morse = self.get_morse().split(self.morse_separator)
        morse = [seq.strip() for seq in morse]
        morse = [seq for seq in morse if seq != '']
        morse = [seq.replace("•", ".") for seq in morse]

        for seq in morse:
            morse_values = list(self.morse_alphabet.values())

            if seq in morse_values:
                morse[morse.index(seq)] = list(self.morse_alphabet.keys())[morse_values.index(seq)]
            else:
                morse[morse.index(seq)] = "#"

        self.text_val = "".join(morse)
