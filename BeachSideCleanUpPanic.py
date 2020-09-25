# https://realpython.com/pygame-a-primer/
# https://www.pygame.org/docs/ref/event.html#pygame.event.get

# Import and initialize the pygame library
import pygame
import random
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([800, 500])
pygame.display.set_caption("Beachside Cleanup Panic")

# Assets
left = False
right = False
up = False
down = False
stop = False
counter = [0,1]
clock = pygame.time.Clock()
sand = pygame.image.load('sand.png')
ocean = pygame.image.load('ocean1.png')
sky = pygame.image.load('sky.png')

# Classes
class player(pygame.sprite.Sprite):
  stand = [pygame.image.load('playersprite1.png'), pygame.image.load('playersprite2.png'), pygame.image.load('playersprite3.png'), pygame.image.load('playersprite4.png')]

  def __init__(self, x, y, width, height):
    super().__init__() # calling pygame.sprite.Sprite's init 
    self.image = pygame.Surface([width, height])
    self.image.fill((255,0,0))

    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.vel = 7
    self.hitbox = (self.x, self.y, self.width, self.height)

    self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 

  def draw(self):
    screen.blit(self.stand[0], (self.x, self.y))
    # pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class trash(pygame.sprite.Sprite):
  trashSprite = [pygame.image.load('trash1.png'), pygame.image.load('trash2.png')]

  def __init__(self, x, y, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill((255,0,0))

    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.hitbox = (self.x, self.y, self.width, self.height)

    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

  def draw(self):
    screen.blit(self.trashSprite[0], (self.x, self.y))
    # pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))
       

class turtle(pygame.sprite.Sprite):
  turtleWalk = [pygame.image.load('turtlesprite1.png'), pygame.image.load('turtlesprite2.png')]

  def __init__(self, x, y, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill((100,0,0))

    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.vel = 2
    self.hitbox = (self.x, self.y, self.width, self.height)

    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
  def draw(self, screen):
    for x in counter:
      screen.blit(self.turtleWalk[x], (self.x,self.y))
      # pygame.draw.rect(screen, (150, 0, 0), self.hitbox, 2)
      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


trash_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
turtle_list = pygame.sprite.Group()

# Garbage Loop
trashCount = 0

while trashCount < 100: # 100
  garbage = trash(random.randint(400,750), random.randint(200,450), 50, 50)
  trash_list.add(garbage)
  
  trashCount += 1

turtleSprite = turtle(0,250,114,69)
avatar = player(350,300,60,80)
player_list.add(avatar)


# Main Loop
running = True
while running:
  while not stop:
    clock.tick(27)
    # Did the user click the window close button?
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Background
    screen.blit(sky,(0,0))
    screen.blit(ocean,(0,0))
    screen.blit(sand, (0,0))

    for x in trash_list: # draws/displays each garbage
      x.draw()

    # Turtle Movement
    turtleSprite.draw(screen)
    pygame.display.update()
    turtleSprite.x += turtleSprite.vel
    turtleSprite.hitbox = (turtleSprite.x, turtleSprite.y, turtleSprite.width, turtleSprite.height)

    # print(avatar.rect) # prints the coordinates of avatar rectangle

    # Player Movement
    keys = pygame.key.get_pressed()
    avatar.draw()
    pygame.display.update()
        
    if keys[pygame.K_LEFT] and avatar.x > avatar.vel:
      avatar.x -= avatar.vel
      left = True
      right = False
      up = False
      down = False
      
    if keys[pygame.K_RIGHT] and avatar.x < 800 - avatar.width - avatar.vel:
      avatar.x += avatar.vel
      left = False
      right = True
      up = False
      down = False

    if keys[pygame.K_DOWN] and avatar.y < 500 - avatar.height - avatar.vel:
      avatar.y += avatar.vel
      left = False
      right = False
      up = False
      down = True

    if keys[pygame.K_UP] and avatar.y > 250 - avatar.height - avatar.vel:
      avatar.y -= avatar.vel
      left = False
      right = False
      up = True
      down = False
    avatar.hitbox = (avatar.x, avatar.y, avatar.width, avatar.height)

    # Pick Up Garbage
    if keys[pygame.K_SPACE]:
      # See if the player block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(avatar, trash_list, True)

    # Are ya winning son?
    if len(trash_list) == 0: # trash_list array length
      print('You won! All the trash got cleaned up!')
      stop = True
    elif pygame.sprite.spritecollideany(turtleSprite, trash_list):
    # pygame.sprite.collide_rect(turtleSprite, trash_list):
      print('You lost! The turtle ate some trash!')
      stop = True

# Done! Time to quit.
pygame.quit()
