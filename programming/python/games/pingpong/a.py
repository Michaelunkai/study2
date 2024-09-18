import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
paddle_a = pygame.Rect(0, HEIGHT // 2 - PADDLE_WIDTH // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_WIDTH // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
BALL_RADIUS = 7
ball = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball.center = (WIDTH // 2, HEIGHT // 2)
ball_speed_x = 4
ball_speed_y = 4

clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Control
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= 5
    if keys[pygame.K_s] and paddle_a.bottom < HEIGHT:
        paddle_a.y += 5
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= 5
    if keys[pygame.K_DOWN] and paddle_b.bottom < HEIGHT:
        paddle_b.y += 5

    # Collision
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y
    if ball.left <= PADDLE_WIDTH and ball.top >= paddle_a.top and ball.bottom <= paddle_a.bottom:
        ball_speed_x = -ball_speed_x
    elif ball.right >= WIDTH - PADDLE_WIDTH and ball.top >= paddle_b.top and ball.bottom <= paddle_b.bottom:
        ball_speed_x = -ball_speed_x
    elif ball.left <= 0 or ball.right >= WIDTH:
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = -ball_speed_x
        ball_speed_y = -ball_speed_y

    # Update ball position
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Draw
    screen.fill(BLACK)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)

    pygame.display.flip()
    clock.tick(60)