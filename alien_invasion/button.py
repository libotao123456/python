import sys
import pygame
class Button():
    def __init__(self, ai_settings, screen, msg):
        '''初始化按钮'''
        self.screen = screen #获取屏幕
        self.screen_rect = screen.get_rect() #获取屏幕的矩形
        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50 # 指定一个宽高
        self.button_color = (0, 255, 0) # 按钮的颜色
        self.text_color = (255, 255, 255) # 字体的颜色
        self.font = pygame.font.SysFont(None, 48) # 字体的 和字体大小
        #创建按钮rect对象， 并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height) # 创建一个按钮 然后反正 0，0 坐标
        self.rect.center = self.screen_rect.center #屏幕居中
        #按钮标签只创建一次
        self.prep_msg(msg)
    
    def prep_msg(self, msg):
        '''将msg渲染成图像，并在按钮上居中'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) #添加一个字体
        self.msg_image_rect = self.msg_image.get_rect() #获取字体的矩形
        self.msg_image_rect.center = self.rect.center #字体 和button 居中
    
    def draw_button(self):
        #绘制一个用颜色填充的按钮，在绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
