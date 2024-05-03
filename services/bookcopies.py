from typing import List, Optional, Any
from .book import Book


class BookCopy:
    bookcopies = []

    def __init__(self, copy_id: Any, book: Book, rack_no: int):
        self.copy_id = copy_id
        self.book = book
        self.rack_no = rack_no
        self.borrowed_by: Optional[str] = None  # Assuming borrowed_by is a string or None
        self.due_date: Optional[str] = None  # Assuming due_date is a string or None

    def __eq__(self, other):
        return isinstance(other, BookCopy) and self.copy_id == other.copy_id

    @classmethod
    def get_book_copy(cls, copy_id: int) -> Any | None:
        """
        Retrieve an existing book copy by copy_id.
        :param copy_id: The unique identifier for the book copy.
        :return: The retrieved BookCopy instance if found, None otherwise.
        """
        for book_copy in cls.bookcopies:
            if book_copy.copy_id == copy_id:
                return book_copy
        return None

    @classmethod
    def get_all_book_copies(cls) -> List['BookCopy']:
        """
        Retrieve all book copies.
        :return: A list of all BookCopy instances.
        """
        return cls.bookcopies

    @classmethod
    def create_book_copy(cls, copy_id: int, book: Book, rack_no: int) -> 'BookCopy':
        """
        Create a new book copy.
        :param copy_id: The unique identifier for the book copy.
        :param book: The Book instance associated with the book copy.
        :param rack_no: The rack number where the book copy is stored.
        :return: The created BookCopy instance.
        """
        book_copy = cls(copy_id, book, rack_no)
        cls.bookcopies.append(book_copy)
        return book_copy

    @classmethod
    def get_or_create_book_copy(cls, copy_id: int, book: Book, rack_no: int) -> 'BookCopy':
        """
        Retrieve an existing book copy or create a new book copy if not found.
        :param copy_id: The unique identifier for the book copy.
        :param book: The Book instance associated with the book copy.
        :param rack_no: The rack number where the book copy is stored.
        :return: The retrieved or created BookCopy instance.
        """
        existing_book_copy = cls.get_book_copy(copy_id)
        if existing_book_copy:
            return existing_book_copy
        else:
            return cls.create_book_copy(copy_id, book, rack_no)

    @classmethod
    def remove_book_copy(cls, copy_id: Any) -> Optional['BookCopy']:
        """
        Remove a book copy from the bookcopies list.
        :param copy_id: The unique identifier for the book copy to remove.
        :return: The removed BookCopy instance if found, None otherwise.
        """
        book_copy = cls.get_book_copy(copy_id)
        if book_copy:
            cls.bookcopies = [bc for bc in cls.bookcopies if bc != book_copy]
            return book_copy
        return None
