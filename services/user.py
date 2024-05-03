from typing import List, Optional

from .bookcopies import BookCopy


class User:
    users = []
    MAX_BOOK_ALLOWED = 5

    def __init__(self, user_id: str, name: str = None, max_books_allowed: Optional[int] = None):
        """
            Initialize a new User instance.
            :param user_id: The unique identifier for the user.
            :param name: Optional name of the user.
            :param max_books_allowed: Maximum number of books the user can borrow (default is 5).
            """
        self.user_id = user_id
        self.name = name
        self.__max_books_allowed = max_books_allowed
        self.borrowed_books = []

    @property
    def max_books_allowed(self) -> int:
        """
        Get the maximum number of books allowed for the user.

        If a specific maximum number is set for the user, return that value.
        Otherwise, return the general maximum number of books allowed.

        :return: The maximum number of books allowed for the user.
        """
        if self.__max_books_allowed is not None:
            return self.__max_books_allowed
        return self.MAX_BOOK_ALLOWED

    @max_books_allowed.setter
    def max_books_allowed(self, max_books_allowed: int) -> None:
        """
        Set the maximum number of books allowed for the user.

        :param max_books_allowed: The new maximum number of books allowed.
        :raises ValueError: If the provided maximum number is negative.
        """
        if max_books_allowed >= 0:
            self.__max_books_allowed = max_books_allowed
        else:
            raise ValueError("Maximum number of books allowed must be non-negative")

    @classmethod
    def set_max_books_allowed(cls, max_books_allowed: int) -> Optional[int]:
        """
        Set the maximum number of books allowed for users.
        :param max_books_allowed: Maximum number of books allowed for users.
        :return: The new max allowed book if successful of None if otherwise
        """
        if max_books_allowed >= 0:
            cls.MAX_BOOK_ALLOWED = max_books_allowed
            return max_books_allowed
        return None

    @classmethod
    def get_user(cls, user_id: str) -> Optional['User']:
        """
            Retrieve an existing user.
            :param user_id: The unique identifier for the user.
            :return: The retrieved User instance if found, None otherwise.
            """
        for user in cls.users:
            if user.user_id == user_id:
                return user
        return None

    @classmethod
    def create_user(cls, user_id: str, name: str = None, max_books_allowed: int = 5) -> 'User':
        """
            Create a new user.
            :param user_id: The unique identifier for the user.
            :param name: Optional name of the user.
            :param max_books_allowed: Maximum number of books the user can borrow (default is 5).
            :return: The created User instance.
            """
        user = cls(user_id, name, max_books_allowed)
        cls.users.append(user)
        return user

    @classmethod
    def get_or_create(cls, user_id: str, name: str = None, max_books_allowed: int = 5) -> 'User':
        """
            Retrieve an existing user or create a new user if not found.
            :param user_id: The unique identifier for the user.
            :param name: Optional name of the user.
            :param max_books_allowed: Maximum number of books the user can borrow (default is 5).
            :return: The retrieved or created User instance.
            """
        existing_user = cls.get_user(user_id)
        if existing_user:
            return existing_user
        else:
            return cls.create_user(user_id, name, max_books_allowed)

    def borrow_book(self, book_copy: 'BookCopy', due_date: str) -> bool:
        """
            Borrow a book copy.
            :param book_copy: The book copy to be borrowed.
            :param due_date: The due date for returning the book copy.
            :return: True if the book copy was borrowed successfully, False otherwise.
            """
        if self.can_borrow_book():
            book_copy.borrowed_by = self.user_id
            book_copy.due_date = due_date
            self.borrowed_books.append(book_copy)
            return True
        else:
            return False

    def get_borrowed_books(self) -> List['BookCopy']:
        """
                Get a list of all book copies borrowed by the user.
                :return: A list of BookCopy instances.
            """
        return sorted(self.borrowed_books, key=lambda book_copy: book_copy.copy_id)

    def return_book(self, book_copy: 'BookCopy') -> bool:
        """
            Return a borrowed book copy.
            :param book_copy: The book copy to return.
            :return: True if the book copy was returned successfully, False otherwise.
            """
        if book_copy.borrowed_by == self.user_id:
            book_copy.borrowed_by = None
            book_copy.due_date = None
            self.borrowed_books.remove(book_copy)
            return True
        else:
            return False

    def can_borrow_book(self) -> bool:
        """
            Check if the user can borrow another book.
            :return: True if the user can borrow another book, False otherwise.
            """
        return len(self.borrowed_books) < self.max_books_allowed
