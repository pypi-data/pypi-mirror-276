"""
Module for creating a checkbox.
"""


from pgpyui import *


class CheckBox:
    """
    A class to create a Checkbox.
    """
    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            num_boxes: int,
            step: int,
            color: tuple[int, int, int] = (43, 38, 39),
            sprites: tuple[str] = []
        ) -> None:
        
        self.__boxes: list[pygame.Rect] = [pygame.Rect(position[0], position[1] + (count * step), *size) for count in range(num_boxes)]
        self.__size = size

        self.__is_sprite: bool = False
        if sprites != []:
            self.__sprites = [pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), size) for sprite in sprites]
            self.__is_sprite = True
            
        self.__indx: list = [0 for _ in range(num_boxes)]

        self.__bg_color: tuple[int, int, int] = color

        self.__text_surface: pygame.Surface = pygame.font.SysFont("Arial", size[1]).render(
            "√", True, color
        )

    def check_events(self, event: pygame.event.Event) -> None:
        """
        Method for checking events.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                num_box = 0
                for box in self.__boxes:
                    if box.collidepoint(pygame.mouse.get_pos()):
                        if self.__indx[num_box] == 0:
                            self.__indx[num_box] = 1
                        else:
                            self.__indx[num_box] = 0
                    
                    num_box += 1

    def draw(self, window) -> None:
        """
        Method for drawing checkbox.
        """
        num_box = 0
        if self.__is_sprite:
            for box in self.__boxes:
                window.blit(self.__sprites[self.__indx[num_box]], (box.x, box.y))
                num_box += 1
        else:
            for box in self.__boxes:
                text_rectangle: pygame.Rect = self.__text_surface.get_rect(
                center=(
                    box.x + self.__size[0] // 2,
                    box.y + self.__size[1] // 2
                    )
                )   
                pygame.draw.rect(window, self.__bg_color, box, 2)
                if self.__indx[num_box]:
                    window.blit(self.__text_surface, text_rectangle)
                num_box += 1

    def data_return(self) -> list[int]:
        """
        Method to return list of push buttons.
        """
        
        return self.__indx
