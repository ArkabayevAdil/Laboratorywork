import pygame

pygame.mixer.init()
pygame.init()

done = False
songs = [
    (r"song\Miras.mp3", 
     r"Previos\Miras.jpg"),

    (r"song\Kairat.mp3", 
     r"Previos\Kairat.jpeg"),

    (r"song\Aikyn.mp3",
     r"Previos\Aikyn.jpeg")
]

bg = pygame.image.load(songs[0][1])
width, height = bg.get_size()
screen = pygame.display.set_mode((width, height))

pygame.mixer.music.load(songs[0][0])
pygame.mixer.music.play()
i = 0
a = True
screen.blit(bg, (0, 0))
pygame.display.flip()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                i = (i + 1) % len(songs)
                pygame.mixer.music.load(songs[i][0])
                pygame.mixer.music.play()
                
                # Загружаем новое изображение
                bg = pygame.image.load(songs[i][1])
                width, height = bg.get_size()
                
                # Меняем размер окна
                screen = pygame.display.set_mode((width, height))
                screen.blit(bg, (0, 0))
                pygame.display.flip()
                
            elif event.key == pygame.K_LEFT:
                i = (i - 1) % len(songs)
                pygame.mixer.music.load(songs[i][0])
                pygame.mixer.music.play()
                
                # Загружаем новое изображение
                bg = pygame.image.load(songs[i][1])
                width, height = bg.get_size()
                
                # Меняем размер окна
                screen = pygame.display.set_mode((width, height))
                screen.blit(bg, (0, 0))
                pygame.display.flip()
                
            elif event.key == pygame.K_SPACE:
                if a:
                    pygame.mixer.music.stop()
                    a = False
                else:
                    pygame.mixer.music.play()
                    a = True

pygame.quit()