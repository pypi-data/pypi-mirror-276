"""
Module for creating a button.

Displays a button on the screen.
"""


from pgpyui import *


class Button:
    """
    A class to create a button.
    """
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        function: Callable[[], None],
        sprites: list = []
    ) -> None:
        
        self.__rectangle: pygame.Rect = pygame.Rect(*position, *size)
        self.__function: Callable[[], None] = function

        self.__bg_color: pygame.Color = pygame.Color("gray")
        self.__text_surface: pygame.Surface = pygame.font.SysFont("Comic Sans MS", size[1] // 4).render(
            text, True, pygame.Color("white")
        )

        self.__is_sprite: bool = False
        if sprites != []:
            self.__sprites: list = [pygame.transform.scale(pygame.image.load(sprites[0]).convert_alpha(), size), pygame.transform.scale(pygame.image.load(sprites[1]).convert_alpha(), size)]
            self.__is_sprite = True
        
        self.__sprtie: int= 0
        

        self.__text_rectangle: pygame.Rect = self.__text_surface.get_rect(
            center=(
                position[0] + size[0] // 2,
                position[1] + size[1] // 2
            )
        )
    
    def check_events(self, event) -> None:
        """
        Method for checking events.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.__check_click(pygame.mouse.get_pos())
        
        if self.__rectangle.collidepoint(pygame.mouse.get_pos()):
            self.__sprite = 1
            self.__bg_color = (43, 38, 38)
        else:
            self.__sprite = 0
            self.__bg_color = pygame.Color("gray")

    def __check_click(self, mouse_position: tuple[int, int]) -> None:
        if self.__rectangle.collidepoint(mouse_position):
            self.__function()

    def draw(self, window: pygame.Surface) -> None:
        """
        Method for drawing button.
        """
        if self.__is_sprite:
            window.blit(self.__sprites[self.__sprite], (self.__rectangle.x, self.__rectangle.y))
        else:
            pygame.draw.rect(window, self.__bg_color, self.__rectangle)
            window.blit(self.__text_surface, self.__text_rectangle)
