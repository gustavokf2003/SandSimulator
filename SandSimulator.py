import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from copy import deepcopy

# Mapa de cores (Branco = Parede, Preto = Fundo, Amarelo = Areia)
cores = mcolors.ListedColormap(['black', 'yellow', 'white'])

# Inicializa a figura
plt.ion()  
fig, ax = plt.subplots()

# Função para atualizar a visualização
def show_matrix(matrix):
    ax.clear()
    ax.imshow(matrix, cmap=cores, interpolation='nearest')
    ax.set_xticks([])  
    ax.set_yticks([]) 
    plt.draw()
    plt.pause(0.001) 
    plt.show()

# Função para obter os vizinhos de uma célula
def get_neighbors(matrix, i, j):
    return {
        # Vizinhos de distância 1
        "up": matrix[i - 1][j],
        "down": matrix[i + 1][j],
        "left": matrix[i][j - 1],
        "right": matrix[i][j + 1],
        "center": matrix[i][j],
        "up_left": matrix[i - 1][j - 1],
        "up_right": matrix[i - 1][j + 1],
        "down_left": matrix[i + 1][j - 1],
        "down_right": matrix[i + 1][j + 1],
        # Vizinhos de distância 2
        "up_up": matrix[i - 2][j],
        "down_down": matrix[i + 2][j],
        "left_left": matrix[i][j - 2],
        "right_right": matrix[i][j + 2],
        "up_left_2": matrix[i - 2][j - 2],
        "up_right_2": matrix[i - 2][j + 2],
        "down_left_2": matrix[i + 2][j - 2],
        "down_right_2": matrix[i + 2][j + 2],

        "up_up_left": matrix[i - 2][j - 1],
        "up_up_right": matrix[i - 2][j + 1],
        "down_down_left": matrix[i + 2][j - 1],
        "down_down_right": matrix[i + 2][j + 1],
        "left_left_up": matrix[i - 1][j - 2],
        "right_right_down": matrix[i + 1][j + 2],
    }

# Função para desenhar um círculo na matrix
def draw_circle(matrix, center, radius, value):
    cx, cy = center
    for x in range(cx - radius, cx + radius + 1):
        for y in range(cy - radius, cy + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                matrix[x][y] = value

# Inicializa a matrix
MATRIX_SIZE = 100
matrix = [[0 for i in range(MATRIX_SIZE + 3)] for j in range(MATRIX_SIZE + 3)]

# Inicializa as bordas da matrix
for i in range(MATRIX_SIZE + 3):
    matrix[0][i] = 2
    matrix[1][i] = 2
    matrix[MATRIX_SIZE+1][i] = 2
    matrix[MATRIX_SIZE+2][i] = 2
    matrix[i][0] = 2
    matrix[i][1] = 2
    matrix[i][MATRIX_SIZE+1] = 2
    matrix[i][MATRIX_SIZE+2] = 2


# Desenha um círculo de raio 10 no centro da matrix
draw_circle(matrix, (MATRIX_SIZE // 2, MATRIX_SIZE // 2), 10, 1)

NUMBER_GENERATIONS = 1000

# Começa a simulação
for g in range(NUMBER_GENERATIONS):
    matrix_aux = deepcopy(matrix)

    for i in range(2, MATRIX_SIZE+1):
        for j in range(2, MATRIX_SIZE + 1):
            neighborns = get_neighbors(matrix, i, j)
            matrix_aux[i][j] = matrix[i][j]
            
            # Conjunto de regras
            if neighborns["center"] == 1 and neighborns["down"] == 0:
                matrix_aux[i][j] = 0
            elif neighborns["center"] == 0 and neighborns["up"] == 1:
                matrix_aux[i][j] = 1
            elif (neighborns["center"] == 1 and neighborns["down"] == 1 and neighborns["left"] == 0 and neighborns["down_left"] == 0 and 
                (neighborns["down_down_left"] == 1 or neighborns["down_down_left"] == 2)):
                matrix_aux[i][j] = 0
            elif (neighborns["up_right"] == 1 and neighborns["right"] == 1 and neighborns["up"] == 0 and neighborns["center"] == 0  and 
                (neighborns["down"] == 1 or neighborns["down"] == 2)):
                matrix_aux[i][j] = 1
            elif (neighborns["center"] == 1 and neighborns["down"] == 1 and neighborns["right"] == 0 and neighborns["down_right"] == 0 and 
                (neighborns["down_down_right"] == 1 or neighborns["down_down_right"] == 2) and neighborns["down_left"] == 1):
                matrix_aux[i][j] = 0
            elif (neighborns["up_left"] == 1 and neighborns["left"] == 1 and neighborns["up"] == 0 and neighborns["center"] == 0  and 
                (neighborns["down"] == 1 or neighborns["down"] == 2) and neighborns["left_left"] == 1):
                matrix_aux[i][j] = 1

    matrix = deepcopy(matrix_aux)
    show_matrix(matrix)
