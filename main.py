"""
THE BACKSTORY - You are a retired extra-terrestrial-military officer in the year 3000. You were looking to have a
leisurely drinking session after a long week, however, the neighboring alien civilization chose today of all days to
wage war - starting at your favorite bar! Do you still have what it takes after all these years
to fend them off until reinforcements arrive??

Hint - You need to survive for 3 minutes for the backup to get to you
"""
import pygame
import time
import random

pygame.font.init()

# creating the window -
window_width, window_height = 1000, 750
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('SPACE BARS')
Background = pygame.image.load("space bar #2.jpeg")

# initialising necessary constants -
avatar_width = 65
avatar_height = 90
avatar_velocity = 10

laser_width = 20
laser_height = 40
laser_velocity = 4

clock = pygame.time.Clock()
Font = pygame.font.SysFont("comic sans", 40)


# the function that is used to draw the main elements -
def drawing(avatar, t_elapsed, lasers_going_down, lasers_going_up):
    window.blit(Background, (0, 0))
    minutes = t_elapsed // 60
    seconds = t_elapsed % 60

    # Format the time as a string
    time_string = "{:02d}:{:02d}".format(minutes, seconds)
    time_text = Font.render("Time alive:" + time_string, 1, "white")
    window.blit(time_text, (8, 8))
    pygame.draw.rect(window, "black", avatar)
    for laser in lasers_going_down:
        pygame.draw.rect(window, "purple", laser)
    for laser in lasers_going_up:
        pygame.draw.rect(window, "purple", laser)

    pygame.display.update()


# function to redraw the main elements to manage the layers -
def redraw(avatar, t_elapsed, lasers_going_down, lasers_going_up):
    drawing(avatar, t_elapsed, lasers_going_down, lasers_going_up)
    pygame.display.update()
    pygame.time.delay(2000)


def display_text(text, x, y):
    window.blit(text,
                ((window_width - x) / 2,
                 (window_height - 2*y - 40) / 2), )


def main():
    running = True
    avatar = pygame.Rect(window_width // 2, (window_height - avatar_height) // 2, avatar_width, avatar_height)
    start_t = time.time()
    hit = False

    # initialising elements for laser creation -
    lasers_going_down = []
    lasers_going_up = []
    laser_increment = 2000
    laser_tick_count = 0
    while running:
        t_elapsed = round(time.time() - start_t)
        minutes = t_elapsed // 60

        # creating the lasers in random x-positions -
        laser_tick_count += clock.tick(75)
        if laser_tick_count > laser_increment:
            for p in range(2):
                laser_x_coordinate = random.randint(0, window_width - laser_width)
                laser_going_down = pygame.Rect(laser_x_coordinate, -laser_height, laser_width, laser_height)
                lasers_going_down.append(laser_going_down)
                laser_x_coordinate = random.randint(0, window_width - laser_width)
                laser_going_up = pygame.Rect(laser_x_coordinate, window_height+laser_height, laser_width, laser_height)
                lasers_going_up.append(laser_going_up)

            laser_increment = max(400, laser_increment - 50)
            laser_tick_count = 0

        # checking for the quit action by user e.g. pressing the X button on the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # setting the corresponding key actions
        key_dict = pygame.key.get_pressed()
        if key_dict[pygame.K_a] and avatar.x - avatar_velocity > 0:
            avatar.x -= avatar_velocity
        if key_dict[pygame.K_d] and avatar.x + avatar_velocity + avatar_width < window_width:
            avatar.x += avatar_velocity
        if key_dict[pygame.K_w] and avatar.y - avatar_velocity > 0:
            avatar.y -= avatar_velocity
        if key_dict[pygame.K_s] and avatar.y + avatar_velocity + avatar_height < window_height:
            avatar.y += avatar_velocity

        # moving the lasers and checking if they have hit
        for laser_going_down in lasers_going_down[:]:
            laser_going_down.y += laser_velocity
            if laser_going_down.y > window_height:
                lasers_going_down.remove(laser_going_down)
            elif laser_going_down.y + laser_height >= avatar_height and avatar.colliderect(laser_going_down):
                hit = True
                break
        for laser_going_up in lasers_going_up[:]:
            laser_going_up.y -= laser_velocity
            if laser_going_up.y < 0:
                lasers_going_up.remove(laser_going_up)
            elif laser_going_up.y <= avatar.y + avatar_height and avatar.colliderect(laser_going_up):
                hit = True
                break

        # what to do when the player has lost i.e. a laser hit the avatar
        if hit:
            # displaying defeat text
            defeat_font_1 = pygame.font.SysFont("century", 60)
            defeat_text_1 = defeat_font_1.render("DEFEATED", 1, "white")
            defeat_font_2 = pygame.font.SysFont("century", 50)
            defeat_text_2 = defeat_font_2.render(f"YOUR TIME - {minutes} minutes,{t_elapsed} seconds", 1, "white")

            redraw(avatar, t_elapsed, lasers_going_down, lasers_going_up)

            display_text(defeat_text_1, defeat_text_1.get_width(), defeat_text_1.get_height())
            display_text(defeat_text_2, defeat_text_2.get_width(), defeat_text_2.get_height() - defeat_text_1.get_height())

            pygame.display.update()
            pygame.time.delay(3000)
            # calling the main function so that game auto-continues after losing
            main()
            break

        # the player has won if their time is at least 3 minutes
        if t_elapsed >= 180:
            # displaying victory text
            victory_font = pygame.font.SysFont("comic sans", 40)
            victory_text_1 = victory_font.render("You have done it!", 1, "white")
            victory_text_2 = victory_font.render("The aliens are finally retreating and the bar is safe!", 1, "white")

            redraw(avatar, t_elapsed, lasers_going_down, lasers_going_up)

            display_text(victory_text_1, victory_text_1.get_width(), victory_text_1.get_height())
            display_text(victory_text_2, victory_text_2.get_width(), victory_text_2.get_height()
                         - victory_text_1.get_height())

            pygame.display.update()
            pygame.time.delay(5000)
            break

        drawing(avatar, t_elapsed, lasers_going_down, lasers_going_up)

    pygame.quit()


if __name__ == '__main__':
    main()
