import random as rd
import base64 as b64
import hashlib as hl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import sys

P = (2, 9)
a, b, p = 35, 3, 101

def keygen(filename="monECC"):
    k = int(rd.randrange(1, 1000))
    Q = multiply_point(k, P)

    with open(f"{filename}.priv", "w") as f:
        f.write("---begin monECC private key---\n")
        f.write(b64.b64encode(str(k).encode()).decode() + "\n")
        f.write("---end monECC key---\n")

    with open(f"{filename}.pub", "w") as f:
        f.write("---begin monECC public key---\n")
        f.write(b64.b64encode(f"{Q[0]},{Q[1]}".encode()).decode() + "\n")
        f.write("---end monECC key---\n")

    print(f"Paire de clefs générée : {filename}.priv et {filename}.pub")

def read_public_key(file: str):
    with open(file, "r") as f:
        lines = [l.strip() for l in f.readlines()]
    if not lines or lines[0] != "---begin monECC public key---":
        print("Erreur : fichier de clef publique invalide.")
        return None
    coords = b64.b64decode(lines[1]).decode()
    x_str, y_str = coords.split(",")
    return (int(x_str), int(y_str))
    
def read_private_key(file: str):
    with open(file, "r") as f:
        lines = [l.strip() for l in f.readlines()]
    if not lines or lines[0] != "---begin monECC private key---":
        print("Erreur : fichier de clef privée invalide.")
        return None
    private_key = int(b64.b64decode(lines[1]).decode())
    return private_key

def inverse_mod(k, p):
    """ Calcul du modulo inverse (on cherche x, (k * x) % p = 1) """
    k = k % p
    try:
        return pow(k, -1, p)
    except ValueError:
        return None

def add_points(P1, P2):
    if P1 is None:
        return P2 # si P1 est le point à l'infini, on retourne P2 (identité additive)
    if P2 is None:
        return P1 # même logique: si P2 est le point à l'infini, on retourne P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P1 != P2:
        inv = inverse_mod(x2 - x1, p) # x2 - x1 est le delta  entre les deux points
        if inv is None:
            return None
        m = ((y2 - y1) * inv) % p # m = pente de la ligne reliant P1 et P2
    else:
        inv = inverse_mod(2 * y1, p) # addition d'un point avec lui-même
        if inv is None:
            return None
        m = ((3 * x1 * x1 + a) * inv) % p # m = pente de la tangente en P1 soit m = dérivée de la courbe elliptique)
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def multiply_point(k, P):
    result = None
    addend = P
    while k:
        if k & 1:
            result = add_points(result, addend)
        addend = add_points(addend, addend)
        k >>= 1
    return result

def shared_secret(k, Q):
    S = multiply_point(k, Q)
    secret_bytes = f"{S[0]},{S[1]}".encode()
    return hl.sha256(secret_bytes).digest()

def encrypt(pubfile, plaintext):
    Qb = read_public_key(pubfile)
    k_eph = rd.randint(1, 1000)
    S = shared_secret(k_eph, Qb)

    iv = S[:16]
    key = S[16:]

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    R = multiply_point(k_eph, P)
    cryptogram = f"{R[0]},{R[1]}:{b64.b64encode(ciphertext).decode()}"
    print(cryptogram)

def decrypt(privfile, cryptogram):
    k = read_private_key(privfile)
    try:
        R_str, c_b64 = cryptogram.split(":")
        Rx, Ry = map(int, R_str.split(","))
        R = (Rx, Ry)
        ciphertext = b64.b64decode(c_b64)
    except:
        raise ValueError("Format de message chiffré invalide.")
    
    S = shared_secret(k, R)
    iv = S[:16]
    key = S[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    print(plaintext.decode())

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print("Script monECC")
        print("Usage: monECC <keygen|crypt|decrypt|help> [<clef>] [<texte>] [-f filename]")
        return
    
    cmd = sys.argv[1]

    if cmd == "keygen":
        filename = "monECC"
        if "-f" in sys.argv:
            idx = sys.argv.index("-f")
            if idx+1 < len(sys.argv):
                filename = sys.argv[idx+1]
        keygen(filename)

    elif cmd == "crypt":
        if len(sys.argv) < 4:
            print("crypt nécessite <clef> et <texte>")
            return
        encrypt(sys.argv[2], sys.argv[3])

    elif cmd == "decrypt":
        if len(sys.argv) < 4:
            print("decrypt nécessite <clef> et <texte_chiffré>")
            return
        decrypt(sys.argv[2], sys.argv[3])

    else:
        print("Commande inconnue")
        return

if __name__ == "__main__":
    main()

