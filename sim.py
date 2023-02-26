import pygame
import random
import math

# Define the dimensions of the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define the colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the parameters for the sprites
SPRITE_SIZE = 10
MAX_SPEED = 5
MAX_ACCELERATION = 0.1
MAX_HEALTH = 100
MAX_HUNGER = 100
MAX_AGE = 50
MAX_REPRODUCTION_CHANCE = 1
MUTATION_CHANCE = 0.05

# Define the environment parameters
FOOD_COLOR = GREEN
FOOD_AMOUNT = 1000
FOOD_SIZE = 2

# Define the game class
class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the window
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sprite Evolution")

        # Create the sprites
        self.sprites = []
        for i in range(50):
            self.sprites.append(Sprite())

        # Create the food
        self.food = []
        for i in range(FOOD_AMOUNT):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.food.append(Food(x, y))

    def run(self):
        # Run the game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the sprites
            for sprite in self.sprites:
                sprite.update(self.food, self.sprites)

            # Draw the game
            self.window.fill(WHITE)
            for sprite in self.sprites:
                sprite.draw(self.window)
            for food in self.food:
                food.draw(self.window)
            pygame.display.flip()
            pygame.time.delay(50)

        # Clean up Pygame
        pygame.quit()

# Define the sprite class
class Sprite:
    def __init__(self, x=None, y=None, speed=None, angle=None, color=None, health=None, hunger=None, age=None, reproduction_chance=None, parent=None):
        # Initialize the sprite's parameters
        if x is None:
            x = random.randint(0, WINDOW_WIDTH)
        self.x = x
        if y is None:
            y = random.randint(0, WINDOW_HEIGHT)
        self.y = y
        if speed is None:
            speed = random.uniform(0, MAX_SPEED)
        self.speed = speed
        if angle is None:
            angle = random.uniform(0, 2 * math.pi)
        self.angle = angle
        if color is None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = color
        if health is None:
            health = MAX_HEALTH
        self.health = health
        if hunger is None:
            hunger = MAX_HUNGER
        self.hunger = hunger
        if age is None:
            age = 0
        self.age = age
        if reproduction_chance is None:
            reproduction_chance = MAX_REPRODUCTION_CHANCE
        self.reproduction_chance = reproduction_chance
        self.parent = parent

    def update(self, food, sprites):
        # Update the sprite's parameters based on the environment and interactions with other sprites
        self.age += 1
        self.hunger -= 0.01
        self.health -= 0.01

        # Check for food
        for f in food:
            if self.distance_to(f) < (SPRITE_SIZE + FOOD_SIZE) / 2:
                self.hunger += 20
                food.remove(f)

        # Check for other sprites
        for s in sprites:
            if s is not self:
                if self.distance_to(s) < SPRITE_SIZE:
                    if self.color == s.color:
                        self.health += 10
                        s.health += 10
                    else:
                        self.health -= 1
                        s.health -= 1

        # Check for reproduction
        if self.age >= MAX_AGE and self.hunger >= MAX_HUNGER / 2 and random.random() < self.reproduction_chance:
            sprites.append(Sprite(x=self.x, y=self.y, speed=self.speed, angle=self.angle, color=self.color, health=self.health / 2, hunger=self.hunger / 2, age=0, reproduction_chance=self.reproduction_chance / 2, parent=self))
            self.health /= 2
            self.hunger /= 2

        # Mutate
        if random.random() < MUTATION_CHANCE:
            self.speed = min(MAX_SPEED, max(0, self.speed + random.uniform(-MAX_ACCELERATION, MAX_ACCELERATION)))
            self.angle = random.uniform(0, 2 * math.pi)
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.reproduction_chance = min(MAX_REPRODUCTION_CHANCE, max(0, self.reproduction_chance + random.uniform(-0.1, 0.1)))

        # Move
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        self.x = min(WINDOW_WIDTH, max(0, self.x + dx))
        self.y = min(WINDOW_HEIGHT, max(0, self.y + dy))

        # Check for health
        if self.hunger <= 0 or self.health <= 0:
            sprites.remove(self)

    def draw(self, surface):
        # Draw the sprite on the surface
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), SPRITE_SIZE)

    def distance_to(self, other):
        # Calculate the distance to another sprite
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.circle(surface, FOOD_COLOR, (int(self.x), int(self.y)), FOOD_SIZE)

game = Game()
game.run()

