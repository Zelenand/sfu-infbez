from PyQt5.QtWidgets import *

import sys

import gui
import hill_cipher


class Main(QMainWindow, gui.Ui_Form):
    """
    Класс интерфейса
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.hill_cipher_encrypt)
        self.pushButton_2.clicked.connect(self.hill_cipher_modified_encrypt)
        self.pushButton_3.clicked.connect(self.hill_cipher_decrypt)
        self.pushButton_4.clicked.connect(self.hill_cipher_modified_decrypt)

    def hill_cipher_encrypt(self):
        self.textEdit.setText(hill_cipher.hill_cipher(self.lineEdit.text(), self.lineEdit_2.text()))

    def hill_cipher_decrypt(self):
        self.textEdit.setText(hill_cipher.hill_cipher(self.lineEdit.text(), self.lineEdit_2.text(), decrypt=True))

    def hill_cipher_modified_encrypt(self):
        self.textEdit_2.setText(hill_cipher.hill_cipher_modified(self.lineEdit_4.text(), self.lineEdit_3.text().split('/')))

    def hill_cipher_modified_decrypt(self):
        self.textEdit_2.setText(hill_cipher.hill_cipher_modified(self.lineEdit_4.text(), self.lineEdit_3.text().split('/'), decrypt=True))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec()