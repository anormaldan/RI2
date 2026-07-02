from pyDatalog import pyDatalog

pyDatalog.create_terms('papa, abuelo,hermano,antecesores,'+
                       'X, Y, Z')

# 2. Assert Facts (prefixed with a '+')
+ papa('Bruno', 'John')
+ papa('John', 'Pedro')
+ papa('Pedro', 'Luis')
+ papa("Pedro", 'Pablo')

abuelo(X, Y) <= papa(X, Z) & papa(Z, Y)
hermano(X,Y) <= papa(Z,X) & papa(Z,Y) & (X != Y)
antecesores(X,Y) <= papa(X,Y)
antecesores(X,Y) <= papa(X,Z) & antecesores(Z,Y)
'''
hombre
mujer
mama
hermana
tío
tía
primo
prima
'''

print("abuelo")
print( abuelo(X, Y))
print("hermano")
print(hermano(X,Y))
print("antecesores")
print(antecesores(X,Y))
