import random as rd
import base64

def keygen(filename="monECC"):
    P = (2, 9)
    Q = (0, 0)

    k = int(rd.randrange(1, 1000))

    with open(f"{filename}.priv", "w") as f:
        f.write("---begin monECC private key---\n")
        f.write(base64.b64encode(str(k).encode()).decode() + "\n")
        f.write("---end monECC key---\n")

    Q = (Q[0] + P[0] * k, Q[1] + P[1] * k)

    with open(f"{filename}.pub", "w") as f:
        f.write("---begin monECC public key---\n")
        f.write(base64.b64encode(f"{Q[0]},{Q[1]}".encode()).decode() + "\n")
        f.write("---end monECC key---\n")

    print(f"Paire de clefs générée : {filename}.priv et {filename}.pub")