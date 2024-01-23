import imageio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import os


def funcion(x):
    return x**2 - x**2 * math.sin(math.radians(x))

# se decodifica la cadena de bits 
def binario_decimal(binary_str):
    try:
        if binary_str:
            return int(binary_str, 2)
        else:
            return 0
    except ValueError:
        print(
            f"Error: La cadena no es válida.")
        return 0
    
# cadena de bits ¿ramdom con los numeros de bits necesarios
def generar_numero_binario(length):
    return ''.join(random.choice('01') for _ in range(length))

# ordenar la población según las evaluaciones
def ordenar_poblacion(poblacion, evaluaciones):
    return [individuo for _, individuo in sorted(zip(evaluaciones, poblacion))]

# Función para seleccionar un porcentaje de los mejores individuos como padres
def seleccionar_mejores_ind(poblacion, evaluaciones, porcentaje, tipoRes):
    poblacion_ordenada = ordenar_poblacion(poblacion, evaluaciones)

    if tipoRes == "Minimización":
        num_padres = int(porcentaje * len(poblacion_ordenada))
        # Selecciona los primeros num_padres individuos (los de evaluaciones más bajas)
        return poblacion_ordenada[:num_padres]
    else:
        num_padres = int(porcentaje * len(poblacion_ordenada))
        # Selecciona los últimos num_padres individuos (los de evaluaciones más altas)
        return poblacion_ordenada[-num_padres:]

def cruza(parejas_nuevas):
    descendencia = []
    for i, pareja in enumerate(parejas_nuevas):
        padre, individuo = pareja
        num_cortes = 1
        posiciones_cortes = sorted(random.sample(
            range(1, min(len(padre), len(individuo)) + 1), num_cortes))
        subcadena_padre = ''
        subcadena_individuo = ''
        alternar = True

        for j in range(len(posiciones_cortes) + 1):
            posicion_corte_inicial = 0 if j == 0 else posiciones_cortes[j - 1]
            posicion_corte_final = posiciones_cortes[j] if j < len(
                posiciones_cortes) else len(padre)

            if alternar:
                subcadena_padre += str(
                    padre[posicion_corte_inicial:posicion_corte_final])
                subcadena_individuo += str(
                    individuo[posicion_corte_inicial:posicion_corte_final])
            else:
                subcadena_padre += str(
                    individuo[posicion_corte_inicial:posicion_corte_final])
                subcadena_individuo += str(
                    padre[posicion_corte_inicial:posicion_corte_final])

            alternar = not alternar

        descendencia.extend([subcadena_padre, subcadena_individuo])
    return descendencia



def anadir_individuos(poblacion, nuevos_individuos):
    return poblacion + nuevos_individuos

def mutacion(individuo, prob_mut_ind, prob_mut_gen):
    individuo_inicial = individuo
    individuo_mutado = ''
    posiciones_mutadas = []

    if random.random() < prob_mut_ind:
        for i, bit in enumerate(individuo):
            if random.random() < prob_mut_gen:
                bit = '1' if bit == '0' else '0'
                posiciones_mutadas.append(i)
            individuo_mutado += bit

        if posiciones_mutadas:
            for bits_cambiados in posiciones_mutadas:
                posicion1 = random.randint(0, len(individuo_mutado) - 1)
                individuo_mutado = list(individuo_mutado)
                individuo_mutado[bits_cambiados], individuo_mutado[
                    posicion1] = individuo_mutado[posicion1], individuo_mutado[bits_cambiados]
                individuo_mutado = ''.join(individuo_mutado)
    else:
        individuo_mutado = individuo_inicial

    return individuo_mutado

def mejor_individuo(evaluaciones, tipoRes):
    
    if tipoRes == "Minimización":
        return evaluaciones.index(min(evaluaciones))
    else:
        return evaluaciones.index(max(evaluaciones))

def poda(poblacion, evaluaciones, pob_max, tipoRes):
    mejor_individuo_mt = mejor_individuo(
        evaluaciones, tipoRes)
    mejor_individuo_mutado = poblacion[mejor_individuo_mt]

    poblacion_ordenada = list(set(poblacion))
    poblacion_ordenada.remove(mejor_individuo_mutado)
    if len(poblacion_ordenada) > pob_max - 1:
        
        poblacion_ordenada = random.sample(
            poblacion_ordenada, pob_max - 1)
    poblacion_ordenada.append(mejor_individuo_mutado)
    return poblacion_ordenada


def grafica_evolucion(todas_generaciones, a, delta_x, funcion, mejor_evolucion, promedio, peor_evolucion, tipoRes):
    x_vals = np.arange(1, len(todas_generaciones) + 1)

    fitness_mejor = [min([funcion(a + binario_decimal(individuo) * delta_x) for individuo in generacion]) if tipoRes == "Minimización" else max(
        [funcion(a + binario_decimal(individuo) * delta_x) for individuo in generacion]) for generacion in todas_generaciones]
    fitness_promedio = [np.mean([funcion(a + binario_decimal(individuo) * delta_x)
                                for individuo in generacion]) for generacion in todas_generaciones]
    fitness_peor = [max([funcion(a + binario_decimal(individuo) * delta_x) for individuo in generacion]) if tipoRes == "Minimización" else min(
        [funcion(a + binario_decimal(individuo) * delta_x) for individuo in generacion]) for generacion in todas_generaciones]

    mejor_evolucion.append(fitness_mejor)
    promedio.append(fitness_promedio)
    peor_evolucion.append(fitness_peor)

    plt.plot(
        x_vals, mejor_evolucion[-1], label='Mejores individuos', color='green', marker='o')
    plt.plot(x_vals, promedio[-1],
             label='Promedio Individuos', color='purple', marker='s')
    plt.plot(x_vals, peor_evolucion[-1],
             label='Peor Individuo', color='red', marker='*')

    # Añadir etiquetas y leyenda
    plt.xlabel('Generación')
    plt.ylabel('funcion(x)')
    plt.xticks(x_vals)
    plt.legend()
    plt.title(
            f'Evolución de la Aptitud de la Población')

    # Mostrar la gráfica
    plt.savefig(f'./images/grafica_aptitud.png')
    plt.show()

def grafica_ind_gen(individuos_generacion, a, b, delta_x, funcion,  tipoRes ):
    num_gen = len(individuos_generacion)

    for generacion in range(num_gen):
        # Calcular los valores 
        x_valores = np.linspace(
            a - 0.1 * (b - a), b + 0.1 * (b - a), 1000)
        y_valores = [funcion(x) for x in x_valores]
        plt.plot(x_valores, y_valores,
                label='Función Costo', color='black', linestyle='--')
        poblacion = individuos_generacion[generacion]
        
        x_vals_generacion = [
            a + binario_decimal(str(individuo)) * delta_x for individuo in poblacion]
        y_vals_generacion = [funcion(x) for x in x_vals_generacion]

       
        plt.scatter(x_vals_generacion, y_vals_generacion,
                    label=f'Generación {generacion + 1} - Individuos', marker='o')

        mejor_individuo_generacion_index = mejor_individuo(
            [funcion(a + binario_decimal(individuo) * delta_x) for individuo in poblacion], tipoRes)
        mejor_individuo_generacion = poblacion[mejor_individuo_generacion_index]
        mejor_x = a + binario_decimal(mejor_individuo_generacion) * delta_x
        plt.scatter(mejor_x, funcion(mejor_x), color='green', marker='+',
                    label=f'Mejor Individuo - Gen {generacion + 1}')

        peor_individuo_generacion_index = mejor_individuo(
            [funcion(a + binario_decimal(individuo) * delta_x) for individuo in poblacion], "max" if tipoRes == "min" else "min")
        peor_individuo_generacion = poblacion[peor_individuo_generacion_index]
        peor_x = a + binario_decimal(peor_individuo_generacion) * delta_x
        plt.scatter(peor_x, funcion(peor_x), color='red', marker='x',
                    label=f'Peor Individuo - Gen {generacion + 1}')
        plt.xlabel('x')
        plt.ylabel('funcion(x)')
        plt.legend()
        plt.title(f'Población de Individuos Generación {generacion + 1}')

        # Guardar o mostrar la gráfica según tus necesidades
        plt.savefig(f'./images/generacion_{generacion + 1}.png')
        plt.show()

def crear_video(images_path,iteraciones, output_path, fps):
    images = []
    num_gen= iteraciones

    for i in range(1, num_gen + 1):
        image_path = os.path.join(images_path, f"generacion_{i}.png")
        images.append(imageio.imread(image_path))

    video_path = output_path
    imageio.mimsave(video_path, images, fps=fps)

def algoritmo_gen(pob_min, pob_max, prob_mut_ind, prob_mut_gen, res, tipoRes, rango_Ax, rango_Bx, iteraciones, labelFx, comboBoxEliminacion, comboBoxMostrarGrafica):
    a = rango_Ax
    b = rango_Bx
    poblacion_inicial = pob_min
    poblacion_maxima = pob_max
    func_fx = labelFx.get()
    safe_delete = comboBoxEliminacion.get()
    show_graphic = comboBoxMostrarGrafica.get()
    delta_x = res
    porcentaje_seleccion = 0.25
    num_gen = iteraciones
    tipoRes = tipoRes.get()
    rango = b - a
    num_saltos = rango/delta_x
    todas_generaciones = []
    descendencia_mut=[]
    datos_estadisticos = []
    probabilidad_mutacion_individuo = prob_mut_ind
    probabilidad_mutacion_gen = prob_mut_gen
    mejor_individuo_global = None
    mejor_evaluacion_global = float('inf')
    mejor_evolucion = []
    promedio = []
    peor_evolucion = []
    print("\nPob_min:", pob_min, "\nPob_max", pob_max, "Prob_mut_ind", prob_mut_ind, "Prob_mut_gen", prob_mut_gen, "Resolución", res, "Hallar x por:", tipoRes, "Rango a", rango_Ax, "Rango B", rango_Bx, "Iteraciones", iteraciones, "f(x)", func_fx, "Eliminacion limpia", safe_delete, "Venta de grafica", show_graphic)
    num_bits = math.ceil(math.log2(num_saltos))
    delta_x1 = rango / ((2**num_bits) - 1)
    mejor_individuo_global = None
    mejor_evaluacion_global = float('inf')

    if delta_x1 < delta_x:
        delta_x = delta_x1

    poblacion = [generar_numero_binario(
        num_bits) for _ in range(poblacion_inicial)]

    for generacion in range(num_gen):
        evaluaciones = [funcion(a + binario_decimal(individuo) * delta_x)
                        for individuo in poblacion]
        todas_generaciones.append(poblacion.copy())

        generacion_str = str(generacion + 1).zfill(len(str(iteraciones)))
        print(f"Generando {generacion_str} / {iteraciones}")
    
        for i, individuo in enumerate(poblacion):
            x = a + binario_decimal(individuo) * delta_x
            posicion_individuo = binario_decimal(individuo)
            

        seleccionados = list(set(seleccionar_mejores_ind(
            poblacion, evaluaciones, porcentaje_seleccion, tipoRes)))
          

        mejor_individuo_generacion_index = mejor_individuo(
            evaluaciones, tipoRes)
        mejor_individuo_generacion = poblacion[mejor_individuo_generacion_index]
        mejor_evaluacion_generacion = evaluaciones[mejor_individuo_generacion_index]

        # Actualización del mejor individuo global si es necesario
        if tipoRes == "Minimización" and mejor_evaluacion_generacion < mejor_evaluacion_global:
            mejor_individuo_global = mejor_individuo_generacion
            mejor_evaluacion_global = mejor_evaluacion_generacion
        elif tipoRes == "Maximización" and mejor_evaluacion_generacion > mejor_evaluacion_global:
            mejor_individuo_global = mejor_individuo_generacion
            mejor_evaluacion_global = mejor_evaluacion_generacion

        combinaciones = set()
        parejas_nuevas = []

        for i, padre in enumerate(seleccionados):
            for j, individuo in enumerate(poblacion):
                if padre != individuo and ((i, j) not in combinaciones and (j, i) not in combinaciones):
                    parejas_nuevas.append((padre, individuo))
                    combinaciones.add((i, j))

        
        print(f"Parejas formadas en > Generación {iteraciones} <\n{parejas_nuevas} ")
        descendencia = cruza(parejas_nuevas)
        print(f"Resultado de cruza > Generación {iteraciones} <\n{descendencia}")
        descendencia_mutada = [mutacion(individuo, probabilidad_mutacion_individuo, probabilidad_mutacion_gen) for individuo in descendencia]
        print(f"Resultadod de la mutación > Generación {iteraciones} <\n{descendencia}")
        # Agregar nuevos individuos a la población existente
        poblacion = anadir_individuos(poblacion, descendencia_mutada)
        descendencia_mut.append(poblacion.copy())
        
        datos = {
            'Id': list(range(1, len(poblacion) + 1)),
            'Individuo': poblacion,
            'i': [binario_decimal(individuo) for individuo in poblacion],
            'x': [a + binario_decimal(individuo) * delta_x for individuo in poblacion],
            'f(x)': [funcion(a + binario_decimal(individuo) * delta_x) for individuo in poblacion]
        }

        print("datos", datos)

        df_generacion = pd.DataFrame(datos)

        if generacion == 0:
            
            df_generacion.to_csv(f'./excel/datos_estadisticos{generacion + 1}.csv', index=False)
        else:
            
            df_generacion.to_csv(f'./excel/datos_estadisticos{generacion + 1}.csv', index=False)
            
        poblacion = poda(
            poblacion, evaluaciones, pob_max, tipoRes)
        
        
        mejor_evolucion.append([min([funcion(a + binario_decimal(individuo) * delta_x)
                               for individuo in generacion]) for generacion in todas_generaciones])
        promedio.append([np.mean([funcion(a + binario_decimal(individuo) * delta_x)
                                  for individuo in generacion]) for generacion in todas_generaciones])
        peor_evolucion.append([max([funcion(a + binario_decimal(individuo) * delta_x) for individuo in generacion]) if tipoRes ==
                              "Minimización" else min([funcion(a + binario_decimal(individuo) * delta_x) for individuo in generacion]) for generacion in todas_generaciones])


    grafica_evolucion(todas_generaciones, a, delta_x, funcion,
                    mejor_evolucion, promedio, peor_evolucion, tipoRes)
    # Llamar a la función grafica_ind_gen con el mejor individuo global
    grafica_ind_gen(descendencia_mut, a, b, delta_x, funcion, tipoRes)


def eliminar_archivos_carpeta(carpeta):
    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(carpeta)

    # Iterar sobre los archivos y eliminar cada uno
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        try:
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
            elif os.path.isdir(ruta_archivo):
                eliminar_archivos_carpeta(ruta_archivo)  # Llamada recursiva para carpetas internas
        except Exception as e:
            print(f"No se pudo eliminar {ruta_archivo}: {e}")

# Especifica la carpeta que contiene los archivos a eliminar
# carpeta_a_limpiar = './excel'

# Llama a la función para eliminar archivos en la carpeta especificada
# eliminar_archivos_carpeta(carpeta_a_limpiar)