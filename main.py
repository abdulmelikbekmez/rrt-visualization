import pygame as pg
from pygame.math import Vector2
from pygame.time import Clock
from drawable import Drawable
from constants import *
from obstacle import Obstacle
from rrt import RRT
from random import randint as rint


class App:
    BACKGROUND_COLOR = pg.color.Color(255, 255, 255)

    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = Clock()
        self.running = True
        self.start: Vector2 | None = None
        self.finish: Vector2 | None = None
        self.tree: RRT | None = None
        l = [Obstacle(Vector2(rint(0, WIDTH), rint(0, HEIGHT))) for _ in range(50)]
        self.drawable_list: list[Drawable] = [*l]
        self.obstacle_list: list[Obstacle] = l
        RRT.OBSTACLE_LIST = self.obstacle_list

    def main(self):
        while self.running:
            self.__event_handler()
            self.screen.fill(self.BACKGROUND_COLOR)

            self.__update()
            self.__draw()

            self.clock.tick(FPS)

            pg.display.set_caption(f"FPS => {self.clock.get_fps()}")
            pg.display.update()

    def __del__(self):
        if self.tree:
            self.tree.stop = True

    def __event_handler(self):
        for event in pg.event.get():
            if event.type is pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if event.key == pg.K_r and self.tree:
                    self.drawable_list.remove(self.tree)
                    self.tree.stop = True
                    self.tree = None

            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    x, y = pg.mouse.get_pos()
                    if self.tree is None:
                        self.tree = RRT(Vector2(x, y))
                        self.drawable_list.append(self.tree)

                    elif not self.tree.started:
                        self.tree.main(Vector2(x, y))

    def __update(self):
        pass

    def __draw(self):
        for drawable in self.drawable_list:
            drawable.draw(self.screen)


if __name__ == "__main__":
    App().main()
