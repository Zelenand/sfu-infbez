import random
from sympy import primerange
def generate_primes(bits):
    while True:
        low_border = random.randint(10 ** (bits // 2 - 1), 10 ** (bits // 2))
        high_border = low_border + random.randint(10**4, 10**5)
        primes = list(primerange(low_border, high_border))
        index1 = random.randint(0, len(primes) - 1)
        index2 = random.randint(0, len(primes) - 1)
        p = primes[index1]
        q = primes[index2]
        #print("primes generating try", p, q, p*q)
        if 10 ** (bits-1) <= p * q <= 10 ** (bits):
            return p, q

def gcd(a, b):
    """Функция для нахождения наибольшего общего делителя"""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Обобщенный алгоритм Евклида"""
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_params_and_keys(bits):
    """Генерация параметров и ключей"""
    p, q = generate_primes(bits)
    #print("primes generated")
    n = p * q
    phi = (p - 1) * (q - 1)
    s = random.randint(2, phi - 1)
    while gcd(s, phi) != 1:
        s = random.randint(2, phi - 1)
    e = mod_inverse(s, phi)
    #print("keys generated")
    return ((p, q), (s, n), (e, n))

def encrypt_block(public_key, block):
    s, n = public_key
    cipher = ''.join([str(len(str(ord(char)))) for char in block])
    for char in block:
        cipher += str(ord(char))
    return str(pow(int(cipher), s, n))

def decrypt_block(private_key, block):
    e, n = private_key
    try:
        plain = str(pow(int(block), e, n))
    except OverflowError:
        return -1
    return plain

def rsa_encrypt_text(public_key, text, block_size):
    encrypted_text = []
    if k_space := (len(text) % block_size):
        text += (block_size - k_space) * " "
    text += str(k_space) * block_size
    for i in range(0, len(text), block_size):
        block = text[i:i + block_size]
        encrypted_text.append(encrypt_block(public_key, block))
    return encrypted_text

def rsa_decrypt_text(private_key, text, block_size):
    decrypt_text = ""
    for block in text:
        block_str = decrypt_block(private_key, block)
        if block_str == -1:
            return -1
        sizes = [int(block_str[i]) for i in range(block_size)]
        curr = block_size
        for size in sizes:
            try:
                decrypt_text += chr(int(block_str[curr:curr+size]))
            except ValueError:
                return -1
            curr += size
    padding = (block_size - int(decrypt_text[-1])) % block_size
    decrypt_text = decrypt_text[:-(block_size+padding)]
    return decrypt_text


if __name__ == "__main__":
    import time


    total_time = 0
    number_of_iterations = 50

    for i in range(number_of_iterations):
        start_time = time.time()
        generate_params_and_keys(38)
        end_time = time.time()
        total_time += (end_time - start_time)


    average_time = total_time / number_of_iterations

    print(f"Среднее время выполнения за {number_of_iterations} вызовов: {average_time} секунд")
    #Среднее время выполнения за 50 вызовов: 0.4098485279083252 секунд
