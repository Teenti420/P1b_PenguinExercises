############################################################
#  Mi primer proyecto
#  Autor: Sebastià Vicens Oliver
#  Asignatura: 11630 - Tecnologies per l'Analisi de Dades Massives
############################################################

# Volvemos a encontrarnos con el conjunto de datos de pingüinos PalmerPenguins. 
# Esta vez trabajaremos con ellos desde Python, para ello instalaremos el paquete 
# que nos permitirá cargarlo:

# !pip install palmerpenguins

# Además usaremos los paquetes para el tratamiento de datos en python

# !pip install pandas
# !pip install numpy


# En segundo lugar, importaremos las librerías necesarias:
import pandas as pd
import numpy as np
from palmerpenguins import load_penguins

# Ahora ya estamos en posición de empezar a trabajar con los datos.

# 1. Vamos a cargar el conjunto de datos. Muestra por pantalla el número de observaciones 
# y sus características. Mira el tipo de datos de cada una de sus columnas.
penguins = load_penguins()
print(penguins)

penguins_dim = penguins.shape 
print(penguins.shape)

print("Por tanto el dataframe tiene un total de " + str(penguins_dim[0]) + " filas y " + str(penguins_dim[1]) + " columnas.\n")

# Como podemos observar tenemos 344 regiostros con 8 columnas o atributos cada uno de ellos.
print(penguins.columns)

# Ahora vamos a ver los tipos de los datos:
print(penguins.info())

# Y una pequeña descripción:
print(penguins.describe())

# 2. Ya sabemos que este conjunto de datos tiene observaciones NA. Vamos a eliminarlas y a 
# verificar que efectivamente no queda ninguno:
print(penguins.head(5).loc[3])

# Como podemos ver en este caso por ejemplo tenemos muchos valores NaN o "missing". 
# Vamos a eliminar dichos valores para poder tener unos datos más limpios y tractables.
penguins_without_na = penguins.dropna()
penguins.columns[penguins.isna().any()]
penguins.notna().sum()
penguins.notnull().sum() # es equivalente a not na en pandas, pero no en numpy

# 3. ¿Cuántos individuos hay de cada sexo? Puedes obtener la longitud media del pico según 
# el sexo:
print(penguins_without_na.columns)

# Es casi seguro que debamos explorar la columna sex del data set
print(np.unique(penguins_without_na["sex"]))

# Como podemos ver tenemos dos columnas diferentes de sex. 
# Estas son 'male' y 'female'. Ahora vamos a contar cuantos individuos tenemos de cada 
# uno de los tipos.
sex_col = penguins_without_na["sex"]
male_regs = penguins_without_na[sex_col == 'male']
total_male = male_regs.shape[0]
print("Hay un total de " + str(total_male) + " individuos masculinos")

# Como vemos tenemos 168 registros que son masculinos o 'male'. Si hacemos la diferencia 
# con el total ya deberiamos obtener los femeninos o female.
print("y " + str(penguins_without_na.shape[0]-total_male) + " femeninos.\n")

# Es decir que hay un total de 168 individuos femeninos. Podemos hecer lo mismo que con 
# los masculinos para ver si el resultado es igual.

female_regs = penguins_without_na[sex_col == 'female']
print(female_regs.shape[0])

# Como podemos ver, de las dos formas obtememos el mismo resultado, como era de esperar. 
# Por tanto, tenemos un total de 168 registros masculinos y 156 femeninos.

# Para obtener el tamaño medio del pico vamos a usar la función describe, que nos da mucha 
# información sobre nuestro data set. Como los datos ya estan separados en el paso anterior 
# solo hará falta aplicar las funciones sobre los datos filtrados.
#Calculamos la longitud media del pico en hombres
print(male_regs[male_regs.columns[2:4]].describe().iloc[1:2])

#Calculamos la longitud media del pico en mujeres
print(female_regs[female_regs.columns[2:4]].describe().iloc[1:2])

# Como vemos la longitud media del pico es de 45 mm en hombres y 42 mm en mujeres. 
# Por tanto los hombres suelen tener un pico mas largo que ellas.

# 4. Vamos a añadir una columna, vamos a realizar una estimación (muy grosera) del área del 
# pico de los pingüinos (bill) tal como si esta fuese un rectángulo. Esta nueva columnas se 
# llama bill_area y debe encontrarse en la última posición. Verifica que es correcto.

# Para ello utilizaremos la función assign con la que crearemos la nueva columna que será el 
# resultado del producto del bill_length_mm con bill_depth_mm.
penguins_b_area = penguins_without_na.assign(bill_area=penguins_without_na.bill_length_mm * penguins_without_na.bill_depth_mm)
print(penguins_b_area)

# Para hacer la verificación vamos a hacer el cálculo del área del primer registro [0] manualmente.
print("Area del primer registro creado: " + str(penguins_b_area.loc[0].bill_area))

bill_length_depth_mm = penguins_without_na[penguins_without_na.columns[2:4]]
print("Area calculada a partir del dataset: " + str(bill_length_depth_mm.loc[0].bill_length_mm * bill_length_depth_mm.loc[0].bill_depth_mm))

# 5. Hagamos algo un poco más elaborado, vamos a realizar una agrupación en función del sexo y de 
# la especie de cada observación. Queremos obtener solamente la información referente al sexo Femenino.

# Pongamos que queremos obtener información sobre el 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm' 
# y 'body_mass_g'. Para ello vamos a obtener un array con dichos nombres.
interest_columns = penguins_without_na.columns[2:6]
print(interest_columns)

# Ahora que tenemos los datos de los quales vamos a extraer la información he pensado dos formas de hacerlo. 
# La primera de ellas es la que me ha gustado más.

# Esta trata de realizar las agrupaciones por partes. Primero de todo, agrupamos el dataset por 'sex'. 
# Una vez tenemos el dataset agrupado obtenemos otro dataset filtrando por 'female'. Es decir, solo con registros 
# del individuo femenino.

# Una vez tenemos este dataset lo que hacemos es agrupar por especie y ya podemos obtener la información que 
# necesitemos sobre los datos.
penguins_grouped_by_sex = penguins_without_na.groupby(["sex"])
female_penguins = penguins_without_na.loc[penguins_grouped_by_sex.groups['female']]

female_penguins_species_grouped = female_penguins.groupby(["species"])

print(female_penguins_species_grouped.describe())

print(female_penguins_species_grouped[interest_columns].mean())

# Vamos a la segunda opción. Se trata de hacer la agrupación conjunta, es decir, a la vez. Para ello necesitamos 
# indicarle un parámetro nuevo que es **as_index** con el qual vamos a tratar la agrupación como si fuese una tabla 
# nueva y cada uno de los miembros agrupados será tractado como una columna. Así será más facil realizar el filtrado.

# Una vez se ha hecho la agrupación obtenemos un nuevo dataset que será el resultado de la operación que 
# queremos realizar sobre los datos. En nuestro caso vamos a obtener la mediana aritmética de los atributos 
# interesantes que hemos cogido al principio. 
penguins_grouped_by_sex_species = penguins_without_na.groupby(["sex", "species"], as_index=False)
mean_interested_columns_by_sex_species = penguins_grouped_by_sex_species[interest_columns].mean()
print(mean_interested_columns_by_sex_species)

# Como podemos observar hemos obtenido los datos correctamente pero aún tenemos los individuos masculinos.

# Es, por tanto, en este punto que debemos realizar el filtrado.
sex_attr = mean_interested_columns_by_sex_species['sex']
print(mean_interested_columns_by_sex_species.loc[sex_attr == 'female'])
# De esta manera, si comparamos los dos realutados veremos que son idénticos. Por tanto, se han visto dos 
# formas de hacer lo mismo.

# 6. Como ya sabemos, la variable peso, se encuentra en gramos, la pasaremos a kg. Para ello crearemos una 
# nueva columna llamada body_mass_kg y eliminaremos body_mass_g.

# Para ello vamos a usar la función asign para crear la nueva columna llamada body_mass_g y drop para 
# eliminar la columna antigua.
penguins_mass_kg = penguins_without_na.assign(body_mass_kg=penguins_without_na.body_mass_g / 1000)
penguins_mass_kg = penguins_mass_kg.drop(columns=["body_mass_g"])
print(penguins_mass_kg)