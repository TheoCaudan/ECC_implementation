# ECC_implementation

## Nom
Théo CAUDAN

## Description
Ce script propose une implémentation simplifiée de chiffrement utilisant des courbes élliptiques.
Ce script permet de:
- Générer une paire de clefs privée (k) et publique (Q = kP)
- Chiffrer un message à l'aide d'une clef publique
- Déchiffrer un message préalablement chiffrée avec la clef publique à l'aide d'une clef privée associée

La clef symétrique est dérivée d'un secret partagé (ECDH), puis utilisée avec AES-CBC et padding PKCS#7.
---
## Pré-requis
Installer Python3 et la librairie cryptography

```bash
pip install cryptography
```
---
## Comment l'utiliser ?
Afficher l'aide:

```bash
python -m monECC help
```

Générer une paire de clefs:

```bash
python -m monECC keygen
```

Cela génère deux fichiers : "monECC.priv" et "monECC.pub"

### Options disponibles

-f <filename>

Permet de spécifier le nom de base des fichiers:

```bash
python -m monECC keygen -f alice
```

-> génère "alice.priv" et "alice.pub"

-s <size>

Permet de choisir la plage d'aléa de la clef privée (défaut = 1000):

```bash
python -m monECC keygen -s 50000
```

Notes: les options se combinent

Chiffrer un message:

```bash
python -m monECC crypt monECC.pub "Texte en clair"
```

-> produit un cryptogramme de la forme :

```bash
Rx,Ry:base64(ciphertext)
```

Déchiffrer un message:

```bash
python -m monECC decrypt monECC.priv "Message chiffré"
```
