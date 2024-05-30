"""
Module for creating a radio-button.
"""


from pgpyui import *


class Circle:
    def __init__(self, r, pos, color):
        self.r = r
        self.pos = pos
        self.__color = color

        self.push: bool = False

    def show(self, screen):
        pygame.draw.circle(screen, self.__color, self.pos, self.r, 3)
        if self.push:
            pygame.draw.circle(screen, self.__color, (self.pos[0], self.pos[1]), self.r // 2)


class Radio:
    """
    A class to create a radio-button.
    """
    def __init__(
            self,
            position: tuple[int, int],
            radius: int,
            num_rb: int,
            step: int,
            color: tuple[int, int, int] = (43, 38, 39),
        ) -> None:
        
        self.__bg_color: tuple[int, int, int] = color
        self.__num_rb = num_rb

        self.__radio_buttons: list = [Circle(radius, (position[0], position[1] + (count * step)), self.__bg_color) for count in range(num_rb)]

        self.__indx: list = [0 for _ in range(num_rb)]

        self.__bg_color: tuple[int, int, int] = color

    def check_events(self, event: pygame.event.Event) -> None:
        """
        Method for checking events.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                num_radio = 0
                for circle in self.__radio_buttons:
                    mouse_pos = pygame.mouse.get_pos()

                    circle_pos = circle.pos
                    delta_x = mouse_pos[0] - circle_pos[0]
                    delta_y = mouse_pos[1] - circle_pos[1]
                    if (delta_x ** 2 + delta_y ** 2) ** 0.5 <= circle.r:
                        self.__indx = [0 for _ in range(self.__num_rb)]
                        self.__indx[num_radio] = 1

                    num_radio += 1

    def draw(self, window) -> None:
        """
        Method for draw radio-button.
        """
        num_radio = 0
        for rd_bt in self.__radio_buttons:
            rd_bt.show(window)

            if self.__indx[num_radio]:
                rd_bt.push = True
            else:
                rd_bt.push = False

            num_radio += 1

    def data_return(self) -> list[int]:
        """
        Method to return list of push buttons.
        """
        
        return self.__indx
