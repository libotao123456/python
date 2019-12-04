import pygame
from pygame.sprite import Sprite
#飞船
class Ship(Sprite):
    def __init__(self, ai_settings, screen): #指定飞船要绘制到什么地方
        '''初始化飞船并设置他的初始位置'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载飞船图片并且获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp') # 加载图像
        self.rect = self.image.get_rect() # 获取图像的矩形 处理rect 对象时，可使用矩形四角和中心的 x 和 y 坐标。可通过设置这些值来指定矩形的位置。
        self.screen_rect = screen.get_rect() # 获取屏幕的矩形

        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx #再将飞船中心的x坐标 放到屏幕中心的x坐标上
        self.rect.bottom = self.screen_rect.bottom # 再将飞船下边缘的y坐标 放到屏幕矩形bottom上
        #Pygame将使用这些rect 属性来放置飞船图像， 使其与屏幕下边缘对齐并水平居中。
        
        #飞船的属性center 保存小数
        self.center = float(self.rect.centerx)
        self.height = float(self.rect.bottom)
        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        '''根据移动标志调整飞船位置'''
        '''更新飞船的center的值不是rect'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.centerx += 1
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.height -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.height += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.bottom = self.height

    def blitme(self): #根据 rect 指定的位置将图像绘制到屏幕上
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        '''飞船在屏幕上居中'''
        self.centerx = self.screen_rect.centerx
        self.height = self.screen_rect.bottom
