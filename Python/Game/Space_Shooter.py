import pygame
from os.path import join, dirname, abspath # import join, dirname, abspath functions

from random import randint, uniform # import randint and uniform functions
# Get the directory where this script is located
BASE_DIR = dirname(abspath(__file__))

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join(BASE_DIR, "5games-main", "space shooter", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300


        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
    
        # mask
        #self.mask = pygame.mask.from_surface(self.image) #not needed if you added the mask in collision function


    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            print(current_time)
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                    self.can_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt


        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
                Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
                self.can_shoot = False 
                self.laser_shoot_time = pygame.time.get_ticks()
                laser_sound.play()

        self.laser_timer()

   
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups): #pos = position where the laser should be created
        super().__init__(groups) 
        self.image = surf   
        self.rect = self.image.get_frect(midbottom = pos)   
        

    def update(self, dt):
         self.rect.centery -= 400 * dt
         if self.rect.bottom < 0:  #laser above the screen - not visible anymore
            self.kill()  #removes the sprite from all groups
    
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups) # initializes the sprite and adds it to the specified groups
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000 
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1) #random direction vector
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0
        

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill() #removes the sprite from all groups
        self.rotation += self.rotation_speed * dt #updates the rotation angle based on the rotation speed and delta time
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1) #rotates the image based on the rotation angle; 1 = no scaling
        self.rect = self.image.get_frect(center = self.rect.center) #keeps the center of the rect the same after rotation

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index] #sets the initial image to the first frame
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt 
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)] #override self.image with the current frame based on the frame index
        else:
            self.kill() #removes the sprite from all groups when the animation is done



def collisions(): # checks for collisions between player, meteors, and lasers
    global running, game_over # allows the function to modify the running variable defined outside the function
    
    collision_sprites = (pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)) #checks for collision between player and meteors; if collides, the meteor is removed
    if collision_sprites:
        game_over = True #sets game_over to True if the player collides with any meteor
        damage_sound.play() #plays the damage sound when the player collides with a meteor
        
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True) #checks for collision between laser and meteors; if collides, the meteor is removed
        if collided_sprites:
            laser.kill() #removes the laser if it collides with any meteor
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites) #creates an explosion at the position of the laser when it collides with a meteor
            explosion_sound.play() #plays the explosion sound when a meteor is hit by a laser

def display_score():
    current_time = pygame.time.get_ticks()  // 1000  # converts milliseconds to seconds
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20,10).move(0, -8) , 5, 10)

def draw_start_screen():
    display_surface.fill('#3a2e3f')
    title_surf = font.render("Space Shooter", True, (240, 240, 240))
    title_rect = title_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
    display_surface.blit(title_surf, title_rect)

    button_surf = font.render("START", True, (0, 0, 0))
    button_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2, 200, 60)
    pygame.draw.rect(display_surface, (240, 240, 240), button_rect)
    display_surface.blit(button_surf, button_surf.get_rect(center=button_rect.center))
    pygame.display.update()
    return button_rect

def draw_game_over_screen():
    display_surface.fill('#3a2e3f')
    over_surf = font.render("GAME OVER", True, (240, 0, 0))
    over_rect = over_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
    display_surface.blit(over_surf, over_rect)

    button_surf = font.render("RESTART", True, (0, 0, 0))
    button_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2, 200, 60)
    pygame.draw.rect(display_surface, (240, 240, 240), button_rect)
    display_surface.blit(button_surf, button_surf.get_rect(center=button_rect.center))
    pygame.display.update()
    return button_rect

# General Setup
pygame.init()  # initializes all the pygame modules
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720  # sets the width and height of the game in pixels
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # creates the main displau window with the specififc size
pygame.display.set_caption('Space Shooter') # Sets the title of the game to this
running = True  # creates a boolean variabel and sets it to true. Typicaaly used to control the main game loop
clock = pygame.time.Clock() #can control the frame rate


# import
star_surf = pygame.image.load(join(BASE_DIR, "5games-main", "space shooter", "images", "star.png")).convert_alpha()
#loads the meteor image from the relative path and converts it for optimal display
meteor_img_path = join(BASE_DIR, "5games-main", "space shooter", "images", "meteor.png")
meteor_surf = pygame.image.load(meteor_img_path).convert_alpha()
#loads the laser image from the relative path and voncerts it for optimal dispaly
laser_img_path = join(BASE_DIR, "5games-main", "space shooter", "images", "laser.png")
laser_surf = pygame.image.load(laser_img_path).convert_alpha()
#import font
font = pygame.font.Font(join(BASE_DIR, "5games-main", "space shooter", "images", "Oxanium-Bold.ttf"), 40)
#import all explosion frames
explosion_frames = [pygame.image.load(join(BASE_DIR, "5games-main", "space shooter", "images", "explosion", f'{i}.png')).convert_alpha() for i in range(21)] #up to 21 but not including 21
# import sounds
laser_sound = pygame.mixer.Sound(join(BASE_DIR, "5games-main", "space shooter", "audio", "laser.wav"))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join(BASE_DIR, "5games-main", "space shooter", "audio", "explosion.wav"))
damage_sound = pygame.mixer.Sound(join(BASE_DIR, "5games-main", "space shooter", "audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join(BASE_DIR, "5games-main", "space shooter", "audio", "game_music.wav"))
game_music.set_volume(0.4)
game_music.play(loops= -1) #plays the game music in an infinite loop

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range (20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


#main game loop: checks for the window close event to stop the game
game_active = False
game_over = False

while not game_active:
    button_rect = draw_start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                game_active = True


while running:
    if game_over:
        button_rect = draw_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Reset game state here
                    all_sprites.empty()
                    meteor_sprites.empty()
                    laser_sprites.empty()
                    for i in range(20):
                        Star(all_sprites, star_surf)
                    player = Player(all_sprites)
                    game_over = False
                    game_active = True
        continue
    
    
    
    dt =clock.tick() / 1000 #if empty it gives the maximun that each computer can run normally in milliseconds; dt(delta time - time it took your computer to render the current frame 1/120 frame)
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites)) #creates a meteor at a random x position above the screen

    # update
    all_sprites.update(dt)
    collisions()


    # Draw the game
    display_surface.fill('#3a2e3f')
    display_score()
    
    all_sprites.draw(display_surface)
    
    pygame.display.update() # updates the display

pygame.quit() # quits the pygame and closes the game window when the loop ends