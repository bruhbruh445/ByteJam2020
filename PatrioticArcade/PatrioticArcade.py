import pygame

 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
bg = pygame.image.load("bg.png")

left = False
right = False
walk_count = 0
 
# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
 
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 30
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .21
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -12.5
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.max_x_vel = -6
        x_accel = -6
        self.change_x += x_accel
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.max_x_vel = 6
        x_accel = 25
        self.change_x += x_accel
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        
 
        self.rect = self.image.get_rect()
 
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
        screen.blit(bg, (0,0))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -8200


        # Array with width, height, x, and y of platform
        level = [ #base level floor
                 [1000, 1080, -1000, 0],
                 [2953, 80, 0, 900],
                 [635, 80, 3048, 900], 
                 [2743, 80, 3819, 900], 
                 [2300, 80, 6647, 900],
                 #pipes
                 [83, 452, 1202, 752],
                 [83, 409, 1631, 709],
                 [83, 366, 1973, 666],
                 [83, 366, 2445, 666],
                 [83, 452, 6989, 752],
                 #[83, 452, 7675, 452],
                 #stair blocks 1
                 [45, 276, 5702, 838],
                 [45, 276, 5745, 795],
                 [45, 246, 5788, 752],
                 [45, 276, 5831, 709],
                 [45, 276, 5874, 666],
                 #stair blocks 2
                 [45, 276, 6001, 666],
                 [45, 276, 6044, 709],
                 [45, 276, 6087, 752],
                 [45, 276, 6130, 795],
                 [45, 276, 6173, 838],
                 #stair block set 3
                 [45, 276, 6302, 838],
                 [45, 276, 6345, 795],
                 [45, 246, 6388, 752],
                 [45, 276, 6431, 709],
                 [45, 276, 6474, 666],
                 [45, 276, 6517, 666],
                 #stair blocks set 4
                 [45, 276, 6647, 666],
                 [45, 276, 6687, 709],
                 [45, 276, 6728, 752],
                 [45, 276, 6771, 795],
                 [45, 276, 6814, 838],
                 #stair block set 5
                 [45, 576, 7717, 838],
                 [45, 576, 7760, 795],
                 [45, 546, 7803, 752],
                 [45, 576, 7845, 709],
                 [45, 576, 7888, 666],
                 [45, 576, 7931, 623],
                 [45, 576, 7974, 580],
                 [45, 576, 8017, 537],
                 [45, 576, 8060, 494],
                 [45, 576, 8103, 494],
                 #making bricks
                 [43, 43, 858,  665],
                 [43, 43, 944,  665],
                 [43, 43, 1030, 665],
                 [43, 43, 3299, 665],
                 [43, 43, 3385, 665],
                 [43, 43, 3430, 493],
                 [43, 43, 3473, 493],
                 [43, 43, 3516, 493],
                 [43, 43, 3559, 493],
                 [43, 43, 3602, 493],
                 [43, 43, 3645, 493],
                 [43, 43, 3688, 493],
                 [43, 43, 3731, 493],
                 [43, 43, 3901, 493],
                 [43, 43, 3944, 493],
                 [43, 43, 3987, 493],
                 [43, 43, 4030, 665],
                 [43, 43, 4287, 665],
                 [43, 43, 4330, 665],
                 [43, 43, 5058, 665],
                 [43, 43, 5187, 493],
                 [43, 43, 5230, 493],
                 [43, 43, 5273, 493],
                 [43, 43, 5488, 493],
                 [43, 43, 5574, 493],
                 [43, 43, 5617, 493],
                 [43, 43, 5531, 665],
                 [43, 43, 5574, 665],
                 [43, 43, 7202, 665],
                 [43, 43, 7245, 665],
                 [43, 43, 7331, 665],
                 
                 #Question Mark Blocks
                 [43, 43, 685, 665],
                 [43, 43, 901, 665],
                 [43, 43, 987, 665],
                 [43, 43, 943, 493],
                 [43, 43, 3342, 665],
                 [43, 43, 4030, 493],
                 [43, 43, 4544, 665],
                 [43, 43, 4672, 665],
                 [43, 43, 4672, 493],
                 [43, 43, 4800, 665],
                 [43, 43, 5531, 493],
                 [43, 43, 7288, 665],


                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -8200
 
        # Array with type of platform, and x, y location of the platform.
        level = [[9000, 70, 0, 580],
                 [310, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Side-scrolling Platformer")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 300
    player.rect.y = 520
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 900:
            diff = player.rect.right - 900
            player.rect.right = 900
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 500:
            diff = 500 - player.rect.left
            player.rect.left = 500
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()