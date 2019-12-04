import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''
    def __init__(self, ai_settings, screen):
        '''初始化外星人并且设置初始位置'''
        super().__init__()
        self.screen = screen #获取屏幕
        self.ai_settings = ai_settings # 获取设置

        #加载外星人图像，并设置rect的属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect() #并且获取他的矩形
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height / 5
        
        #存储外星人的准确位置
        self.x = float(self.rect.x) #把外星人的位置存起来

    def update(self):
        '''向右移动外星人'''
        #当前位置等于外星人的速度，乘以他的方向
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x # 然后把当前位置复制给外星人的位置

    def blitme(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        '''如果外星人位于屏幕边缘，就返回True'''
        screen_rect = self.screen.get_rect() #获取屏幕的矩形
        if self.rect.right >= screen_rect.right: #如果外星人的右边到了屏幕的右边也就是到边缘了
            return True
        elif self.rect.left <= 0: # 外星人到了左边边缘
            return True

