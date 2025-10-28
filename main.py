import random as rd
import base64 as b64
import hashlib as hl

P = (2, 9)
a, b, p = 35, 3, 101

def keygen(filename="monECC"):
    Q = (0, 0)

    k = int(rd.randrange(1, 1000))

    with open(f"{filename}.priv", "w") as f:
        f.write("---begin monECC private key---\n")
        f.write(b64.b64encode(str(k).encode()).decode() + "\n")
        f.write("---end monECC key---\n")

    Q = (Q[0] + P[0] * k, Q[1] + P[1] * k)

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
    private_key = b64.b64decode(lines[1]).decode()
    return private_key

def inverse_mod(k, p):
    """ Calcul du modulo inverse (on cherche x, (k * x) % p = 1) """
    k = k % p
    return pow(k, -1, p)

def add_coordinates(P1, P2):
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
            result = add_coordinates(result, addend)
        addend = add_coordinates(addend, addend)
        k >>= 1
    return result

def shared_secret():
    return 

if __name__ == "__main__":
    print("Coucou")

