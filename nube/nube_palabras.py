"""
Laboratorio: Nube de Palabras desde Archivo de Texto
Autores: Nava Campos Alejandro Dante.

Objetivo:
Leer un archivo de texto plano, contar la frecuencia de sus palabras
y generar una nube de palabras visual.

Entradas:
    archivo_de_texto.txt

Salidas:
    output/nube_palabras.png
"""

import os
import re
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords


# ---------------------------------------------------------
# Descargar stopwords de NLTK (solo la primera vez)
# ---------------------------------------------------------

nltk.download("stopwords", quiet=True)


# ---------------------------------------------------------
# Rutas
# ---------------------------------------------------------

INPUT_FILE  = "archivo_de_texto.txt"
OUTPUT_DIR  = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "nube_palabras.png")


# ---------------------------------------------------------
# Leer archivo
# ---------------------------------------------------------

def leer_archivo(ruta):
    """Lee el archivo en UTF-8, codificación estándar para texto en español
    con acentos y caracteres especiales (á, é, ñ, etc.)."""

    # Se usa únicamente UTF-8 porque es el estándar moderno y la codificación
    # que manejan los editores actuales (VS Code, Notepad++, etc.).
    # Una mejora futura sería detectar automáticamente la codificación
    # con la librería chardet para mayor compatibilidad.
    with open(ruta, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------
# Limpiar texto
# ---------------------------------------------------------

def limpiar_texto(texto):
    """Convierte a minúsculas y elimina caracteres no alfabéticos."""

    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


# ---------------------------------------------------------
# Contar frecuencias
# ---------------------------------------------------------

def contar_frecuencias(texto):
    """Cuenta cuántas veces aparece cada palabra, sin stopwords."""

    # stopwords en español e inglés desde NLTK + las de la librería wordcloud
    stops_es = set(stopwords.words("spanish"))
    stops_en = set(stopwords.words("english"))
    stops_wc = {w.lower() for w in STOPWORDS}

    todas_stopwords = stops_es | stops_en | stops_wc

    palabras = [
        p for p in texto.split()
        if len(p) >= 3 and p not in todas_stopwords
    ]

    return Counter(palabras)


# ---------------------------------------------------------
# Generar nube
# ---------------------------------------------------------

def generar_nube(frecuencias, ruta_salida):
    """Genera la nube de palabras y la guarda como imagen."""

    nube = WordCloud(
        width=1000,
        height=600,
        background_color="black",   # fondo negro para mayor contraste visual
        max_words=60,               # toma las 60 palabras con mayor frecuencia; el resto se descarta
        colormap="plasma",
        collocations=False,
    ).generate_from_frequencies(dict(frecuencias))

    plt.figure(figsize=(12, 7))
    plt.imshow(nube, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de palabras", fontsize=14)
    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(ruta_salida, dpi=150)

    print("Imagen guardada en:", ruta_salida)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 50)
    print("NUBE DE PALABRAS")
    print("=" * 50)

    # --------------------------
    # Leer y limpiar
    # --------------------------

    print("\nLeyendo archivo:", INPUT_FILE)

    texto = leer_archivo(INPUT_FILE)
    texto = limpiar_texto(texto)

    # --------------------------
    # Contar frecuencias
    # --------------------------

    print("Contando frecuencias...")

    frecuencias = contar_frecuencias(texto)

    print("Palabras únicas encontradas:", len(frecuencias))

    # --------------------------
    # Generar nube
    # --------------------------

    print("Generando nube de palabras...")

    generar_nube(frecuencias, OUTPUT_FILE)

    # --------------------------
    # VALIDACIÓN PARA REPORTE
    # --------------------------

    print("\n" + "=" * 50)
    print("VALIDACIÓN PARA REPORTE")
    print("=" * 50)

    print("\nTop 20 palabras más frecuentes:\n")
    print(f"{'#':<4} {'Palabra':<20} {'Frecuencia':>10}")
    print("-" * 36)

    for i, (palabra, conteo) in enumerate(frecuencias.most_common(20), 1):
        print(f"{i:<4} {palabra:<20} {conteo:>10}")

    # verificación de la palabra más frecuente
    palabra_top, conteo_top = frecuencias.most_common(1)[0]
    total = sum(frecuencias.values())

    print(f"\nPalabra más frecuente : '{palabra_top}'")
    print(f"Aparece               : {conteo_top} veces de {total} tokens totales")

    print("\nPROCESO TERMINADO")

    plt.show()


main()

if __name__ == "__main__":
    pass