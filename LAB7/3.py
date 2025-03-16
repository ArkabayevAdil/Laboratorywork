import pygame
pygame.init()

w,h = 500,500
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Moving ball")

White = (255,255,255)
Red = (255,0,0)

Radious = 25
x, y = w//2, h//2
Step = 2
running = True
while running:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x - Radious - Step >= 0:
        x -= Step
    if keys[pygame.K_RIGHT] and x + Radious + Step <= w:
        x += Step
    if keys[pygame.K_UP] and y - Radious - Step >= 0:
        y -= Step
    if keys[pygame.K_DOWN] and y + Radious + Step <= h:
        y += Step

    screen.fill(White)
    pygame.draw.circle(screen, Red, (x,y), Radious)
    pygame.display.flip()
pygame.quit()

