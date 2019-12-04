import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0: #就是玩家还有几条命， 大于0就是游戏还可以继续
      #将ships_ships_left减去1
      stats.ships_left -= 1
      #当前还剩下多少飞机，然后根据数量在左边绘制飞机
      sb.prep_ships()
      #清空外星人列表和子弹列表
      aliens.empty()
      bullets.empty()
      #创建新的一群外星人，并将飞船放到底部居中
      create_fleet(ai_settings, screen, ship, aliens)
      ship.center_ship()
      #暂停
      sleep(0.5)
    else: # 如果等于0 也就是结束了
      stats.game_active = False #活动状态变成了false
      pygame.mouse.set_visible(True) #光标显示出来了

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get(): #监听点击事件
        if event.type == pygame.QUIT: # 点了x把
            sys.exit() # 退出
        elif event.type == pygame.MOUSEBUTTONDOWN: # 点击左键
            mouse_x, mouse_y = pygame.mouse.get_pos() # 获取点击时候的坐标
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y) #点击play开始游戏
        elif event.type == pygame.KEYDOWN: # 监听按下按键
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP: # 监听松开按键
            check_keyup_events(event, ship)
        # elif event.type == pygame.KEYUP:
        #     check_keydown_events(event, ship)
        # elif event.type == pygame.KEYDOWN:
        #     check_keyup_events(event, ship)
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''玩家点击play按钮开始游戏'''
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active: #如果点击的的坐标是按钮的坐标 并且 游戏状态是未开始
        #重置游戏
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True #游戏开始
        sb.prep_level() # 等级
        sb.prep_ships() # 飞船
        #清空子弹和外星人
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''响应按键'''
    #按住右键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    #按住左键
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    #按住上键
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    #按住下键
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将它加入编组bullets中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    '''响应松开'''
    #松开右键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    #松开左键
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    #松开上键
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    #松开下键
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # #先背景后飞船，飞船就在背景前面了
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #绘制飞船
    ship.blitme()
    #绘制外星人
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #如果游戏在非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()
        #删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)



def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #检查是否击中了外星人
    #如果击中了就删除对应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #每次打到一个加分
    if collisions:
        for aliens in collisions.values():
          stats.score += ai_settings.alien_points * len(aliens)
          sb.prep_score()
        check_high_score( stats, sb)
    #如果外星人都打完了
    if len(aliens) == 0:
      #删除所有的子弹，并重新创建一个外星人群
      bullets.empty()
      ai_settings.increase_speed()
      #提高等级
      stats.level += 1
      sb.prep_level()
      create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    '''计算可以容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - (alien_width * 2)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算可以容纳多少行'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算一行可以容纳多少个外星人
    #外星人之间的间距是外星人的宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #创建第一行外星人
    # for alien_number in range(number_aliens_x):
    #     create_alien(ai_settings, screen, aliens, alien_number)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''有外星人到达边缘执行相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''整群外星人向下移动，并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''检查外星人是否到了底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像撞了飞船一样处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, sb, screen,  ship, aliens, bullets):
    '''检查是否有外星人位于屏幕边缘'''
    '''更新外星人人群中所有外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人与飞船之间的碰撞
    if pygame.sprite.pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    #检查外星人是否到了底部
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
    '''检查是否诞生了新的最高分'''
    if stats.score > stats.height_score:
        stats.height_score = stats.score
        sb.prep_high_score()


