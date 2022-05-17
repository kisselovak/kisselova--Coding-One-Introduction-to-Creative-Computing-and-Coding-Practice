# Final pong game for: Coding One: Introduction to Creative Computing and Coding Practice
# By Katie Kiselova


from pygame.locals import *
import pygame
import random
import time

WIDTH = 640
HEIGHT = 500

# PONG CLASS OBJECT 
class Pong(object):
    
    # Constructor functions
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Python Pong")
        
        # Class Variables
        
        # Display Setup
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg_color = (0,0,0)
        
        # Initial Position of Ball and Paddles Setup
        self.ball_x = 320
        self.ball_y = 240
        self.left_paddle_mv = self.right_paddle_mv = self.centery = 240
        self.rad = 12
        self.paddle_height = 120
        self.paddle_width = 20
        self.ball_rect = pygame.Rect(self.ball_x,self.ball_y, self.rad*2, self.rad*2)
        
        # Colors for Balls, Paddles, Texts
        self.color = (39, 239, 67)        # GREEN
        self.title_color = (0, 0, 255)    #  BLUE
        
        

        # Directions, hits Vars
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.speed = 2
        self.hit_edge_left = False
        self.hit_edge_right = False
        
        # Information and Score Area
        self.info_area = (0.15 * HEIGHT)  
        self.game_area_top = self.info_area
        self.game_area_bottom = HEIGHT 
        self.score = [0, 0]

    # Function For Info Area and Scores
    def info(self):
        
        # Draw divider line
        pygame.draw.rect(self.display, self.color, (0, self.info_area - 5, WIDTH, 5))
        
        # Printing Scores and Instructions
        pygame.font.init()
        font = pygame.font.SysFont("agencyfb", 20)
        font2 = pygame.font.SysFont("ubuntumono", 21, bold=True)
        
        # Score for left paddle: Player A
        left_label = font.render("Player A: %d" %self.score[0], 1, self.color)
        self.display.blit(left_label, (45, 13))
        
        # Score for left paddle: Player B
        right_label = font.render("Player B: %d" %self.score[1], 1, self.color)
        self.display.blit(right_label, (530, 13))
        
      
        # Title 
        title = font2.render("1v1 Pong Game", 1, self.title_color)
        self.display.blit(title, (240, 5))

    # Function For Right Paddle 
    def right_paddle(self): 
           
        # Input from user 
        key = pygame.key.get_pressed()
        if key[K_UP]:
            self.right_paddle_mv = self.right_paddle_mv - 7
        if key[K_DOWN]:
            self.right_paddle_mv = self.right_paddle_mv + 7

        # Limiting the posible y positons so that paddle doesn't go off window
        if self.right_paddle_mv <= self.game_area_top:
            self.right_paddle_mv = self.game_area_top
        if self.right_paddle_mv + self.paddle_height >= self.game_area_bottom:
            self.right_paddle_mv = self.game_area_bottom - self.paddle_height

        # Draw right paddle after updateing its y position
        pygame.draw.rect(self.display, self.color,
                         (WIDTH - self.paddle_width,    # for right paddle to be at far right of the window
                         self.right_paddle_mv, self.paddle_width, self.paddle_height)
                        )

    # Function For Left Paddle
    def left_paddle(self): 
          
        # Input from user
        key = pygame.key.get_pressed()
        if key[K_w]:
            self.left_paddle_mv = self.left_paddle_mv - 7
        if key[K_s]:
            self.left_paddle_mv = self.left_paddle_mv + 7

        # Limiting the posible y positons so that paddle doesn't go off window 
        if self.left_paddle_mv <= self.game_area_top:
            self.left_paddle_mv = self.game_area_top
        if self.left_paddle_mv + self.paddle_height >= self.game_area_bottom:
            self.left_paddle_mv = self.game_area_bottom - self.paddle_height

        # draw left paddle as we update its y position
        pygame.draw.rect(self.display, self.color,
                         (0,         # 0 because paddle is on far left of the window
                         self.left_paddle_mv, self.paddle_width, self.paddle_height)
                        )     

    # Function for Ball
    def update_ball(self):
        self.ball_x += self.speed * self.direction[0]
        self.ball_y += self.speed * self.direction[1]
    
        self.ball_rect = pygame.Rect(self.ball_x,self.ball_y, self.rad*3,self.rad*3)
        self.ball_rect.centerx = self.ball_x + self.rad
        self.ball_rect.centery = self.ball_y - self.rad
        
        # Change direction of puck if it hits the right paddle
        if (self.ball_rect.centerx + self.rad >= WIDTH - self.paddle_width) and (self.ball_rect.centerx + self.rad <= WIDTH - 1):
            if (self.ball_rect.centery + (self.rad/1) >= self.right_paddle_mv) and (self.ball_rect.centery <= self.right_paddle_mv + self.paddle_height - (self.rad/1)):
                self.direction[0] = -1


        # If puck hits right side, change direct of puck
        # Set variable for score keeping to True 
        if (self.ball_rect.centerx + self.rad >= WIDTH):
            self.direction[0] = -1
            self.hit_edge_left = True
          
            
        # Change direction of puck if it hits the left paddle
        if (self.ball_rect.centerx - self.rad <= self.paddle_width) and (self.ball_rect.centerx - self.rad >= 0):
            if (self.ball_rect.centery + (self.rad/2) >= self.left_paddle_mv) and (self.ball_rect.centery <= self.left_paddle_mv + self.paddle_height - (self.rad/2)):
                self.direction[0] = 1
              

        # If puck hits left side, change direct of puck
        # Set variable for score keeping to True 
        if(self.ball_rect.centerx - self.rad <= 0):
            self.direction[0] = 1
            self.hit_edge_right = True
            

        # Change direction of puck when it hits the top or bottom 
        # For top
        if self.ball_rect.centery + 10 <= self.game_area_top:
            self.direction[1] = 1
        
        # For bottom
        if self.ball_rect.centery + 40 >= self.game_area_bottom:
            self.direction[1] = -1
           

		# Draw puck!
        pygame.draw.rect(self.display, self.color, (self.ball_x, self.ball_y, self.rad*2, self.rad*2))
        
        tally = [0, 0]
        if self.hit_edge_left:
            tally[0] += 1
            self.hit_edge_left = False
            
                          
            
        if self.hit_edge_right:
            tally[1] += 1
            self.hit_edge_right = False
            
       
        
        self.score[0] = self.score[0] + tally[0]
        self.score[1] = self.score[1] + tally[1]
    
    def reset_board(self):
        self.ball_x = 320
        self.ball_y = 240
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        time.sleep(0.3)

    def reset_game(self):
        # Initialize keyboard listener
        key = pygame.key.get_pressed()

        # On pressing Return/Enter or Escape key, reset game 
        if key[K_RETURN] or key[K_SPACE]:
            self.ball_x = 320
            self.ball_y = 240
            self.left_paddle_mv = self.right_paddle_mv = random.randint(300,340)
            self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
            self.score = [0, 0]
            time.sleep(0.5)

# Main Function to run the game
if __name__ == "__main__":
    
    print("|- Pong Game By Katie K -|")  
    print("****************************************************") 
    print("Press mouse on the screen to start playing.")
    
    print("Player A the left side: Press W or S to move up and down.")
    
    print("Player B the right side: Press ArrowUp or ArrowDown to move up and down.")
    
    print("****************************************************")
    
    clock = pygame.time.Clock()
    game = Pong()
    status = True

    while status:
        clock.tick(64)

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if pressed[K_ESCAPE]:
                status = False
            if event.type == QUIT:
                status = False

        game.display.fill(game.bg_color)
        game.info()
        game.right_paddle() 
        game.left_paddle()
        game.update_ball()
        pygame.display.flip()
        game.reset_game()
        pygame.event.pump()
    pygame.quit()