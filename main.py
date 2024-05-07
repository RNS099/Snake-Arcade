import pygame, sys
from pygame.math import Vector2
import random, math

pygame.init()
pygame.font.init() 

cell_size = 20
cell_number = 40
start = False

my_font = pygame.font.SysFont('Raleway Bold', 40)
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) # we will get 600x600 window
pygame.display.set_caption('Snake Arcade')
clock = pygame.time.Clock()

class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(1, cell_number-1)
        self.pos = Vector2(self.x, self.y) # 2d vector
        
    
    def draw_fruit(self):
        # create a rect
        fruit_rect = pygame.Rect(self.pos.x*cell_size , self.pos.y*cell_size , cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)
 

    def randomize(self, sbody):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(1, cell_number-1)
        self.pos = Vector2(self.x, self.y)

        while self.pos in sbody:
            self.x = random.randint(0, cell_number-1)
            self.y = random.randint(1, cell_number-1)
            self.pos = Vector2(self.x, self.y)


class SNAKE:   
    
    def __init__(self) :
        self.body = [Vector2(5,10),  Vector2(4,10), Vector2(3,10), Vector2(2,10)]
        self.body_reset = self.body.copy()
        self.direction = Vector2(1,0)

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0,255,0), block_rect)

    def move_snake(self):
        # creates a moving simulation
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        body_copy = self.body[:] # similar to move_snake() but here we are copying the entire block
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.get_distance()
        # print((self.snake.body[0].x) , (self.snake.body[0].y))   

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize(self.snake.body)
            # add a block to snake
            self.snake.add_block()
            self.score+=1
    
    def display_stats(self, font):
        text_surface = font.render(f" SCORE | {self.score}", False, (255, 255, 255))
        screen.blit(text_surface, (1,1))


    def get_distance(self):
        # finding euclidean distance
        x , y = self.fruit.pos.x, self.fruit.pos.y
        x1, y1 = self.snake.body[0].x , self.snake.body[0].y
        dist = math.sqrt( (x-x1)**2 + (y-y1)**2 )
        
    def reset(self):
        global start
        self.snake.body = self.snake.body_reset
        self.fruit.randomize()
        self.score = 0
        start = False


    def check_fail(self):
        # check is outside of screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.reset()

        # check if snake collided itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.reset()


if __name__ == "__main__":
 
    main_game = GAME()
    SCREEN_UPDATE = pygame.USEREVENT # custom userevemt
    pygame.time.set_timer(SCREEN_UPDATE, 100) 
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                start = True
            
            if start:
            
                if event.type == SCREEN_UPDATE:
                    main_game.update()


                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                        

                    if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    

                    if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                

                    if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
       
      
        screen.fill((0,0,0))
        main_game.draw_elements()
        main_game.display_stats(my_font)

        pygame.display.update()
        clock.tick(60)