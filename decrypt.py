import random as rd

P = (2, 9)
Q = (0, 0)

k = int(rd.randrange(1, 1000))
print(f"k = {k}")

Q = (Q[0] + P[0] * k, Q[1] + P[1] * k)

print(f"Q = {Q}")
