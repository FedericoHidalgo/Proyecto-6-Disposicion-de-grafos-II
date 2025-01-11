import pygame, math, random
from generadorModelos import *
from generadorGrafos import Grafo

# Configuración de pantalla
ancho, alto = 1900, 1000
radioNodo = 4
colorArista = (200, 200, 200)
colorNodo = (50, 150, 250)
colorFondo = (30, 30, 30)
reloj = pygame.time.Clock()
FPS = 240

# Algoritmo de resortes
def fzaAtractiva(d, k):
    """
    Calcula la fuerza de atracción entre dos nodos 
    conectados por una arista
    """
    return (d ** 2) / k

def fzaRepulsiva(d, k):
    """
    Calcula la fuerza de repulsión entre dos nodos
    """
    return k ** 2 / d if d > 0 else k ** 2

# Inicializar posiciones y fuerzas
def posicionesIniciales(g, ancho, alto):
    """
    Obtiene posiciones iniciales aleatorias para los nodos
    """
    posiciones = {nodo: (random.randint(50, ancho - 50), random.randint(50, alto - 50))\
                  for nodo in g["nodos"]}
    return posiciones

def Spring(g, posiciones, ancho, alto, pantalla=None):
    """
    Método Spring para la visualización de grafos
    """
    k = math.sqrt((250 * 230) / (len(g["nodos"])/ 2))/2  # Constante de distancia óptima
    # Calcular fuerzas repulsivas
    fuerzas = {nodo: [0, 0] for nodo in g["nodos"]}
    for n1 in g["nodos"]:
        for n2 in g["nodos"]:
            if n1 != n2:
                x1, y1 = posiciones[n1]
                x2, y2 = posiciones[n2]
                dx, dy = x2 - x1, y2 - y1
                distancia = math.sqrt(dx**2 + dy**2)
                fuerza = fzaRepulsiva(distancia, k)
                angulo = math.atan2(dy, dx)
                fuerzas[n1][0] -= math.cos(angulo) * fuerza
                fuerzas[n1][1] -= math.sin(angulo) * fuerza

    # Calcular fuerzas atractivas
    for e in g["aristas"]:
        n1, n2 = e
        x1, y1 = posiciones[n1]
        x2, y2 = posiciones[n2]
        dx, dy = x2 - x1, y2 - y1
        distancia = math.sqrt(dx**2 + dy**2)
        fuerza = fzaAtractiva(distancia, k)
        angulo = math.atan2(dy, dx)
        fuerzas[n1][0] += math.cos(angulo) * fuerza
        fuerzas[n1][1] += math.sin(angulo) * fuerza
        fuerzas[n2][0] -= math.cos(angulo) * fuerza
        fuerzas[n2][1] -= math.sin(angulo) * fuerza

    m = 0.001 # Factor de movimiento
    # Actualizar posiciones
    for n in g["nodos"]:
        posiciones[n] = (
            min(ancho - 25, max(25, posiciones[n][0] + fuerzas[n][0] * m)),
            min(alto - 25, max(25, posiciones[n][1] + fuerzas[n][1] * m)),
        )
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
    for n, (x, y) in posiciones.items():
        pygame.draw.circle(pantalla, colorNodo, (int(x), int(y)), radioNodo)
    pygame.display.flip()
    reloj.tick(FPS)

# Main
def main():
    #Iniciamos Pygame
    pygame.init()
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Visualización de Grafos - Método de Resortes")
    # Creamos un modelo de grafo
    n = 10
    modelo = modeloMalla(n,n)
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
    # Bucle principal
    ejecucion = True
    while ejecucion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecucion = False

        #actualizarPantalla(pantalla, g, posiciones)
        Spring(g, posiciones, ancho, alto, pantalla=pantalla)
    pygame.quit()

