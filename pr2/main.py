"""Модуль с интерфейсом"""
import json
import sys
from rsa import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


def read_in_chunks(file_path, chunk_size=4096):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk


class Window():
    def __init__(self):
        self.ui = uic.loadUi('gui.ui')
        self.ui.setWindowTitle("RSA")
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decipher.clicked.connect(self.decipher_text)
        self.ui.btn_generate_key.clicked.connect(self.generate_key)
        #Вариант 24(4) - 38
        self.bits = 38
        # Unicod - // 8, Ascii - // 4
        self.block_size = self.bits // 8
        self.curr_open_key = None
        self.last_open_file = None
        try:
            with open('data.json', 'r') as file:
                self.privates_key = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.privates_key = {}
        self.ui.show()


    def encrypt_text(self):
        key = self.ui.lineEdit_key.text().strip()
        text = self.ui.textEdit_original.toPlainText()
        if not self.validate_input(key, text):
            return
        key = list(map(int, key.split()))
        crypt_text = " ".join(rsa_encrypt_text(key, text, self.block_size))
        self.ui.textEdit_encrypted.setText(str(crypt_text))
        self.show_message("Текст зашифрован")

    def decipher_text(self):
        key = self.ui.lineEdit_key.text().strip()
        encrypt_text = self.ui.textEdit_encrypted.toPlainText().strip()
        if not self.validate_input(key, encrypt_text):
            return
        try:
            encrypt_text = list(map(int, encrypt_text.split()))
        except ValueError:
            return self.show_message("Ошибка дешифровки")
        crypt_text = rsa_decrypt_text(
            self.privates_key[key], encrypt_text, self.block_size)
        if crypt_text == -1:
            return self.show_message("Ошибка дешифровки")
        self.ui.textEdit_original.setText(str(crypt_text))
        self.show_message("Текст расшифрован")

    def generate_key(self):
        _, open_key, private_key = generate_params_and_keys(self.bits)
        str_open_key = f"{open_key[0]} {open_key[1]}"
        self.ui.lineEdit_key.setText(str_open_key)
        self.privates_key[str_open_key] = private_key
        self.ui.line_message.setText(f"Ключ успешно сгенерирован")

    def validate_input(self, key, text):
        if not key:
            self.show_message("Введите открытый ключ в формате s n")
            return False
        if self.privates_key.get(key, None) is None:
            self.show_message("Такой открытого ключа нет")
            return False
        if not text:
            self.show_message("Введите текст")
            return False
        return True

    def show_message(self, message):
        self.ui.line_message.setText(message)


if __name__ == "__main__":
    app = QApplication([])
    myapp = Window()
    sys.exit(app.exec_())