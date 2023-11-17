import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Acording to the keydown'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        

def check_keyup_events(event, ship):
    '''Acording to the keyup'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Keyboard and mouse events'''
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Moves the spaceship to the right or left when the keydown is being pressed
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets)

            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Starts a new game when the player clicks on the button PLAY'''

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # Hides the cursor
        pygame.mouse.set_visible(False)

        # Restarts the statistic data
        stats.reset_stats()
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()

        # Restarts the images of the scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empties the aliens and bullets
        aliens.empty()
        bullets.empty()

        # Creates a new fleet and centers the spaceship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''Updates the screen'''
    screen.fill(ai_settings.bg_color)

    # Draw again the bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draws information about the score
    sb.show_score()

    # Draws the button Play if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Keeps the most recent screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Updates the position of the bullets and gets rid of the old ones'''
    # Updates the position
    bullets.update()

    # Gets rid of the bullets that are gone
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullets_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullets_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Answers collisions between bullets and aliens'''
    # Verifies if any bullet hit an alien and gets rid of both
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Starts a new level if all the fruit has been destroyed
        bullets.empty()
        ai_settings.increase_speed()

        # Increase the level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

        check_high_score(stats, sb)


def fire_bullets(ai_settings, screen, ship, bullets):
    '''Creates a new bullet and adds to the group of bullets'''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determinates the number of lines with aliens that the screen suport'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def get_number_aliens_x(ai_settings, alien_width):
    '''Determinates the number of aliens tha can appear in one line'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Creates an alien and positions in the line'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''Creates a fleet of aliens'''
    # Creates an alien and calculates the number of aliens in one line
    # The space between the aliens is tha same as the width

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Creates the first line of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    '''Answers properly if any alien reached the border'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Makes all the fleet go down and change the direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Responds to the collision between an alien and a spaceship'''

    if stats.ship_left > 0:
        # Decrements ships_left
        stats.ship_left -= 1

        # Updates the scoreboard
        sb.prep_ships()

        # Empties the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Creates a new fleet and centraliza the spaceship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pauses
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Verifies if any alien reached the bottom of the screen'''
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treats this case the same way when the spaceship is hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Verifies to see if the fleet is in one of the border and then updates the positions of all aliens'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Verifies if there was a collision between aliens and the spaceship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Verifies if there is any alien who hit the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    '''Checks if it has a new high score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()