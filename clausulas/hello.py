"""
Laboratorio: Clausulas de Datalog (relaciones familiares)
Autores: Nava Campos Alejandro Dante, Jonathan Tiro Cuanenemi.

Objetivo:
Completar el programa base de pyDatalog (que ya definia papa, abuelo,
hermano y antecesores) agregando las clausulas faltantes: mama, hombre,
mujer, hermana, tio, tia, primo y prima.

Nota sobre los datos:
El programa original solo tenia hechos "papa" para una linea paterna
(Bruno -> John -> Pedro -> {Luis, Pablo}). Con esos datos no hay forma de
obtener resultados no vacios para hermana, tio, tia, primo o prima (no hay
mujeres ni hermanos con hijos propios en la familia). Por eso se agregan
algunos hechos adicionales (una madre por cada hijo, una hermana de Pedro
y sus hijos) para poder mostrar corridas con resultados reales.
"""

from pyDatalog import pyDatalog

# 1. Declaracion de terminos (predicados y variables) usados en el programa.
#    Se agregan los predicados que faltaban: mama, hombre, mujer, hermana,
#    tio, tia, primo, prima; y la variable auxiliar P1.
pyDatalog.create_terms(
    'papa, mama, abuelo, hombre, mujer, hermano, hermana, tio, tia, '
    'primo, prima, antecesores, X, Y, Z, P1'
)

# ---------------------------------------------------------------------------
# 2. Assert Facts (prefixed with a '+')
# ---------------------------------------------------------------------------

# --- Relacion paterna (papa): la que ya traia el programa -------------------
+ papa('Bruno', 'John')
+ papa('John', 'Pedro')
+ papa('Pedro', 'Luis')
+ papa("Pedro", 'Pablo')

# Descendientes adicionales, necesarios para poder mostrar resultados no
# vacios en hermana/tio/tia/primo/prima (ver nota del encabezado).
+ papa('John', 'Ana')          # Ana es hermana de Pedro (hija de John)
+ papa('Pedro', 'Lucia')       # Lucia es hermana de Luis y Pablo (hija de Pedro)

# --- Relacion materna (mama): NUEVO -----------------------------------------
# El genero y la relacion materna no se pueden deducir logicamente solo a
# partir de "papa"; se agregan como hechos explicitos, igual que "papa".
+ mama('Rosa', 'John')
+ mama('Elena', 'Pedro')
+ mama('Elena', 'Ana')
+ mama('Sofia', 'Luis')
+ mama('Sofia', 'Pablo')
+ mama('Sofia', 'Lucia')
+ mama('Ana', 'Diego')         # Diego es hijo de Ana -> primo de Luis/Pablo/Lucia
+ mama('Ana', 'Valeria')       # Valeria es hija de Ana -> prima de Luis/Pablo/Lucia

# --- Genero (hombre / mujer): NUEVO -----------------------------------------
# Tampoco se puede inferir el genero solo con "papa"/"mama" (ser padre o
# madre no dice si Luis o Pablo, que nunca aparecen como padres, son
# hombres). Se agregan como hechos explicitos.
+ hombre('Bruno')
+ hombre('John')
+ hombre('Pedro')
+ hombre('Luis')
+ hombre('Pablo')
+ hombre('Diego')

+ mujer('Rosa')
+ mujer('Elena')
+ mujer('Sofia')
+ mujer('Ana')
+ mujer('Lucia')
+ mujer('Valeria')

# ---------------------------------------------------------------------------
# 3. Reglas (clausulas)
# ---------------------------------------------------------------------------

# abuelo(X, Y): X es abuelo/abuela de Y si X es papa de alguien (Z) que a
# su vez es papa de Y. (regla original, sin modificar)
abuelo(X, Y) <= papa(X, Z) & papa(Z, Y)

# hermano(X, Y): definicion original, sin modificar. Comparten padre Z y
# son distintos (no filtra genero).
hermano(X, Y) <= papa(Z, X) & papa(Z, Y) & (X != Y)

# hermana(X, Y): NUEVO. Igual que hermano (comparten papa o mama), pero
# ademas X debe ser mujer.
hermana(X, Y) <= papa(Z, X) & papa(Z, Y) & (X != Y) & mujer(X)
hermana(X, Y) <= mama(Z, X) & mama(Z, Y) & (X != Y) & mujer(X)

# tio(X, Y): NUEVO. X es tio de Y si X es hombre y es hermano de alguno de
# los padres (papa o mama) de Y.
tio(X, Y) <= hermano(X, Z) & papa(Z, Y) & hombre(X)
tio(X, Y) <= hermano(X, Z) & mama(Z, Y) & hombre(X)

# tia(X, Y): NUEVO. X es tia de Y si X es hermana de alguno de los padres
# (papa o mama) de Y. (hermana ya exige que X sea mujer)
tia(X, Y) <= hermana(X, Z) & papa(Z, Y)
tia(X, Y) <= hermana(X, Z) & mama(Z, Y)

# primo(X, Y) / prima(X, Y): NUEVO. X es primo/prima de Y si el papa o la
# mama de X (P1) es tio o tia de Y. primo exige que X sea hombre; prima,
# que X sea mujer.
primo(X, Y) <= papa(P1, X) & tio(P1, Y) & hombre(X)
primo(X, Y) <= papa(P1, X) & tia(P1, Y) & hombre(X)
primo(X, Y) <= mama(P1, X) & tio(P1, Y) & hombre(X)
primo(X, Y) <= mama(P1, X) & tia(P1, Y) & hombre(X)

prima(X, Y) <= papa(P1, X) & tio(P1, Y) & mujer(X)
prima(X, Y) <= papa(P1, X) & tia(P1, Y) & mujer(X)
prima(X, Y) <= mama(P1, X) & tio(P1, Y) & mujer(X)
prima(X, Y) <= mama(P1, X) & tia(P1, Y) & mujer(X)

# antecesores(X, Y): regla original, sin modificar.
antecesores(X, Y) <= papa(X, Y)
antecesores(X, Y) <= papa(X, Z) & antecesores(Z, Y)

# ---------------------------------------------------------------------------
# 4. Corridas: se imprime el resultado de cada predicado
# ---------------------------------------------------------------------------

print("abuelo(X, Y)")
print(abuelo(X, Y))

print("\nhermano(X, Y)")
print(hermano(X, Y))

print("\nhermana(X, Y)")
print(hermana(X, Y))

print("\nhombre(X)")
print(hombre(X))

print("\nmujer(X)")
print(mujer(X))

print("\ntio(X, Y)")
print(tio(X, Y))

print("\ntia(X, Y)")
print(tia(X, Y))

print("\nprimo(X, Y)")
print(primo(X, Y))

print("\nprima(X, Y)")
print(prima(X, Y))

print("\nantecesores(X, Y)")
print(antecesores(X, Y))
