from abc import ABC, abstractmethod
from pygame.surface import Surface


class Drawable(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        ...
