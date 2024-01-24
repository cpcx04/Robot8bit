import pygame
from robot import Robot

pygame.init()

# Nueva ventana
playgame = False

# Opciones del menu
menu = ["Jugar", "Salir"]
select = 0

# Ventana Principal
ventana = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Menu Principal")

# Para el bucle
jugando = True

# Fondo de pantalla mapa
background = pygame.image.load("images/mapa.png").convert()
level1_image = pygame.image.load("images/level1.jpg").convert()

# Musica de fondo principal
pygame.mixer.music.load("sonidos/intro.mp3")
pygame.mixer.music.play(-1)

# Carga de musica primer nivel
def level1_music():
    pygame.mixer.music.load("sonidos/level1.mp3")
    pygame.mixer.music.play(-1)

# Metodo de menu principal
def menu_principal():
    global playgame
    fuente_menu = pygame.font.Font("font/AncientModernTales-a7Po.ttf", 38)

    ventana.blit(background, [0, 0])  # Dibuja el fondo fuera del bucle del menú

    for i, opcion in enumerate(menu):
        color = (0, 255, 0)
        if i == select:
            texto = fuente_menu.render("> " + opcion, True, (255, 0, 0))
        else:
            texto = fuente_menu.render(opcion, True, color)

        # Se dibuja el menu en el centro de la pantalla
        text_rect = texto.get_rect(center=(ventana.get_width() // 2, 200 + i * 50))
        ventana.blit(texto, text_rect)

# Jugar
# Jugar
def play_game():
    global playgame
    ventana.fill((0, 0, 0))
    ventana.blit(level1_image, [0, 0])
    pygame.display.set_caption("Level 1")
    pygame.display.flip()
    level1_music()
    player1 = Robot()
    while playgame:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player1.move_right()
                if event.key == pygame.K_LEFT:
                    player1.move_left()
                if event.key == pygame.K_ESCAPE:
                    playgame = False


# Menu Principal
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
