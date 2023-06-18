# Mem generator

This project is a multimedia application to dynamically generate memes, including an image with an overlaid quote

## Setup

Install all project dependencies is writen in `requirements.txt` file by pip.
Example install Pillow:
```
pip install -r requirements.txt
```

## Getting Start
### Run by command line
This program can run through main script with three optional arguments:
```
-p PATH, --path PATH           An image path    
-b BODY, --body BODY           A string quote body
-a AUTHOR, --author AUTHOR     A string quote author
```
The program returns a path to a generated image. If any argument is not defined, a random selection is used.
Example:
```
python main.py --path './_data/photos/dog/xander_1.jpg' --body 'This is body' --author 'author'
```

### Run by web application
- Start server by running below commands:
```
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
```
- Access application by URL below:
http://127.0.0.1:3000/

## Modules
### main module
- Generate a meme given an path and a quote
### MemeEngine module
- This module is responsible for manipulating and drawing text onto images
- `load_image`: this function to load a file from disk
- `crop_image`: this function resizing image by output_width argument
- `overlay_text`: this function to overlay text to an image to random location on the image
- `make_meme`: this function to generate image path by given image path, quote text, quote author, max width is 500 

### QuoteEngine module
- This module is responsible for ingesting many types of files that contain quotes
- A `QuoteModel` class, to represent a quote
- `IngestorInterface`: an abstract class, are defined two methods 
```
def can_ingest(cls, path: str) -> bool
def parse(cls, path: str) -> List[QuoteModel]
```

- `TxtIngestor` inherits the `IngestorInterface` to parse text file
- `PdfIngestor` inherits the `IngestorInterface` to parse pdf file
- `DocxIngestor` inherits the `IngestorInterface` to parse docx file
- `CsvIngestor` inherits the `IngestorInterface` to parse csv file