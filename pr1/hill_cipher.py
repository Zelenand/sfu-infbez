import numpy as np
import math
from sympy import Matrix

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя?., "
alphabet_len = len(alphabet)

def hill_cipher(message, key, decrypt=False):
    if len(message) == 0 or len(key) == 0:
        return "Неккоректный ввод"
    n = math.sqrt(len(key))
    if n % 1 == 0:
        n = int(n)
    else:
        return "Неккоректный ввод"
    if (not (set(message) <= set(alphabet))) or (not (set(key) <= set(alphabet))):
        return "Неккоректный ввод"

    splitted_message = list([list(message[i:i + n]) for i in range(0, len(message), n)])

    while len(splitted_message[-1]) < n:
        splitted_message[-1].append(alphabet[-1])

    digit_message = []
    for i in range(0, len(splitted_message)):
        digit_message.append([])
        for j in splitted_message[i]:
            digit_message[i].append(alphabet.index(j))

    digit_key = []
    for i in key:
        digit_key.append(alphabet.index(i))
    matrix_key = np.array([digit_key[i:i + n] for i in range(0, len(digit_key), n)])

    if decrypt:
        matrix_key = np.array(Matrix(matrix_key).inv_mod(alphabet_len))

    ciphertext = ""
    for block in digit_message:
        new_block = [i % alphabet_len for i in np.array(block).dot(matrix_key)]
        for i in new_block:
            ciphertext += alphabet[i]
    return ciphertext

def hill_cipher_modified(message, keys, decrypt=False):
    if len(message) == 0 or min([len(i) for i in keys]) == 0:
        return "Неккоректный ввод"
    if type(keys) != list or len(keys) < 2:
        return "Неккоректный ввод"
    n = math.sqrt(len(keys[0]))
    if n % 1 == 0:
        n = int(n)
    else:
        return "Неккоректный ввод"
    for i in range(1, len(keys)):
        if len(keys[i]) != len(keys[0]):
            return "Неккоректный ввод"

    if (not (set(message) <= set(alphabet))) or (not (set("".join(keys)) <= set(alphabet))):
        return "Неккоректный ввод"

    splitted_message = list([list(message[i:i + n]) for i in range(0, len(message), n)])

    while len(splitted_message[-1]) < n:
        splitted_message[-1].append(alphabet[-1])

    digit_message = []
    for i in range(0, len(splitted_message)):
        digit_message.append([])
        for j in splitted_message[i]:
            digit_message[i].append(alphabet.index(j))
    digit_keys = []
    for key in keys:
        digit_keys.append([])
        for i in key:
            digit_keys[-1].append(alphabet.index(i))
    matrix_keys = []
    for key in digit_keys:
        matrix_key = np.array([key[i:i + n] for i in range(0, len(key), n)])
        matrix_keys.append(matrix_key)

    if decrypt:
        for i in range(0, len(matrix_keys)):
            matrix_key = np.array(Matrix(matrix_keys[i]).inv_mod(alphabet_len))
            matrix_keys[i] = matrix_key

    ciphertext = ""
    for i in range(0, len(digit_message)):
        new_block = [i % alphabet_len for i in np.array(digit_message[i]).dot(matrix_keys[i % len(matrix_keys)])]
        for i in new_block:
            ciphertext += alphabet[i]
    return ciphertext


if __name__ == '__main__':
    message = "шифр хилла это неплохой шифр"

    key = "альпинизм"
    ciphertext = hill_cipher(message, key)
    print("'" + ciphertext + "'")
    print(hill_cipher(ciphertext, key, decrypt=True))

    keys = ["альпинизм", "жаргонизм", "эфемерный"]
    ciphertext = hill_cipher_modified(message, keys)
    print("'" + ciphertext + "'")
    print(hill_cipher_modified(ciphertext, keys, decrypt=True))