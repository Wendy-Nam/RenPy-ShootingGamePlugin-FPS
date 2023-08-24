### Game Rules ###

# This is a first-person shooter game from the hunter's point of view.
# Configure the number of targets per round, the number of rounds, time limits for each round, and the player's life count.

# 1. The player must eliminate all targets within the time limit for each round.
# 2. Failure to eliminate a target within the time limit results in an attack on the player.
# 3. The player can shoot targets by clicking the mouse.
init python:   
    # Define the game configuration class
    class GameConfig:
        def __init__(self,
                     target_img_name='default_target',
                     target_img_path='images/targets1/',
                     target_nb=4,
                     time_limit=10,
                     life_max=3,
                     round_nb=3,
                     bullet_max=15,
                     target_speed_range=(1, 2.5),
                     target_ypos_range=(0.2, 0.8),
                     target_scale_range=(2.5, 2.5)):
            self.target_img_path = target_img_path
            self.target_img_name = target_img_name
            self.target_nb = target_nb
            self.time_limit = time_limit
            self.life_max = life_max
            self.round_nb = round_nb
            self.bullet_max = bullet_max
            self.target_speed_range = target_speed_range
            self.target_ypos_range = target_ypos_range
            self.target_scale_range = target_scale_range
    
            # Image paths for various game elements
            self.IMG_BULLET = 'hunt/imgs/bullets/bullet.png'
            self.IMG_BULLET_EMPTY = 'hunt/imgs/bullets/bullet_empty.png'
            self.IMG_AIM_IDLE = 'hunt/imgs/weapon/crosshair.png'
            self.IMG_AIM_HOVER = 'hunt/imgs/weapon/crosshair_focused.png'
            self.IMG_WEAPON = 'hunt/imgs/weapon/gun.png'
            self.IMG_HEART = 'hunt/imgs/life/heart.png'
            self.IMG_HEART_EMPTY = 'hunt/imgs/life/heart_empty.png'
            # Determine size of the weapon image
            self.IMG_SIZE_WEAPON = renpy.image_size(self.IMG_WEAPON)
            
# Initialize the game
init:
    # Define transforms for animations
    # Moving aim transform to follow the cursor
    transform moving_aim:
        function moveAim
        pause 0.01
        repeat

    # Moving target transform for target animation
    transform moving_target(target_speed=1.0, target_ypos=275, target_scale=1.0):
        zoom target_scale
        ypos target_ypos
        linear target_speed xpos 2000
        xpos -300
        repeat

    # Moving weapon transform for weapon animation
    transform moving_weapon:    
        function moveWeapon
        pause 0.01
        repeat
    
    # Alpha dissolve transform for fading effects
    transform alpha_dissolve:
        alpha 0.0
        linear 0.5 alpha 1.0
        on hide:
            linear 0.5 alpha 0

    # Screen displaying game status
    screen board():
        # Frame to display round and score information
        frame align(0, 0, 1.0):
            margin (30, 30)
            padding (15, 15)
            background "#ffffff00"
            vbox:
                # Display current round number
                text "{b}{i}Round %d{/i}{/b}  " % (hunt.status.round_now) size 35 color "#ffffff" yalign 0.5 line_spacing 5
                # Display remaining targets and total targets
                text "{b}{i}Scores: {color=#ffff00}%d{/color} / %d{/i}{/b}  " % (hunt.status.target_nb - hunt.status.target_now, hunt.status.target_nb) size 35 color "#ffffff" yalign 0.5 line_spacing 5
                # Display time left with red color if running out
                timer 1 repeat True action If(hunt.status.time_left > 0 and hunt.is_round_running == True, true=[SetVariable('hunt.status.time_left', hunt.status.time_left - 1)])
                text "{b}{i}Time Left : %d{/i}{/b}  " % (hunt.status.time_left) size 35 line_spacing 5 at alpha_dissolve:
                    if hunt.status.time_left <= 2:
                        color "#ff0000"
                    else:
                        color "#ffffff"
        # Frame to display bullet and life information
        frame align (1.0, 0.0):
            margin (30, 30)
            padding (10, 10)
            background "#4f5a6680"
            hbox:
                # Display remaining bullets
                text "{b}{i} Bullets: %d{/i}{/b}  " % hunt.status.bullet_now size 35 color "#ffffff" yalign 0.5
                # Display bullet images based on remaining bullets
                for i in range(hunt.status.bullet_max):
                    if hunt.status.bullet_max > hunt.status.bullet_now + i:
                        image hunt.config.IMG_BULLET_EMPTY:
                            xalign 0.5 yalign 0.5 rotate 15 alpha 0.5 zoom 0.7
                    else:
                        image hunt.config.IMG_BULLET:
                            xalign 0.5 yalign 0.5 rotate 15 zoom 0.7
                # Display remaining life and heart images based on life count
                text "{b}{i}Life: %d / %d{/i}{/b}  " % (hunt.status.life_now, hunt.status.life_max) size 35 color "#ff5858" yalign 0.5
                for i in range(hunt.status.life_max):
                    if hunt.status.life_max > hunt.status.life_now + i:
                        image hunt.config.IMG_HEART_EMPTY:
                            xalign 0.5 yalign 0.5 alpha 0.5 zoom 0.8
                    else:
                        image hunt.config.IMG_HEART:
                            xalign 0.5 yalign 0.5 zoom 0.8
    
    # Screen for the aim that follows the mouse
    screen gun():
        # Timer to control game time and actions
        timer 1 repeat True action If(hunt.status.time_left > 0, false=Return("timeout"))
        # Imagebutton for aim with hover effect
        imagebutton idle hunt.config.IMG_AIM_IDLE hover hunt.config.IMG_AIM_HOVER xalign 0.5 yalign 0.5 action [SetVariable('hunt.player.fired', True), Return("fired")] at moving_aim
        frame:
            background "#ffffff00"
            xalign 0.0 yalign 1.5
            image hunt.config.IMG_WEAPON at moving_weapon

init python:
    # Define transform functions

    # Transform function to move aim based on cursor position
    def moveAim(trans, at, st):
        trans.pos = trackCursor()
        trans.zoom = distance_zoom(renpy.get_mouse_pos()[1], 0.5, 1.0)
        return None

    # Transform function to move weapon based on cursor position
    def moveWeapon(trans, at, st):
        trans.zoom = distance_zoom(renpy.get_mouse_pos()[1], 0.8, base=2.0)
        trans.alpha = alpha_zoom()
        trans.pos = trackCursor(xpos_offset=int(hunt.config.IMG_SIZE_WEAPON[0]), ypos_offset=int((hunt.config.IMG_SIZE_WEAPON[1]) * 0.5))
        trans.alpha = 1 - (renpy.get_mouse_pos()[1] / config.screen_height) * 1.2
        return None
    
    # Calculate zoom based on cursor position for various elements
    def distance_zoom(ypos, mult, base):
        return (-((config.screen_height / 2 - ypos) / config.screen_height) * mult + base)
        
    # Track cursor position with optional offsets
    def trackCursor(xpos_offset=0, ypos_offset=0):
        return (renpy.get_mouse_pos()[0] - xpos_offset, renpy.get_mouse_pos()[1] - ypos_offset)

    # Calculate alpha value based on cursor position
    def alpha_zoom():
        return (1 - (renpy.get_mouse_pos()[1] / config.screen_height) * 1.2)

    # Define the main game class
    class HuntingGame:
        def __init__(self, config):
            # Initialize game elements based on provided configuration
            self.config = config
            self.player = self.Player(self.config)
            self.targets = [self.Target(self.config, i) for i in range(self.config.target_nb)]
            self.status = self.Status(self.config.target_nb, 
                                      self.config.time_limit, 
                                      self.config.life_max, 
                                      self.config.round_nb, 
                                      self.config.bullet_max)
            self.is_round_running = True
            self.is_game_running = True

        def run(self):
            # Run through rounds of the game
            for i in range(self.status.round_nb):
                if not self.is_game_running:
                    return
                self.round_init()
                while self.is_round_running and self.is_game_running:
                    self.player.attack(self.status, self.targets)
                    self.handle_events()
            return None
            
        def round_init(self):
            # Initialize round elements
            self.status.round_init()
            renpy.scene('black')
            renpy.say(who=None, what="ROUND " + str(self.status.round_now), interact=True)
            renpy.show_screen("board")
            for i in range(self.config.target_nb):
                self.targets.append(self.Target(self.config, i))
                self.targets[i].display()
            self.is_round_running = True
            
        def round_end(self, result, is_game_over=False):
            # End the current round
            self.status.round_end()
            renpy.hide_screen("board")
            self.targets.clear()
            self.is_round_running = False
            renpy.say(who=None, what=result, interact=True)
            if is_game_over:
                self.is_game_running = False
            return
        
        def handle_events(self):
            # Handle various game events
            if self.status.is_game_over():
                self.round_end("GAME OVER", True)
                return
            if self.status.is_clear():
                self.round_end("clear")
                return
            if self.status.is_time_up():
                self.round_end("time up")
                return
    
        # Define the Player class
        class Player:
            def __init__(self, config):
                # Initialize player attributes
                self.config = config
                self.hit_pos = None
                self.fired = False
    
            def attack(self, status, targets):
                # Perform player attack and hit detection
                renpy.call_screen("gun")
                self.hit_pos = [renpy.get_mouse_pos()[0], renpy.get_mouse_pos()[1]]
                for i in range(self.config.target_nb):
                    if not targets[i].killed:
                        pos = targets[i].get_pos()
                        if self.is_hit(pos, targets[i].image_size):
                            targets[i].hide()
                            targets[i].killed = True
                            status.target_now -= 1
                renpy.with_statement(vpunch)
                if self.fired:
                    status.bullet_now -= 1
                    self.fired = False
                return None
            
            def is_hit(self, target_pos, target_size):
                # Check if a hit has occurred
                if target_pos[0] <= self.hit_pos[0] <= target_pos[0] + target_size[0]:
                    if target_pos[1] <= self.hit_pos[1] <= target_pos[1] + target_size[1]:
                        return True
                return False
    
        # Define the Target class
        class Target:
            def __init__(self, config, id):
                # Initialize target attributes
                self.config = config
                self.id = str(id)
                self.image = (self.config.target_img_name) + self.id
                self.image_path = (self.config.target_img_path) + self.image + '.png'
                self.target_speed = renpy.random.uniform(*self.config.target_speed_range)
                self.target_ypos = int(renpy.random.uniform(*self.config.target_ypos_range) * (renpy.config.screen_height))
                self.target_scale = renpy.random.uniform(*self.config.target_scale_range)
                self.image_size = [renpy.image_size(self.image_path)[0] * self.target_scale, renpy.image_size(self.image_path)[1] * self.target_scale]
                self.position = At(ImageReference(self.image), moving_target(self.target_speed, self.target_ypos, self.target_scale))
                self.killed = False
            
            def display(self):
                # Display the target on screen
                self.position = At(ImageReference(self.image), moving_target(self.target_speed, self.target_ypos, self.target_scale))
                renpy.show(name=self.id, what=self.position)
                
            def get_pos(self):
                # Get the current position of the target
                return self.position.xpos, self.position.ypos
            
            def hide(self):
                # Hide the target
                renpy.hide(self.id)
    
        # Define the Status class
        class Status:
            def __init__(self, target_nb, time_limit, life_max, round_nb, bullet_max):
                # Initialize game status attributes
                self.target_nb = target_nb
                self.time_limit = time_limit
                self.life_max = life_max
                self.round_nb = round_nb
                self.bullet_max = bullet_max
                self.target_now = target_nb
                self.time_left = time_limit
                self.life_now = life_max
                self.bullet_now = bullet_max
                self.round_now = 0

            def round_init(self):
                # Initialize attributes for a new round
                self.round_now += 1
                self.target_now = self.target_nb
                self.time_left = self.time_limit

            def round_end(self):
                # Perform actions at the end of a round
                self.life_now -= self.target_now
                if self.life_now < 0:
                    self.life_now = 0
            
            def is_game_over(self):
                # Check if the game is over
                if self.life_now <= 0 or (self.bullet_now <= 0 and self.round_now <= self.round_nb):
                    return True
                return False
            
            def is_clear(self):
                # Check if the round is clear
                if self.target_now <= 0:
                    return True
                return False
                
            def is_time_up(self):
                # Check if time is up for the current round
                if self.time_left <= 0:
                    return True
                return False
# Image Reference

# crosshair : https://github.com/ColoradoStark/Renpy_Shooter/tree/master/game/hunt
# bullet : https://www.flaticon.com/free-icon/bullet_942477
# gun : https://www.pngwing.com/en/free-png-pbhhx
# targets : https://luizmelo.itch.io/monsters-creatures-fantasy
# heart : https://creazilla-store.fra1.digitaloceanspaces.com/emojis/56085/heart-suit-emoji-clipart-md.png
