import pygame

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

# Cargar música del menú principal fuera del bucle
pygame.mixer.music.load("sonidos/intro.mp3")
pygame.mixer.music.play(-1)  # El valor -1 indica reproducir en bucle



pygame.mixer.music.load("sonidos/intro.mp3")
pygame.mixer.music.play(-1)


def level1_music():
    pygame.mixer.music.load("sonidos/level1.mp3")
    pygame.mixer.music.play(-1)


def menu_principal():
    global playgame  # Necesitas declarar la variable como global para modificarla dentro de la función
    fuente_menu = pygame.font.Font("font/AncientModernTales-a7Po.ttf", 38)

    ventana.blit(background, [0, 0])  # Dibuja el fondo fuera del bucle del menú

    for i, opcion in enumerate(menu):
        color = (0, 255, 0)
        if i == select:
            texto = fuente_menu.render("> " + opcion, True, (255, 0, 0))
        else:
            texto = fuente_menu.render(opcion, True, color)

    # Dibujamos
        text_rect = texto.get_rect(center=(ventana.get_width() // 2, 200 + i * 50))
        ventana.blit(texto, text_rect)


def play_game():
    global playgame
    ventana.fill((0, 0, 0))
    ventana.blit(level1_image, [0, 0])
    level1_music()


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
                    pygame.mixer.music.fadeout(1000)
                    play_game()

    if not playgame:
        menu_principal()

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()  # Detener la música al salir del bucle
pygame.quit()
