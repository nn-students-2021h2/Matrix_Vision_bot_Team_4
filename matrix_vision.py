import imageio
import pygame as pg
import random


class MatrixLetters:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.letters = [chr(int('0x30a0', 16) + i) for i in range(1, 95)]
        self.font_size = 15
        self.font = pg.font.Font('ms_mincho.ttf', self.font_size, bold=True)

        self.columns = width // self.font_size
        self.drops = [1 for i in range(0, self.columns)]

    def draw(self, surface):
        for i in range(0, len(self.drops)):
            char = random.choice(self.letters)
            char_render = self.font.render(char, False, (0, 255, 0))
            pos = i * self.font_size, (self.drops[i] - 1) * self.font_size
            surface.blit(char_render, pos)
            if self.drops[i] * self.font_size > self.height and random.uniform(0,1) > 0.975:
                self.drops[i] = 0
            self.drops[i] = self.drops[i] + 1



class MatrixVision:
    def __init__(self):
        pg.init()
        self.size = self.width, self.height = 600, 600
        self.screen = pg.display.set_mode(self.size, pg.HIDDEN)
        self.surface = pg.Surface(self.size, pg.SRCALPHA)
        self.clock = pg.time.Clock()
        self.matrixLetters = MatrixLetters(self.width, self.height)
        self.images = []

    def draw(self):
        self.surface.fill((0,0,0,10))
        self.matrixLetters.draw(self.surface)
        self.screen.blit(self.surface, (0,0))

    def run(self):
        counter = 0
        while counter < 100:
            self.draw()
            self.images.append(self.screen.copy())
            pg.display.flip()
            counter += 1
            self.clock.tick(30)
        self.generateGIF()

    def generateGIF(self):
        with imageio.get_writer('res.gif', mode='I', fps = 30) as writer:
            for img in self.images:
                writer.append_data(pg.surfarray.array3d(img).swapaxes(0,1))
