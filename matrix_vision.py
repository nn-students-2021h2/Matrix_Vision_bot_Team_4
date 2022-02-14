import cv2
from datetime import datetime
import numpy as np
import pygame as pg
import random


class Matrix:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_size = 15
        self.letters = np.array([chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for i in range(10)])
        self.font = pg.font.Font('ms_mincho.ttf', self.font_size, bold=True)
        self.size = self.rows, self.columns = \
            height // self.font_size, width // self.font_size
        self.matrix = np.random.choice(self.letters, self.size)
        self.char_intervals = np.random.randint(25, 50, size=self.size)
        self.cols_speed = np.random.randint(1, 500, size=self.size)
        self.prerendered_chars = self.get_prerendered_chars()

    def get_prerendered_chars(self):
        char_colors = [(0, green, 0) for green in range(256)]
        prerendered_chars = {}
        for char in self.letters:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    def draw(self, surface, image):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.font_size, y * self.font_size
                    _, red, green, blue = pg.Color(image[pos])
                    if red and green and blue:
                        color = (red + green + blue) // 3
                        color = 220 if 160 < color < 220 else color
                        char = self.prerendered_chars[(char, (0, color, 0))]
                        char.set_alpha(color + 60)
                        surface.blit(char, pos)

    def shift_column(self, frames):
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.letters, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars
    
    def run(self, surface, image):
        frames = pg.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.draw(surface, image)


class MatrixVision:
    def __init__(self, image_name):
        pg.init()
        surf = pg.image.load(image_name) # convert_alpha()
        self.image = pg.pixelarray.PixelArray(surf)
        self.size = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.surface = pg.Surface(self.size, pg.SRCALPHA)
        self.screen = pg.display.set_mode(self.size, pg.HIDDEN)
        self.clock = pg.time.Clock()
        self.matrix = Matrix(self.width, self.height)
        self.images = []

    def draw(self):
        self.surface.fill(pg.Color('black'))
        self.matrix.run(self.surface, self.image)
        self.screen.blit(self.surface, (0,0))

    def run(self, duration = 100):
        counter = 0
        while counter < duration:
            self.draw()
            self.images.append(self.screen.copy())
            pg.display.flip()
            counter += 1
            self.clock.tick(30)
        return self.generate_animation()

    def generate_animation(self):
        video_writer = cv2.VideoWriter()
        file_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f') + ".mp4"
        video_writer.open(file_name, cv2.VideoWriter_fourcc(*'MP4V'), 30, self.size)
        if video_writer.isOpened():
            for img in self.images:
                video_writer.write(pg.surfarray.array3d(img).swapaxes(0,1))
            video_writer.release()
            return file_name
        else:
            raise RuntimeError("Can't open cv2.VideoWriter()!")
