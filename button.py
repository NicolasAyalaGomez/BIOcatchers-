import pygame

class Button():

    def __init__(self,image,pos,text_input,font,base_color,hovering_color):

        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font= font
        self.base_color, self.hovering_color= base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def cargar(self,screen):
        if self.image is not None:
            screen.blit(self.image,self.rect)
        screen.blit(self.text,self.text_rect)
        
    def checkForInput(self,position):

        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):

            return True
        
    def click(self,screen):
        # Simular efecto de hundimiento
        self.rect.move_ip(0, 5)
        self.cargar(screen)
        pygame.display.flip()
        pygame.time.wait(50)
        self.rect.move_ip(0, -5)
        self.cargar(screen)
        pygame.display.flip()
        

    def cambiar_color(self,position):

        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input,True, self.hovering_color)

        else:
            self.text = self.font.render(self.text_input,True,self.base_color)

