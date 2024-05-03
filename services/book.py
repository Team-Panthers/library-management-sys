from typing import List, Any


class Book:
    books = []

    def __init__(self, book_id: str, title: str, authors: List[str], publishers: List[str], **kwargs):
        self.book_id = book_id
        self.title = title
        self.author_id = authors
        self.publisher_id = publishers

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        """
                Check if two books are equal based on their attributes.
            """
        if not isinstance(other, Book):
            return False

        return self.book_id == other.book_id

    @classmethod
    def get_book(cls, book_id: str) -> Any | None:
        """
            Retrieve an existing book by book_id.
            :param book_id: The unique identifier for the book.
            :return: The retrieved Book instance if found, None otherwise.
            """
        for book in cls.books:
            if book.book_id == book_id:
                return book
        return None

    @classmethod
    def get_all_books(cls) -> List['Book']:
        """
            Retrieve all books.
            :return: A list of all Book instances.
            """
        return cls.books

    @classmethod
    def create_book(cls, book_id: str, title: str, authors: List[str], publishers: List[str], **kwargs) -> 'Book':
        """
            Create a new book.
            :param book_id: The unique identifier for the book.
            :param title: The title of the book.
            :param authors: List of authors of the book.
            :param publishers: List of publishers of the book.
            :param kwargs: Additional keyword arguments for Book initialization
            :return: The created Book instance.
            """
        book = cls(book_id, title, authors, publishers, **kwargs)  # Initialize Book instance with provided
        # arguments
        cls.books.append(book)
        return book

    @classmethod
    def get_or_create_book(cls, book_id: str, title: str, authors: List[str], publishers: List[str],
                           **kwargs) -> 'Book':
        """
            Retrieve an existing book or create a new book if not found.
            :param book_id: The unique identifier for the book.
            :param title: The title of the book.
            :param authors: List of authors of the book.
            :param publishers: List of publishers of the book.
            :param kwargs: Additional keyword arguments for Book initialization
            :return: The retrieved or created Book instance.
            """
        existing_book = cls.get_book(book_id)
        if existing_book:
            return existing_book
        else:
            return cls.create_book(book_id, title, authors, publishers, **kwargs)
