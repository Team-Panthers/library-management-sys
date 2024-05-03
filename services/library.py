from typing import List, Optional, Dict, Tuple, Any
from .book import Book
from .user import User
from .bookcopies import BookCopy


class Library:
    MAX_BOOKS_PER_RACK = 1

    def __init__(self):
        self.library_id = None
        self.racks = None

    def create_library(self, no_of_racks: int, **kwargs) -> Tuple[Optional[int], Optional[str]]:
        """
        Create the library with an optional library_id and an optional max number
        of books per rack and return the total number of racks created for the library
        :param no_of_racks: The total number of racks to be created in the library
        :param kwargs: Optional arguments including library_id and max_books_per_rack
        :return: A tuple containing the total number of racks created and an error message if any
        """
        try:
            self.MAX_BOOKS_PER_RACK = kwargs.get('max_books_per_rack', 1)
            self.library_id = kwargs.get('library_id', None)
            self.racks: Dict[int, list] = {rack_no: [] for rack_no in range(1, no_of_racks + 1)}

            return len(self.racks), None

        except Exception:
            return None, "Error Creating Library"

    def add_book(self, book_id: Any, title: str, authors: List[str], publishers: List[str], book_copy_ids: List[Any],
                 **kwargs) -> Tuple[List[Optional[Any]], Optional[str]]:
        """
        Adds a new book to the library.
        
        :param book_id: The unique identifier for the book.
        :param title: The title of the book.
        :param authors: A list of authors of the book.
        :param publishers: A list of publishers of the book.
        :param book_copy_ids: A list of copy IDs for the book copies to be added.
        :return: A tuple containing a list of rack numbers where the book copies were added and an error message if any.
        """
        try:

            book = Book.get_or_create_book(book_id, title, authors, publishers, **kwargs)
            rack_numbers = []
            for copy_id in book_copy_ids:
                rack_no = self.find_first_available_rack()
                if rack_no:
                    book_copy = BookCopy.get_or_create_book_copy(copy_id, book, rack_no)
                    rack_no, error_msg = self.add_book_copy_to_rack(book_copy, rack_no)
                    if error_msg is None:
                        rack_numbers.append(rack_no)
                    else:
                        rack_numbers.append(None)
                else:
                    rack_numbers.append(None)
                    break
            return rack_numbers, None
        except Exception:
            return [], "Error adding book"

    def remove_book_copy(self, book_copy_id: Any) -> Tuple[Optional[Tuple['BookCopy', int]], Optional[str]]:
        """
            Removes a book copy from the library by its ID.

            :param book_copy_id: The ID of the book copy to be removed.
            :return: A tuple containing the instance of the removed book copy and the rack number it was removed from if successful,
                    or None and an error message if the book copy ID is invalid.
            """
        try:
            result = self.get_book_copy_by_field('copy_id', book_copy_id)
            if result is not None:
                book_copy, rack_no = result
                if book_copy:
                    book_copy = book_copy.remove_book_copy(book_copy.copy_id)
                    self.racks[rack_no].remove(book_copy)
                    return (book_copy, rack_no), None

            return None, "Invalid Book Copy ID"
        except Exception as e:
            return None, f"Error removing book copy: {str(e)}"

    def borrow_book(self, book_id: Any, user_id: str, due_date: str) -> Tuple[Optional[int], Optional[str]]:
        """
            Borrow a book copy for a user.

            :param book_id: The ID of the book to borrow.
            :param user_id: The ID of the user borrowing the book.
            :param due_date: The due date for returning the book.
            :return: A tuple containing the rack number and None if the book is successfully borrowed,
                    or None and an error message if borrowing fails.
        """
        user = User.get_or_create(user_id)

        if not user.can_borrow_book():
            return None, "Overlimit"

        book = Book.get_book(book_id)
        if not book:
            return None, "Invalid Book ID"

        result = self.get_book_copy_by_field('book', book)
        if not result:
            return None, "Not available"

        book_copy, rack_no = result
        self.racks[rack_no].remove(book_copy)

        if not user.borrow_book(book_copy, due_date):
            return None, "An Error occurred"

        return rack_no, None

    def borrow_book_copy_by_id(self, copy_id: Any, user_id: str, due_date: str) -> Tuple[Optional[int], Optional[str]]:
        """
        Borrow a book copy by its copy ID for a user.

        :param copy_id: The ID of the book copy to borrow.
        :param user_id: The ID of the user borrowing the book.
        :param due_date: The due date for returning the book.
        :return: A tuple containing the rack number and None if the book copy is successfully borrowed,
                or None and an error message if borrowing fails.
        """
        user = User.get_or_create(user_id)
        if not user.can_borrow_book():
            return None, "Overlimit"

        result = self.get_book_copy_by_field('copy_id', copy_id)
        if not result:
            return None, "Invalid Book Copy ID"

        book_copy, rack_no = result
        self.racks[rack_no].remove(book_copy)

        if not user.borrow_book(book_copy, due_date):
            return None, "An Error occurred"

        return rack_no, None

    def return_book_copy(self, copy_id: Any) -> tuple[None, str] | tuple[str, str | None]:
        """
        Return a book copy by its copy ID.

        :param copy_id: The ID of the book copy to return.
        :return: A tuple containing the rack number and None if the book copy is successfully returned,
                or None and an error message if returning fails.
        """
        book_copy = BookCopy.get_book_copy(copy_id)
        if not book_copy:
            return None, "Invalid Book Copy ID"

        if not book_copy.borrowed_by:
            return None, "Copy not borrowed"

        user_id = book_copy.borrowed_by
        user = User.get_user(user_id)
        user.return_book(book_copy)

        rack_no = self.find_first_available_rack()
        if not rack_no:
            return None, f"Returned book copy {copy_id} but no available rack"

        rack_no, error = self.add_book_copy_to_rack(book_copy, rack_no)

        if error:
            return None, error

        return f"Returned book copy {copy_id} and added to rack: {rack_no}", None

    @staticmethod
    def get_user_borrowed_book_copy(user_id: Any) -> List[BookCopy]:
        """
            Get a list of book copies borrowed by a user.
            :param user_id: The ID of the user.
            :return: A list of BookCopy instances borrowed by the user.
        """
        user = User.get_user(user_id)
        if user:
            return user.get_borrowed_books()
        else:
            return []

    def search(self, attribute: str, attribute_value: str) -> List['BookCopy']:
        """
        Search for books based on a given attribute and attribute value.
        :param attribute: The attribute to search for (e.g., 'book_id', 'author', 'publisher').
        :param attribute_value: The value to search for.
        :return: A list of BookCopy instances matching the search criteria.
        """
        found_books = []

        for book in Book.get_all_books():
            # Handle case where attribute is a list
            if isinstance(getattr(book, attribute, None), list):
                if attribute_value in getattr(book, attribute):
                    found_books.extend(self.get_copies_of_book(book))
            else:
                # Handle case where attribute is not a list
                attribute_value_book = getattr(book, attribute, None)
                if attribute_value_book is not None and attribute_value_book == attribute_value:
                    found_books.extend(self.get_copies_of_book(book))

        return sorted(found_books, key=lambda book_copy: book_copy.rack_no if book_copy.rack_no is not None else float('inf'))

    @staticmethod
    def get_copies_of_book(book: 'Book') -> List['BookCopy']:
        """
        Retrieve all copies of a given book.
        :param book: The book to retrieve copies for.
        :return: A list of copies of the given book.
        """
        copies = []
        for book_copy in BookCopy.get_all_book_copies():
            if book_copy.book == book:
                copies.append(book_copy)
        return copies

    @staticmethod
    def modify_user_max_borrowed_books_allowed(max_books_allowed: int, user_id: str) -> tuple[User, None] | tuple[
            None, str] | tuple[None, Exception]:
        """
        Modify the maximum number of books allowed for a user.

        :param user_id: The ID of the user whose maximum allowed books to modify.
        :param max_books_allowed: The new maximum number of books allowed for the user.
        :return: A tuple containing the updated user object and None if the modification was successful,
                 otherwise None and an error message.
        """
        try:
            user = User.get_or_create(user_id)
            if user:
                user.max_books_allowed = max_books_allowed
                return user, None
            else:
                return None, "User not found"
        except Exception:
            return None, 'Maximum number of books allowed must be non-negative'

    @staticmethod
    def modify_general_user_max_borrowed_books_allowed(max_books_allowed: int) -> tuple[int, None] | tuple[None, str]:
        """
            Modify the maximum number of books allowed for general users.

            :param max_books_allowed: Maximum number of books allowed for users.
            :return: The new maximum number of books allowed if successful, otherwise None.
            """
        max_books_allowed = User.set_max_books_allowed(max_books_allowed)
        if max_books_allowed:
            return max_books_allowed, None
        return None, "Maximum number of books allowed must be non-negative"

    def add_book_copy_to_rack(self, book_copy: BookCopy, rack_no: int) -> Tuple[Optional[int], Optional[str]]:
        """
        Adds a book copy to the specified rack.

        :param book_copy: The BookCopy object to be added to the rack.
        :param rack_no: The rack number where the book copy should be added.
        :return: A tuple containing the rack number and None if successful, or None and an error message if there's an exception.
        """
        try:
            self.racks[rack_no].append(book_copy)
            return rack_no, None
        except Exception:
            return None, f"Error adding book copy to rack {rack_no}"

    def find_first_available_rack(self) -> Optional[int]:
        """
            Finds the first available rack in the library.
        """
        for rack_no, copies in self.racks.items():
            if len(copies) < self.MAX_BOOKS_PER_RACK:
                return rack_no
        return None

    def get_book_copy_by_field(self, field_name: str, value: Any) -> Optional[Tuple['BookCopy', int]]:
        """
        Retrieve a book copy from all racks in the library based on a specified field.
        :param field_name: The name of the field to search for.
        :param value: The value to search for in the specified field.
        :return: A tuple containing the first BookCopy instance found with the specified field value in any rack and the rack number,
                 or None if not found.
        """
        for rack_no, copies in self.racks.items():
            for book_copy in copies:
                # Check if the field exists in the BookCopy instance
                if hasattr(book_copy, field_name):
                    # Retrieve the value of the specified field
                    field_value = getattr(book_copy, field_name)
                    # Compare the field value with the provided value
                    if field_value == value:
                        return book_copy, rack_no
        return None


library_service = Library
