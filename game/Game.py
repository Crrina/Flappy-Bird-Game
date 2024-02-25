import sys
import pygame
import random
from game.Bird import Bird
from Pipe import Pipe
from constants import *

''''
The Game module, where there is the main method to start the game.
It is responsible for controlling the game, drawing game elements,
checking if the game is over, keeping score count.
'''


class Game:

    """
    Initialize the game and the game speed. The background image is loaded and the bird and pipes list are initialised.
    The score is set to 0.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        # convert is used to convert a image that does not have transparent background
        self.background_image = pygame.image.load('../assets/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bird = Bird(100, SCREEN_HEIGHT // 2, 2) #bird object
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.running = True

    """
    Displays the start screen, which leads to the game when the space key is pressed.
    The game runs in loop until the user loses.
    """
    def run(self):
        self.start_screen()
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw_elements()
            self.clock.tick(120)
        self.end_game()

    """
    Handle events like quitting, mouse clicks and key presses.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.flap(FLAP_POWER)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap(FLAP_POWER)

    """
    Updates the bird position and generates new pipes at intervals during the game.
    Moves the pipes and removes the off-screen pipes from their list. Increments score for
    passing pipes. At the end it checks for collisions.
    """
    def update_game(self):
        self.bird.update(GRAVITY)
        if pygame.time.get_ticks() - self.last_pipe_time > PIPE_FREQUENCY:
            pipe_height = random.randint(250, 500)
            self.create_pipe(SCREEN_WIDTH, pipe_height, False)
            self.create_pipe(SCREEN_WIDTH, pipe_height - PIPE_GAP, True)
            self.last_pipe_time = pygame.time.get_ticks()

        for pipe in self.pipes:
            pipe.move()
        offscreen_pipes = [pipe for pipe in self.pipes if pipe.rect.right < 0]
        # Check if any pipes have gone off-screen and remove them
        self.pipes = [pipe for pipe in self.pipes if pipe.rect.right >= 0]
        # Increment score if a pipe has passed the bird's position
        if len(offscreen_pipes) > 0:
            self.score += 1
        self.check_collisions()

    """
    Adds to the pipes list the new created pipe.
    """
    def create_pipe(self, x, y, is_top):
        self.pipes.append(Pipe(x, y, is_top))

    """
    Ends game if bird collides with pipe or goes off screen.
    """
    def check_collisions(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect):
                self.game_over()
                return
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over()

    """
    Terminates the game, by breaking from the run loop.
    """
    def game_over(self):
        self.running = False

    """
    Draw background, bird, pipes and score.
    """
    def draw_elements(self):
        self.screen.blit(self.background_image, (0, 0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.draw_score()
        pygame.display.update()

    """
    Renders the score, formats it and draws it.
    """
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

    """
    Creates the welcome screen at the beginning of the game with instructions.
    """
    def start_screen(self):
        start_font = pygame.font.Font(None, 40)
        x = start_font.render('Welcome to my Flappy Bird Game!', True, (255, 255, 255))
        y = start_font.render('You can play using the space key or the mouse', True, (255, 255, 255))
        z = start_font.render('Press any key to start', True, (255, 255, 255))
        self.start_end_screen(x, y, z)

    """
    Formats the text from the start and end screen and shows it. Waits for the user key press to continue.
    """
    def start_end_screen(self, x, y, z):
        image = pygame.transform.scale(pygame.image.load('../assets/bird.png').convert_alpha(),
                                       (int(50 * 10), int(35 * 10)))
        s1 = x.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        s2 = y.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        s3 = z.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.4))
        self.screen.fill((135, 206, 235))
        self.screen.blit(image, (SCREEN_WIDTH / 3.4, SCREEN_HEIGHT / 2.4))
        self.screen.blit(x, s1)
        self.screen.blit(y, s2)
        self.screen.blit(z, s3)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    """
    End screen text that is shown when game is over.
    """
    def end_game(self):
        # creates a new font
        start_font = pygame.font.Font(None, 40)
        # creates the text using that font, True is used to make the text smoother
        x = start_font.render('You Lost!', True, (255, 255, 255))
        y = start_font.render(f'Your score is: {self.score}', True, (255, 255, 255))
        z = start_font.render('To play again press any key', True, (255, 255, 255))
        self.start_end_screen(x, y, z)
        games = Game()
        games.run()


#Starts the game.
if __name__ == "__main__":
    game = Game()
    game.run()



