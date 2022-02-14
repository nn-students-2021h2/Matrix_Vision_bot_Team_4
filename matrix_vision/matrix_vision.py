from io import BytesIO
import logging

import cv2
import imageio
import numpy as np
import pygame as pg

log = logging.getLogger(__name__)


class Matrix:
    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_size = 8
        self.letters = np.array([chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for i in range(10)])
        self.font = pg.font.Font(font_path, self.font_size, bold=True)
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
    def __init__(self, source_data, font_path=None, fps=30, use_opencv=False):
        pg.init()
        surface = None
        if isinstance(source_data, bytearray):
            surface = pg.image.load(BytesIO(source_data), '.jpg')
        elif isinstance(source_data, str):
            surface = pg.image.load(source_data)
        else:
            raise ValueError("Unsupported image source type")

        self.fps = fps
        self.use_opencv = use_opencv

        self.image = pg.pixelarray.PixelArray(surface)
        self.size = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.surface = pg.Surface(self.size, pg.SRCALPHA)
        self.screen = pg.display.set_mode(self.size, pg.HIDDEN)
        self.clock = pg.time.Clock()
        self.matrix = Matrix(self.width, self.height, font_path)
        self.images = []

    def draw(self):
        self.surface.fill(pg.Color('black'))
        self.matrix.run(self.surface, self.image)
        self.screen.blit(self.surface, (0,0))

    def run(self, out_name, duration = 100):
        counter = 0
        while counter < duration:
            self.draw()
            self.images.append(self.screen.copy())
            pg.display.flip()
            counter += 1
            self.clock.tick(30)
        self.generate_animation(out_name)

    def generate_animation(self, out_name):
        # prepare file as mp4 because tg reduce size of gifs https://github.com/telegramdesktop/tdesktop/issues/7738
        if self.use_opencv:
            video_writer = cv2.VideoWriter()
            video_writer.open(out_name, cv2.VideoWriter_fourcc(*'MP4V'), self.fps, self.size)
            if video_writer.isOpened():
                for img in self.images:
                    video_writer.write(pg.surfarray.array3d(img).swapaxes(0,1))
                video_writer.release()
            else:
                raise RuntimeError("Can't open cv2.VideoWriter()!")
        else:
            imageio.mimwrite(out_name, [pg.surfarray.array3d(img).swapaxes(0,1) for img in self.images], format='mp4', fps=self.fps)
        log.info(f"Save result to {out_name}")
