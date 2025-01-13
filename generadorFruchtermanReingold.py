import pygame, math, random
from generadorModelos import *

# Parámetros generales
ancho, alto = 1900, 1000  # Tamaño de la ventana
radioNodo = 4          # Radio de los nodos
iteraciones = 1000          # Número máximo de iteraciones
FPS = 30                  # Frames por segundo
reloj = pygame.time.Clock()
pantalla = pygame.display.set_mode((ancho, alto))

# Colores
colorFondo = (30, 30, 30)
colorNodo = (50, 150, 250)
colorArista = (200, 200, 200)

# Inicializar posiciones de los nodos aleatoriamente
def posicionesIniciales(g, ancho, alto):
    """"
    Obtiene las posiciones iniciales de los nodos
    """
    posiciones = {nodo: (random.randint(50, ancho - 50),\
                         random.randint(50, alto - 50)) for nodo in g["nodos"]}
       
    return posiciones

def distanciaEuclidiana(pos1,pos2):
    """
    Calcula la distancia euclidiana entre dos puntos
    """
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx**2 + dy**2)

def fuerzaRepulsiva(d, k):
    """
    Calcula la fuerza de repulsión entre dos nodos
    """
    return k**2 / d if d > 0 else 0

def fuerzaAtractiva(d, k):
    """
    Calcula la fuerza de atracción entre dos nodos 
    conectados por una arista
    """
    return d**2 / k

def fruchtermanReingold(posiciones, g, temperatura, k):
    """
    Método Fruchterman Reingold para la visualización de grafos
    """
    fuerzas = {nodo: [0,0] for nodo in g["nodos"]}
    # Calcular fuerzas de repulsión entre todos los pares de nodos
    for n1 in g["nodos"]:
        for n2 in g["nodos"]:
            if n1 != n2:
                deltaX = posiciones[n1][0] - posiciones[n2][0]
                deltaY = posiciones[n1][1] - posiciones[n2][1]
                distancia = distanciaEuclidiana(posiciones[n1], posiciones[n2])
                fuerza = fuerzaRepulsiva(distancia, k)
                if distancia > 0:
                    fuerzas[n1][0] += (deltaX / distancia) * fuerza
                    fuerzas[n1][1] += (deltaY / distancia) * fuerza       
            
    # Calcular fuerzas de atracción para las aristas del grafo
    for e in g["aristas"]:
        n1, n2 = e
        deltaX = posiciones[n1][0] - posiciones[n2][0]
        deltaY = posiciones[n1][1] - posiciones[n2][1]
        distancia = distanciaEuclidiana(posiciones[n1], posiciones[n2])
        fuerza = fuerzaAtractiva(distancia, k)
        if distancia > 0:
            fuerzas[n1][0] -= (deltaX / distancia) * fuerza
            fuerzas[n1][1] -= (deltaY / distancia) * fuerza
            fuerzas[n2][0] += (deltaX / distancia) * fuerza
            fuerzas[n2][1] += (deltaY / distancia) * fuerza
    # Actualizar posiciones de los nodos
    for n in g["nodos"]:
        despX = fuerzas[n][0]
        despY = fuerzas[n][1]
        desp = math.sqrt(despX ** 2 + despY ** 2)
        if desp > 0:
            posiciones[n] = ((posiciones[n][0] + (despX / desp) * min(desp, temperatura)),\
                            (posiciones[n][1] + (despY / desp) * min(desp, temperatura)))
        posiciones[n] = (min(ancho-25, max(25, posiciones[n][0] )),\
                        min(alto-25, max(25, posiciones[n][1])))
    #Imprimir grafo en pantalla
    actualizarPantalla(pantalla, g, posiciones)
    
    return posiciones

# Dibujar grafo con Pygame
def actualizarPantalla(pantalla, g, posiciones):
    pantalla.fill(colorFondo)
    # Dibujar aristas
    for e in g["aristas"]:
        n1, n2 = e
        pygame.draw.line(pantalla, colorArista, posiciones[n1], posiciones[n2], 2)
    
    # Dibujar nodos
    for pos in posiciones.values():
        pygame.draw.circle(pantalla, colorNodo, (int(pos[0]), int(pos[1])), radioNodo)

    pygame.display.flip()
    reloj.tick(FPS)

def modeloFruchtermanReingold():
    """
    Ejecutar el modelo Fruchterman Reingold
    """
    # Inicializar Pygame
    pygame.init()
    pygame.display.set_caption("Disposición de grafos - Algoritmo Fruchterman-Reingold")

    # Bucle principal de visualización
    ejecucion = True
    bandera = 0
    #Modelo de grafo
    n= 10
    modelo= modeloMalla(n,n)
    # Obtenemos los nodos y aristas del modelo
    nodos = []
    aristas = []
    for i in modelo.nodos.values():
        nodos.append(i)
    for i in modelo.aristas.values():
        e = modelo.nodoVecino(i)
        aristas.append(e)
    # Creamos el grafo
    g = {
        "nodos": nodos,
        "aristas": aristas,
    }
    # Obtenemos las posiciones iniciales de los nodos
    posiciones = posicionesIniciales(g, ancho, alto)
    # Constantes para las fuerzas
    k = math.sqrt((ancho * alto) / len(g["nodos"])/4)/2  # Espaciado ideal entre nodos
    temperatura = ancho / 100                 # Temperatura inicial
    factorEnf = temperatura / iteraciones  # Factor de enfriamiento


    while ejecucion and bandera < iteraciones:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecucion = False

        # Ejecutar un paso del algoritmo Fruchterman-Reingold
        posiciones = fruchtermanReingold(posiciones, g, temperatura, k)

        # Reducir la temperatura
        temperatura -= factorEnf

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(FPS)
        bandera += 1

    # Salir de Pygame
    pygame.quit()
