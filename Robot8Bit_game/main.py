import pygame
from pygame.locals import *

from sprites import *
from config import *

pygame.init()

# Nueva ventana
playgame = False

# Opciones del menu
menu = ["Jugar", "Salir"]
select = 0

# Ventana Principal
ventana = pygame.display.set_mode((1024,840))
clock = pygame.time.Clock()
pygame.display.set_caption("Menu Principal")

# Para el bucle
jugando = True

# Fondo de pantalla mapa
background = pygame.image.load("images/menu.jpg").convert()
level1_image = pygame.image.load("images/level1.jpg").convert()

# Musica de fondo principal
pygame.mixer.music.load("sonidos/intro.mp3")
pygame.mixer.music.play(-1)

# Carga de musica primer nivel
def level1_music():
    pygame.mixer.music.load("sonidos/level1.mp3")
    pygame.mixer.music.play(-1)

# Método de menu principal
def menu_principal():
    global playgame
    fuente_menu = pygame.font.Font("font/AncientModernTales-a7Po.ttf", 38)

    ventana.blit(background, [0, 0])  # Dibuja el fondo fuera del bucle del menú

    for i, opcion in enumerate(menu):
        color = (213,213,213)
        if i == select:
            texto\
                = fuente_menu.render("> " + opcion, True, (255, 0, 0))
        else:
            texto = fuente_menu.render(opcion, True, color)

        # Se dibuja el menú en el centro de la pantalla
        text_rect = texto.get_rect(center=(ventana.get_width() // 2, 200 + i * 50))
        ventana.blit(texto, text_rect)

# Jugar
def play_game():
    global playgame
    player1 = Robot()
    ostaculo1 = Obstaculo()
    ventana.fill((0, 0, 0))
    pygame.display.set_caption("Level 1")
    pygame.display.flip()
    level1_music()

    while playgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playgame = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player1.mover_derecha=True
                elif event.key == pygame.K_LEFT:
                    player1.mover_izquierda=True
                elif event.key == pygame.K_UP:
                    player1.mover_arriba=True
                elif event.key == pygame.K_DOWN:
                    player1.mover_abajo=True
                elif event.key == pygame.K_ESCAPE:
                    playgame = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player1.mover_derecha = False
                elif event.key == pygame.K_LEFT:
                    player1.mover_izquierda = False
                elif event.key == pygame.K_UP:
                    player1.mover_arriba = False
                elif event.key == pygame.K_DOWN:
                    player1.mover_abajo = False

        player1.mover()
        ventana.fill((0, 0, 0))
        ventana.blit(player1.image1, player1.position)
        if player1.mover_derecha:
            ventana.blit(player1.image2, player1.position)
        if player1.mover_izquierda:
            ventana.blit(player1.image1, player1.position)
        pygame.display.flip()
        clock.tick(60)

# Menú Principal
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                select = (select - 1) % len(menu)
            elif event.key == pygame.K_DOWN:
                select = (select + 1) % len(menu)
            elif event.key == pygame.K_RETURN:
                if select == 1:  # Comprueba si la opción seleccionada es "Salir" y si lo es, sale del juego
                    pygame.quit()
                elif select == 0:
                    playgame = True
                    jugando = False
                    pygame.mixer.music.fadeout(1000)
                    play_game()

    if not playgame:
        menu_principal()
    else:
        play_game()

    pygame.display.flip()
    clock.tick(60)

# Cerrar el juego
pygame.mixer.music.stop()  # Detener la música al salir del bucle
pygame.quit()
