import struct

def lire_audio(fichier_audio):
    with open(fichier_audio, "rb") as f:
        contenu = f.read()
    data = contenu[44:]  # On saute l'entête du fichier WAV (44 octets)
    nb_echantillons = len(data) // 2
    echantillons = struct.unpack(f"<{nb_echantillons}h", data)
    canal_gauche = echantillons[::2]
    canal_droit = echantillons[1::2]
    return canal_gauche, canal_droit

def reduire_echantillons(g, d):
    # on prend un échantillon sur deux
    return g[::2], d[::2]

def sauvegarder_audio(g, d):
    nb = len(g)
    entete = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + nb * 4, b'WAVE', b'fmt ', 16,
        1, 2, 44100, 44100 * 4, 4, 16,
        b'data', nb * 4
    )
    flux_audio = bytearray()
    for i in range(nb):
        flux_audio += struct.pack('<h', g[i]) + struct.pack('<h', d[i])
    return entete + flux_audio

def lisser_audio(g, d):
    new_g, new_d = [], []
    for i in range(len(g) - 1):
        new_g.append(g[i])
        new_g.append((g[i] + g[i + 1]) // 2)
        new_d.append(d[i])
        new_d.append((d[i] + d[i + 1]) // 2)
    return new_g, new_d

def changer_vitesse(facteur, pistes):
    g, d = pistes
    g_mod, d_mod = [], []
    position = 0.0
    while int(position) < len(g) - 1:
        i = int(position)
        frac = position - i
        # Interpolation linéaire pour éviter les sauts brusques
        val_g = int(g[i] * (1 - frac) + g[i + 1] * frac)
        val_d = int(d[i] * (1 - frac) + d[i + 1] * frac)
        g_mod.append(val_g)
        d_mod.append(val_d)
        position += facteur
    return g_mod, d_mod

def effet_echo(pistes, delay, force):
    g, d = pistes
    taille = len(g)
    out_g = [0] * taille
    out_d = [0] * taille
    for i in range(delay):
        out_g[i] = g[i]
        out_d[i] = d[i]
    for i in range(taille - delay):
        # Mélange le signal original et retardé pour créer l’écho
        out_g[i + delay] = int((1 - force) * g[i] + force * out_g[i + delay])
        out_d[i + delay] = int((1 - force) * d[i] + force * out_d[i + delay])
    return out_g, out_d

if __name__ == "__main__":
    fichier_source = '/Users/erixxu/Desktop/Python Mines/26 mars/the_wall.wav'
    gauche, droite = lire_audio(fichier_source)

    echantillons_reduits = reduire_echantillons(gauche, droite)
    ralenti = lisser_audio(gauche, droite)
    vitesse_modifiee = changer_vitesse(1.5, (gauche, droite))
    piste_echo = effet_echo((gauche, droite), delay=10000, force=0.5)

    resultat = sauvegarder_audio(piste_echo[0], piste_echo[1])
    with open("audio_modifie.wav", "wb") as f_sortie:
        f_sortie.write(resultat)

    print("Fichier modifié sauvegardé.")
