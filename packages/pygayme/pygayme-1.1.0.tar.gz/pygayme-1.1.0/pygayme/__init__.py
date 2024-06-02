import pygame

pygame.init()

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("pygayme")

clock = pygame.time.Clock()

dt = 0

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

  
    screen.fill((255, 255, 255)) # Background Color

    # Content to draw
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 600, 100))
    pygame.draw.rect(screen, (255, 140, 0), (0, 100, 600, 100))
    pygame.draw.rect(screen, (255, 255, 0), (0, 200, 600, 100))
    pygame.draw.rect(screen, (0, 255, 0), (0, 300, 600, 100))
    pygame.draw.rect(screen, (0, 0, 255), (0, 400, 600, 100))
    pygame.draw.rect(screen, (255, 0, 255), (0, 500, 600, 100))
    

    pygame.display.flip()
    dt = clock.tick(60) # Change this to FPS

pygame.quit()