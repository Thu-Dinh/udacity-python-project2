"""MemeGenerator class.

This class overlays text(body, author)
from `QuoteEngine` on  image files.
"""

import tempfile
from pathlib import Path
import textwrap
import random
from PIL import Image, ImageDraw, ImageOps, ImageFont


class MemeGenerator:
    """MemeGenerator generates a meme from an image and text."""

    def __init__(self,
                 output_dir: str = './output',
                 input_image_path: str = None,
                 quote_body: str = '',
                 quote_author: str = '',
                 output_width: int = None
                 ):
        """Creation of a Meme Image.

        All params have defaults so they can be applied(or not).

        :param output_dir: Destination directory for saving
        :param input_image_path: Path and filename for image load
        :param quote_body: Quote body text
        :param quote_author: Quote Author text
        :param output_width: Desired image output width
        """
        self.output_path = Path(output_dir)
        self.quote_body = quote_body
        self._quote_author = quote_author
        self.output_width = output_width

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
        """Return None after loading an image from path."""
        self.image = Image.open(image_path)

    def overlay_text(self, output_width: int = None):
        """Overlays text on loaded image."""
        if output_width:
            self.crop_image(output_width=output_width)

        fnt_body_path = './MemeEngine/fonts/OpenSans-ExtraBold.ttf'
        fnt_author_path = './MemeEngine/fonts/OpenSans-LightItalic.ttf'
        self.font_body = ImageFont.truetype(fnt_body_path, 25)
        self.font_author = ImageFont.truetype(fnt_author_path, 20)

        d1 = ImageDraw.Draw(self.image)

        body_lines = textwrap.wrap(self.quote_body, width=30)
        body = textwrap.fill(self.quote_body, width=30)
        author = textwrap.fill(self.quote_author, width=30)

        x_body = random.randint(10, 30)
        y_body = random.randint(10, 300)
        x_author = x_body + 30
        y_author = y_body + len(body_lines) * 35 + 5
        d1.text((x_body, y_body), body,
                font=self.font_body, fill="white")
        d1.text((x_author, y_author), author,
                font=self.font_author, fill="white")

    def save_image(self):
        """Return path of saved image file."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        full_output_path = tempfile.NamedTemporaryFile(
            dir=self.output_path.name,
            prefix='meme-generator-',
            suffix='.jpg',
            delete=False).name
        self.image.save(full_output_path)
        return str(self.output_path) + "/" + str(Path(full_output_path).name)

    def crop_image(self, output_width: int = None) -> None:
        """Return an image crop cropped to single_dim keeping aspect ratio."""
        if not output_width and not self.output_width:
            raise ValueError("utput_width isn't set")
        if output_width and self.output_width != output_width:
            self.output_width = output_width

        scale = output_width / self.image.width
        w, h = self.image.size[0] * scale, self.image.size[0] * scale
        self.image = ImageOps.fit(self.image, (int(w), int(h)))

    def make_meme(self, img_path: str, quote_body: str,
                  quote_author: str, width: int = 500) -> str:
        """Override previously supplied params and saves image.

        :param img_path: Loads image from path,
        overriding and previously stored image
        :param quote_body: Loads quote_body from supplied text,
        overriding quote_body a previously set quote_body
        :param quote_author: Same as quote_body but for quote_author
        :param width: Scaled image keeping
        :return: location of saved file as a str
        """
        self.load_image(img_path)
        self.quote_body = quote_body
        self.quote_author = quote_author

        self.overlay_text(output_width=width)

        return self.save_image()
