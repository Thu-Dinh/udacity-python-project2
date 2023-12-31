"""Class for generating meme by web."""

import random
import os
import requests
from itertools import chain
import tempfile
from PIL import Image
from flask import Flask, render_template, abort, request

import QuoteEngine
from MemeEngine import MemeGenerator
from QuoteEngine import Ingestor

app = Flask(__name__)

meme = MemeGenerator('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = list(chain(*[Ingestor.parse(f) for f in quote_files]))

    images_path = "_data/photos/dog/"
    imgs = [f"{images_path}/{f}" for f in os.listdir(images_path)]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    try:
        img_data = requests.get(request.form['image_url'],
                                allow_redirects=True,
                                stream=True)
        tmp_file = tempfile.NamedTemporaryFile(prefix='meme-gen-fg-',
                                               suffix='.jpg',
                                               delete=False).name
        Image.open(img_data.raw).save(tmp_file)
    except requests.exceptions.ConnectionError:
        print("Image url is invalid")
        return render_template('meme_error.html')
    except OSError:
        print(f"cannot convert file to jpg")
        return render_template('meme_error.html')

    quote = QuoteEngine.QuoteModel(body=request.form['body'],
                                   author=request.form['author'])
    path = meme.make_meme(tmp_file, quote.body, quote.author)

    os.unlink(tmp_file)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
