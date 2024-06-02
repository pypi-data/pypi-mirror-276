import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])
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

    pygame.display.flip()
    dt = clock.tick(60) # Change this to FPS

pygame.quit()