import hashlib


def calcular_sha256(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as arquivo:
        while bloco := arquivo.read(4096):
            sha256.update(bloco)

    return sha256.hexdigest()