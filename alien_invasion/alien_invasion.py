import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf 
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings() #使用设置初始化
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) #设置屏幕的宽高
    pygame.display.set_caption('Alien Invasion') # 设置标题
    #创建开始按钮
    play_button = Button(ai_settings, screen, "Play")
    #创建一个用于存储数据的实例
    stats = GameStats(ai_settings)
    #创建一艘飞船
    ship = Ship(ai_settings, screen) # 传入屏幕矩形
    #创建一个外星人
    alien = Alien(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建一个用于存储外星人的编组
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #必须在主while 循环前面创建该实例

    #创建统计游戏信息的实例，并创建的分牌
    sb = Scoreboard(ai_settings, screen, stats)
    #开始游戏
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets) #监听键盘点击事件
        if stats.game_active: #判断游戏是否开始，开始了才开始执行
          ship.update() #重新绘制飞船
          gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets) # 删除多余的子弹，并且绘制子弹
          gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, ) # 更新飞船
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button) # 传入设置 屏幕 和 外星人 飞船 
run_game()
            