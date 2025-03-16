import pygame
import sys
import datetime
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Mickey Clock")
rightarm = pygame.image.load("image/hand1.png")
leftarm = pygame.image.load("image/hand2.png")
main = pygame.transform.scale(pygame.image.load("image/body.png"), (800, 600))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    now = datetime.datetime.now()
    minute = now.minute
    second = now.second
    screen.fill((255, 255, 255))
    m_angle = -(minute * 6 + (second / 60) * 6)  
    s_angle = -(second * 6) 
    screen.blit(main, (0, 0))
    r_rotate = pygame.transform.rotate(pygame.transform.scale(rightarm, (150, 400)), m_angle)
    r_center = r_rotate.get_rect(center=(400, 300))
    screen.blit(r_rotate, r_center)
    l_rotate = pygame.transform.rotate(pygame.transform.scale(leftarm, (100, 350)), s_angle)
    l_center = l_rotate.get_rect(center=(400, 300))
    screen.blit(l_rotate, l_center)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
