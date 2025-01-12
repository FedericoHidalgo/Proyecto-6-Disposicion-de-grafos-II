import math, random
import pygame

# Parámetros de la ventana
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 4
ITERATIONS = 100
FPS = 30

# Colores
BACKGROUND_COLOR = (30, 30, 30)
NODE_COLOR = (200, 100, 100)
EDGE_COLOR = (100, 100, 200)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruchterman-Reingold con math y Pygame")
clock = pygame.time.Clock()

# Grafo de ejemplo (lista de aristas)
graph = [(0, 1), (1, 2), (0, 3), (1,4), (2,5), (3,4), (4,5), (3,6), (4,7), (5,8), (6,7), (7,8)]
num_nodes = 9

# Posiciones iniciales de los nodos (aleatorias dentro de la ventana)
#positions = {i: [math.floor(random.random() * WIDTH), math.floor(random.random() * HEIGHT)] for i in range(num_nodes)}
positions = {0: [713, 32], 1: [612, 528], 2: [281, 67], 3: [204, 316], 4: [107, 561], 5: [224, 531], 6: [104, 273], 7: [426, 369], 8: [639, 15]}

# Constantes para las fuerzas
area = WIDTH * HEIGHT
k = math.sqrt(area / num_nodes)  # Espaciado ideal entre nodos
temperature = WIDTH / 10        # Temperatura inicial
cooling_factor = temperature / ITERATIONS  # Factor de enfriamiento

def euclidean_distance(pos1, pos2):
    """Calcula la distancia euclidiana entre dos posiciones."""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx**2 + dy**2)

def repulsive_force(distance):
    """Fuerza de repulsión entre nodos."""
    return k**2 / distance if distance > 0 else 0

def attractive_force(distance):
    """Fuerza de atracción entre nodos conectados."""
    return distance**2 / k

def fruchterman_reingold_step(positions, graph, temperature):
    """Realiza un paso del algoritmo Fruchterman-Reingold."""
    forces = {i: [0, 0] for i in positions}
    
    # Calcular fuerzas de repulsión
    for i in positions:
        for j in positions:
            if i != j:
                delta_x = positions[i][0] - positions[j][0]
                delta_y = positions[i][1] - positions[j][1]
                distance = euclidean_distance(positions[i], positions[j])
                force = repulsive_force(distance)
                #print(f"Nodos: {i},{j} \tD: {distance}, \tdX: {delta_x}, \tdY: {delta_y} \tF:{force}")
                if distance > 0:
                    forces[i][0] += (delta_x / distance) * force
                    forces[i][1] += (delta_y / distance) * force
                #print(f"Fzas en nodos {i}: {forces[i][0]}, {forces[i][1]}")
    print("\n\n")
    # Calcular fuerzas de atracción
    for u, v in graph:
        delta_x = positions[u][0] - positions[v][0]
        delta_y = positions[u][1] - positions[v][1]
        distance = euclidean_distance(positions[u], positions[v])
        force = attractive_force(distance)
        #print(f"Arista: {u}-{v} \tD: {distance}, \tF: {force}")
        if distance > 0:
            forces[u][0] -= (delta_x / distance) * force
            forces[u][1] -= (delta_y / distance) * force
            forces[v][0] += (delta_x / distance) * force
            forces[v][1] += (delta_y / distance) * force
        #print(f"Fzs {u}: {forces[u]}, Fzs {v}: {forces[v]}")
    print("\n\n")
    # Actualizar posiciones
    for i in positions:
        displacement_x = forces[i][0]
        displacement_y = forces[i][1]
        displacement_magnitude = math.sqrt(displacement_x**2 + displacement_y**2)
        if displacement_magnitude > 0:
            positions[i][0] += (displacement_x / displacement_magnitude) * min(displacement_magnitude, temperature)
            positions[i][1] += (displacement_y / displacement_magnitude) * min(displacement_magnitude, temperature)
            #posX = positions[i][0] + (displacement_x / displacement_magnitude) * min(displacement_magnitude, temperature)
            #posY = positions[i][1] + (displacement_y / displacement_magnitude) * min(displacement_magnitude, temperature)
        # Limitar posiciones dentro de los bordes
        positions[i][0] = min(WIDTH-25, max(25, positions[i][0]))
        positions[i][1] = min(HEIGHT-25, max(25, positions[i][1]))
        #positions[i][0] = min(WIDTH-25, max(25, posX))
        #positions[i][1] = min(HEIGHT-25, max(25, posY))
        print(f"Posición {i} X,Y: {positions[i][0]}, {positions[i][1]}")

    return positions

# Bucle principal de visualización
running = True
iteration = 0
iteracion = 1
while running and iteration < iteracion: #ITERATIONS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar pantalla
    screen.fill(BACKGROUND_COLOR)

    # Dibujar aristas
    for u, v in graph:
        pygame.draw.line(
            screen, EDGE_COLOR,
            (positions[u][0], positions[u][1]),
            (positions[v][0], positions[v][1]), 2
        )

    # Dibujar nodos
    for pos in positions.values():
        pygame.draw.circle(screen, NODE_COLOR, (int(pos[0]), int(pos[1])), NODE_RADIUS)

    # Ejecutar un paso del algoritmo Fruchterman-Reingold
    positions = fruchterman_reingold_step(positions, graph, temperature)

    # Reducir la temperatura
    temperature -= cooling_factor

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(FPS)
    iteration += 1

# Salir de Pygame
pygame.quit()
