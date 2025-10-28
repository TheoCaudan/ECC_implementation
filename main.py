import random as rd
import base64 as b64
import hashlib as hl

P = (2, 9)

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
    if not lines or lines[0] != "---begin mon ECC public key---":
        print("Erreur : fichier de clef publique invalide.")
        return None
    coords = b64.b64decode(lines[1]).decode()
    x_str, y_str = coords.split(",")
    return (int(x_str), int(y_str))
    
if __name__ == "__main__":
    print("Coucou")
