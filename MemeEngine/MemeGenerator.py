"""Meme generators overlays text(body, author) from `QuoteEngine` on  image files."""
import tempfile
from pathlib import Path
from typing import Tuple
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from PIL.ImageFont import FreeTypeFont


class MemeGenerator:
    """MemeGenerator generates a meme from an image and text."""

    def __init__(self,
                 output_dir: str = './output',
                 input_image_path: str = None,
                 quote_body: str = '',
                 quote_author: str = '',
                 output_width: int = None,
                 text_width_percent: float = 0.7,
                 font_size: int = None,
                 ):
        """Creation of a Meme Image.

        All params have defaults so they can be applied(or not) and any desired fashion.

        :param output_dir: Destination directory for saving
        :param input_image_path: Path and filename for image load
        :param quote_body: Quote body text
        :param quote_author: Quote Author text
        :param output_width: Desired image output width
        :param text_width_percent: Percentage of image with for text to use
        :param font_size: set font size
        """
        self.output_path = Path(output_dir)
        self.quote_body = quote_body
        self._quote_author = quote_author
        self.output_width = output_width
        self.text_width_percent = text_width_percent
        self.font_size = font_size

        self.font_body = None
        self.font_author = None
        self.image = None
        self.input_image_path = input_image_path
        # Load image now if supplied to constructor
        if self.input_image_path:
            self.load_image(self.input_image_path)

    @property
    def quote_author(self):
        """Return quote author in the format of choice for rendering."""
        return f'- {self._quote_author}'

    @quote_author.setter
    def quote_author(self, value):
        self._quote_author = value

    def load_image(self, image_path: str) -> None:
        """Return None after loading an image from path into class attribute."""
        self.image = Image.open(image_path)

    def overlay_text(self, output_width: int = None):
        """Overlays text on loaded image."""

        if output_width:
            self.crop_image(output_width=output_width)

        self.set_fonts_image_scale()
        position = self.random_image_position()

        d1 = ImageDraw.Draw(self.image)

        lines = textwrap.wrap(self.quote_body, width=40)
        for line in lines:
            d1.text(position, line, font=self.font_body, anchor='rb', fill=(255, 255, 255))

        author_lines = textwrap.wrap(self.quote_author, width=40)
        for line in author_lines:
            d1.text(position, line, font=self.font_author, anchor='rt', fill=(255, 255, 255))

    def save_image(self):
        """Return path of saved image file."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        full_output_path = tempfile.NamedTemporaryFile(dir=self.output_path.name, prefix='meme-generator-',
                                                       suffix='.jpg', delete=False).name
        self.image.save(full_output_path)
        return str(self.output_path) + "/" + str(Path(full_output_path).name)

    def crop_image(self, output_width: int = None) -> None:
        """Return an image crop cropped to single_dim keeping aspect ratio."""
        if not output_width and not self.output_width:
            raise ValueError("output_width must be supplied or set on instance before calling fit_image")
        if output_width and self.output_width != output_width:
            self.output_width = output_width

        scale = output_width / self.image.width
        w, h = self.image.size[0] * scale, self.image.size[0] * scale
        self.image = ImageOps.fit(self.image, (int(w), int(h)))

    def set_font_size(self, size: int) -> None:
        """Return a font for author based on class attributes."""

        self.font_body = FreeTypeFont('./MemeEngine/fonts/OpenSans-ExtraBold.ttf', size)
        self.font_author = FreeTypeFont('./MemeEngine/fonts/OpenSans-LightItalic.ttf', int(size * 0.7))

    def set_fonts_image_scale(self, text_width_pct: float = None) -> None:
        """Return two fonts for body and author text scaled to percentage of width."""
        if text_width_pct and self.text_width_percent != text_width_pct:
            self.text_width_percent = text_width_pct
        self.set_font_size(1)
        while self.font_body.getlength(self.quote_body) < self.image.width * self.text_width_percent:
            self.set_font_size(self.font_body.size + 1)

    def random_image_position(self) -> Tuple[int, int]:
        """Return random position for text placement."""
        box_padding = np.append(self.font_body.getbbox(self.quote_body, anchor='rb')[:2],
                                np.array(self.font_author.getbbox(self.quote_author, anchor='rt')[2:])) * -1
        x_min, y_min, x_max, y_max = tuple(np.array(((0, 0), self.image.size)).flatten() + box_padding)
        return np.random.random_integers(x_min, x_max), np.random.random_integers(y_min, y_max)

    def make_meme(self, img_path: str, quote_body: str, quote_author: str, width: int = 500) -> str:
        """Override previously supplied params and saves image.

        :param img_path: Loads image from path, overriding and previously stored image
        :param quote_body: Loads quote_body from supplied text, overriding quote_body a previously set quote_body
        :param quote_author: Same as quote_body but for quote_author
        :param width: Scaled image keeping
        :return: location of saved file as a str
        """
        self.load_image(img_path)
        self.quote_body = quote_body
        self.quote_author = quote_author

        self.overlay_text(output_width=width)

        return self.save_image()
