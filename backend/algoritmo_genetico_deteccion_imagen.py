import random as rd
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Definir los parámetros para el procesamiento de imágenes
def getIndividuo():
    # Cada individuo tiene parámetros de brillo, contraste, umbral (filtros)
    return [rd.uniform(0.5, 1.5),  # Brillo
            rd.uniform(0.5, 1.5),  # Contraste
            rd.uniform(0, 255)]    # Umbral para la detección de bordes

# Definir población
def getPoblacion(numero):
    return [getIndividuo() for i in range(numero)]

# Función de evaluación del individuo (fitness)
def CalcularAdaptacion(individuo, img):
    # Descomponer el individuo en sus parámetros
    brillo, contraste, umbral = individuo

    # Procesar la imagen aplicando los valores del individuo
    enhancer = ImageEnhance.Brightness(img)
    img_bright = enhancer.enhance(brillo)

    enhancer = ImageEnhance.Contrast(img_bright)
    img_contrast = enhancer.enhance(contraste)

    img_gray = img_contrast.convert("L")  # Escala de grises
    img_edge = img_gray.filter(ImageFilter.FIND_EDGES)

    # Convertir la imagen en un array numpy para evaluar
    img_array = np.array(img_edge)
    
    # Aplicar umbral para contar bordes detectados
    edge_count = np.sum(img_array > umbral)

    # Fitness es el número de píxeles con bordes detectados
    return edge_count

# Cruce (mezclar parámetros entre padres)
def cruce(lPoblacion, lPadres):
    for i in range(len(lPoblacion)-1):
        puntoCruce = rd.randint(0, len(lPoblacion[0]) - 1)
        lPoblacion[i][:puntoCruce] = lPadres[0][1][:puntoCruce]
        lPoblacion[i][puntoCruce:] = lPadres[1][1][puntoCruce:]
    return lPoblacion

# Mutación (modificar aleatoriamente los parámetros)
def mutacion(listaCruzados, probMutacion=0.8):
    for i in range(len(listaCruzados)-1):
        if rd.random() <= probMutacion:
            punto = rd.randint(0, len(listaCruzados[0])-1)
            nuevo_valor = rd.uniform(0.5, 1.5) if punto < 2 else rd.randint(0, 255)
            listaCruzados[i][punto] = nuevo_valor
    return listaCruzados

# Cargar imagen para procesamiento
def run_genetic_algorithm(image_path):
    # Cargar imagen
    img = Image.open(image_path)

    # Parámetros iniciales
    tamanoPoblacion = 10
    numMejores = 5
    iteraciones = 100
    probMutacion = 0.8

    # Generar población inicial
    listaPoblacion = getPoblacion(tamanoPoblacion)

    for j in range(iteraciones):
        # Calculo de la adaptación
        listaValorados = [(CalcularAdaptacion(i, img), i) for i in listaPoblacion]
        listaOrdenados = sorted(listaValorados, reverse=True)

        # Selección de los mejores individuos
        listaSeleccionados = listaOrdenados[:numMejores]
        listaPadres = rd.sample(listaSeleccionados, 2)

        # Cruce de la población
        listaPoblacionCruzada = cruce(listaPoblacion, listaPadres)

        # Aplicar mutación
        listaPoblacionMutada = mutacion(listaPoblacionCruzada)

        # Actualizar población
        listaPoblacion = listaPoblacionMutada

    # Seleccionar el mejor individuo después de todas las iteraciones
    listaMejores = sorted([(CalcularAdaptacion(i, img), i) for i in listaPoblacion], reverse=True)
    mejor_individuo = listaMejores[0]

    print("\nMejor individuo después de " + str(iteraciones) + " iteraciones")
    print("Parámetros: Brillo: {}, Contraste: {}, Umbral: {}".format(
        mejor_individuo[1][0], mejor_individuo[1][1], mejor_individuo[1][2]))
    print("Fitness (bordes detectados):", mejor_individuo[0])

    return mejor_individuo[1]
