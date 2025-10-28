# ECC_implementation

## Nom
Théo CAUDAN

## Description
Le script suivant permet de :
- Générer une paire de clefs privée (k) et publique (Q = kP)
- Chiffrer un message à l'aide d'une clef publique
- Déchiffrer un message préalablement chiffrée avec la clef publique à l'aide d'une clef privée associée

---
## Pré-requis
Installer Python3 et la librairie cryptography

```python
pip install cryptography
```
---
## Comment l'utiliser ?
Afficher l'aide:

```python
python -m monECC help
```

Générer une paire de clefs:

```python
python -m monECC keygen
```

Chiffrer un message:

```python
python -m monECC crypt monECC.pub "Texte en clair"
```

Déchiffrer un message:

```python
python -m monECC decrypt monECC.priv "Message chiffré"
```
