"""Classes to read quote from various file types."""

from abc import ABC, abstractmethod
from QuoteEngine import QuoteModel
from typing import List
import tempfile
import docx
import pandas as pd
import subprocess


class IngestorInterface(ABC):
    """This is a abstract class."""

    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """Check extension file is valid.

        :param path: path of quote file
        :return: True if extension file is valid to ingest
        """
        pass

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse content file to `List[QuoteModel]`.

        :param path: path of quote file
        :return: List[QuoteModel]
        """
        pass

    @classmethod
    def ext_from_path(cls, path):
        """Return extension of file.

        :param path: path of quote file
        :return: file extension
        """
        return path.split('.')[-1]


class CsvIngestor(IngestorInterface):
    """This class to parse CSV file."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check valid with csv file."""
        return cls.ext_from_path(path) == 'csv'

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse CSV file to list of QuoteModel."""
        if not cls.can_ingest(path):
            raise ValueError(f"File type not supported for {path}")
        return pd.read_csv(path)\
            .apply(lambda x: QuoteModel(body=x.body, author=x.author), axis=1)\
            .to_list()


class DocxIngestor(IngestorInterface):
    """This class to parse DOCX file."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check valid with DOCX file."""
        return cls.ext_from_path(path) == 'docx'

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse DOCX file to list of QuoteModel."""
        if not cls.can_ingest(path):
            raise ValueError(f"File type not supported for {path}")
        doc = docx.Document(docx=path)
        return [QuoteModel(body=q.text.split("-")[0],
                           author=q.text.split("-")[1])
                for q in doc.paragraphs if q.text]


class PdfIngestor(IngestorInterface):
    """This class to parse CSV file."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check valid with PDF file."""
        return cls.ext_from_path(path) == 'pdf'

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse PDF file to list of QuoteModel."""
        if not cls.can_ingest(path):
            raise ValueError(f"File type not supported for {path}")

        tmp = tempfile.NamedTemporaryFile(suffix=".txt")
        sub_p = subprocess.run(['pdftotext', path, tmp.name], check=True)
        if sub_p.returncode:
            raise RuntimeError("Can not convert PDF to TXT by subprocess")
        content = open(tmp.name, 'r').readlines()
        lines = content[0].split(' "')
        return [QuoteModel(body=ln.split("-")[0], author=ln.split("-")[1])
                for ln in lines if ln]


class TxtIngestor(IngestorInterface):
    """This class to parse TEXT file."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check valid with TEXT file."""
        return cls.ext_from_path(path) == 'txt'

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse TEXT file to list of QuoteModel."""
        if not cls.can_ingest(path):
            raise ValueError(f"File type not supported for {path}")
        lines = open(path, 'r').readlines()
        return [QuoteModel(body=ln.split("-")[0], author=ln.split("-")[1])
                for ln in lines if ln]


class Ingestor(IngestorInterface):
    """This class encapsulates all the ingestors.

    It provides one interface to load nay supported file type.
    """

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return list of QuoteModel with any file type."""
        base = cls.__base__
        parser = next((c for c in base.__subclasses__()
                       if c.can_ingest(path)), None)
        if parser is None:
            raise ValueError(f"File type not supported for {path}")
        return parser.parse(path)
