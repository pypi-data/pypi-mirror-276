"""
Module for creating a Slider.
"""


from pgpyui import *


class Slider:
    """
    Slider. 28-100 (Sorry, I really don't understand why this happened).
    """
    def __init__(
            self,
            position: tuple[int, int],
            size_block: tuple[int, int],
            len: int,
            orientation: bool = False
        ) -> None:
        
        self.__len: int = len

        self.__orientation: bool = orientation
        self.__rectangle: pygame.Rect = pygame.Rect(*position, *size_block)

        self.__is_push: bool = False

        self.__start: tuple = (self.__rectangle.centerx, self.__rectangle.centery)

        self.__finish: tuple
        self.__line_rect: pygame.Rect
        self.__line_pos: tuple
        if not orientation:
            self.__line_pos = ((self.__rectangle.centerx, self.__rectangle.centery), (self.__rectangle.centerx + self.__len, self.__rectangle.centery))
            self.__line_rect = pygame.Rect(*position, self.__len, size_block[1])
            self.__finish = (self.__start[0] + len, self.__start[1])
        else:
            self.__line_pos = ((self.__rectangle.centerx, self.__rectangle.centery), (self.__rectangle.centerx, self.__rectangle.centery + self.__len))
            self.__line_rect = pygame.Rect(*position, size_block[0], self.__len)
            self.__finish = (self.__start[0], self.__start[1] + len)
        
    
    def __move(self) -> None:
        x, y = pygame.mouse.get_pos()
        if self.__is_push:
            if self.__line_rect.collidepoint(x, y):
                if not self.__orientation:
                    self.__rectangle.x = x
                else:
                    self.__rectangle.y = y
        
    def draw(self, window) -> None:
        """
        Method for drawing slider.
        """
        
        pygame.draw.line(window, (255, 255, 255), self.__line_pos[0], self.__line_pos[1], 5)
        pygame.draw.rect(window, (255, 255, 255), self.__rectangle)
            

    def check_events(self, event: pygame.event.Event) -> None:
        """
        Method for checking events.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__is_push = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.__is_push = False
        
        self.__move()

    def data_return(self) -> int:
        """
        Method for return progress of slider.
        """

        progress: int
        if not self.__orientation:
            progress = int(round(self.__rectangle.centerx / self.__finish[0], 2) * 100)
        else:
            progress = int(round(self.__rectangle.centery / self.__finish[1], 2) * 100)

        return progress
