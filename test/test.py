import unittest
from services.library import Library
from services.bookcopies import BookCopy


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.create_library(10)

        # Populating the library with books and book copies using the add_book method

        # Adding Book 1 and its copies to rack 1
        self.library.add_book(
            book_id=1,
            title="Test Book 1",
            authors=["Author 1"],
            publishers=["Publisher 1"],
            book_copy_ids=[101, 102, 103]
        )

        # Adding Book 2 and its copies to rack 2
        self.library.add_book(
            book_id=2,
            title="Test Book 2",
            authors=["Author 2"],
            publishers=["Publisher 2"],
            book_copy_ids=[104, 105]
        )

    def test_create_library(self):
        # Test creating a library with no optional arguments
        total_racks, error_msg = self.library.create_library(5)
        self.assertEqual(total_racks, 5)
        self.assertIsNone(error_msg)

        # Test creating a library with optional arguments
        total_racks, error_msg = self.library.create_library(10, max_books_per_rack=2, library_id=123)
        self.assertEqual(total_racks, 10)
        self.assertIsNone(error_msg)
        self.assertEqual(self.library.MAX_BOOKS_PER_RACK, 2)
        self.assertEqual(self.library.library_id, 123)

    def test_add_book(self):
        # Test adding a book
        rack_numbers, error_msg = self.library.add_book(
            book_id=1,
            title="Test Book",
            authors=["Author 1", "Author 2"],
            publishers=["Publisher 1", "Publisher 2"],
            book_copy_ids=[106, 107]
        )
        self.assertEqual(len(rack_numbers), 2)
        self.assertIsNone(error_msg)

        # Test adding a book with extra arguments
        rack_numbers, error_msg = self.library.add_book(
            book_id=2,
            title="Test Book",
            authors=["Author 1", "Author 2"],
            publishers=["Publisher 1", "Publisher 2"],
            book_copy_ids=[108],
            invalid_argument='invalid'
        )
        self.assertEqual(len(rack_numbers), 1)
        self.assertIsNone(error_msg)
        self.assertEqual(self.library.racks[rack_numbers[0]][0].book.book_id, 2)

    def test_remove_book_copy_valid_id(self):
        # Ensure the book copy to be removed exists in rack 1
        self.assertEqual(len(self.library.racks[1]), 1)

        # Ensure the id of the book in rack one is 101
        self.assertEqual(self.library.racks[1][0].copy_id, 101)

        # Remove one of the book copies from rack 1
        removed_result, error_msg = self.library.remove_book_copy(101)

        # Ensure the removal was successful
        self.assertIsNotNone(removed_result)
        self.assertIsNone(error_msg)

        # Ensure the book copy is removed from rack 1
        self.assertEqual(len(self.library.racks[1]), 0)

        # Ensure the returned result contains the correct book copy and rack number
        removed_book_copy, removed_rack_no = removed_result
        self.assertEqual(removed_book_copy.copy_id, 101)
        self.assertEqual(removed_rack_no, 1)

    def test_remove_book_copy_invalid_id(self):
        # Attempt to remove a book copy with an invalid ID
        removed_result, error_msg = self.library.remove_book_copy(999)

        # Ensure no book copy is removed and an error message is returned
        self.assertIsNone(removed_result)
        self.assertEqual(error_msg, "Invalid Book Copy ID")

    def test_borrow_book_success(self):
        # Ensure the book copy is initially in rack 1
        self.assertEqual(len(self.library.racks[1]), 1)

        # Borrow the book copy for a user
        result, error_msg = self.library.borrow_book(book_id=1, user_id='user1', due_date='2024-05-10')

        # Ensure the borrowing was successful
        self.assertIsNotNone(result)
        self.assertIsNone(error_msg)

        # Ensure the book copy is removed from rack 1
        self.assertEqual(len(self.library.racks[1]), 0)

    def test_borrow_book_overlimit(self):
        # Create a user with maximum borrowed books limit reached
        self.library.modify_user_max_borrowed_books_allowed(2, 'user2')  # Set max books allowed for user2 to 2
        # Borrow 2 books for user2
        for i in range(2):
            result, error_msg = self.library.borrow_book(book_id=1, user_id='user2', due_date='2024-05-10')
            self.assertIsNotNone(result)
            self.assertIsNone(error_msg)

        # Attempt to borrow another book for user2 (should fail due to overlimit)
        result, error_msg = self.library.borrow_book(book_id=1, user_id='user2', due_date='2024-05-10')
        self.assertIsNone(result)
        self.assertEqual(error_msg, "Overlimit")

    def test_borrow_book_copy_by_id_success(self):
        # Ensure the book copy is initially in rack 1
        self.assertEqual(len(self.library.racks[1]), 1)

        # Borrow the book copy by its ID for a user
        result, error_msg = self.library.borrow_book_copy_by_id(copy_id=101, user_id='user1', due_date='2024-05-10')

        # Ensure the borrowing was successful
        self.assertIsNotNone(result)
        self.assertIsNone(error_msg)

        # Ensure the book copy is removed from rack 1
        self.assertEqual(len(self.library.racks[1]), 0)

    def test_borrow_book_copy_by_id_overlimit(self):
        # Create a user with maximum borrowed books limit reached
        self.library.modify_user_max_borrowed_books_allowed(2, 'user3')  # Set max books allowed for user2 to 2
        # Borrow 2 books for user2
        for i in range(2):
            result, error_msg = self.library.borrow_book(book_id=1, user_id='user3', due_date='2024-05-10')
            self.assertIsNotNone(result)
            self.assertIsNone(error_msg)

        # Attempt to borrow a book copy by its ID for the user
        result, error_msg = self.library.borrow_book_copy_by_id(copy_id=101, user_id='user3', due_date='2024-05-10')

        # Ensure borrowing fails due to maximum borrow limit reached
        self.assertIsNone(result)
        self.assertEqual(error_msg, "Overlimit")

    def test_borrow_book_copy_by_id_invalid_copy_id(self):
        # Attempt to borrow a book copy with an invalid copy ID
        result, error_msg = self.library.borrow_book_copy_by_id(copy_id=999, user_id='user1', due_date='2024-05-10')

        # Ensure borrowing fails due to invalid copy ID
        self.assertIsNone(result)
        self.assertEqual(error_msg, "Invalid Book Copy ID")

    def test_return_book_copy_success(self):
        # Borrow the book copy by its ID for a user
        rack_no, error = self.library.borrow_book_copy_by_id(copy_id=101, user_id='user4', due_date='2024-05-10')

        # Ensure the book copy is borrowed
        self.assertIsNone(error)
        self.assertEqual(len(self.library.racks[rack_no]), 0)
        book_copy = BookCopy.get_book_copy(101)

        # Ensure then book was borrowed by user4
        self.assertIsNotNone(book_copy)
        self.assertEqual(book_copy.borrowed_by, 'user4')

        # Return the book copy
        result, error_msg = self.library.return_book_copy(copy_id=101)

        # Ensure the returning was successful
        self.assertIsNotNone(result)
        self.assertIsNone(error_msg)

        # Ensure the book copy is added back to rack 1
        self.assertEqual(len(self.library.racks[1]), 1)

    def test_return_book_copy_invalid_copy_id(self):
        # Attempt to return a book copy with an invalid copy ID
        result, error_msg = self.library.return_book_copy(copy_id=999)

        # Ensure returning fails due to invalid copy ID
        self.assertIsNone(result)
        self.assertEqual(error_msg, "Invalid Book Copy ID")

    def test_return_book_copy_not_borrowed(self):
        # Attempt to return a book copy that is not borrowed
        result, error_msg = self.library.return_book_copy(copy_id=101)

        # Ensure returning fails because the copy is not borrowed
        self.assertIsNone(result)
        self.assertEqual(error_msg, "Copy not borrowed")

    def test_get_user_borrowed_book_copy_with_books_borrowed(self):
        # Borrow book copies for a user
        user_id = 'user7'
        self.library.borrow_book_copy_by_id(copy_id=101, user_id=user_id, due_date='2024-05-10')
        self.library.borrow_book_copy_by_id(copy_id=102, user_id=user_id, due_date='2024-05-10')

        # Get borrowed book copies for the user
        borrowed_books = self.library.get_user_borrowed_book_copy(user_id)

        # Ensure the user has borrowed book copies
        self.assertEqual(len(borrowed_books), 2)

    def test_get_user_borrowed_book_copy_with_no_books_borrowed(self):
        # Get borrowed book copies for a user who has not borrowed any books
        borrowed_books = self.library.get_user_borrowed_book_copy('user8')

        # Ensure the user has not borrowed any book copies
        self.assertEqual(len(borrowed_books), 0)

    def test_search_books_found(self):
        # Search for books with author 'Author 1'
        found_books = self.library.search(attribute='author_id', attribute_value='Author 1')

        # Ensure books matching the search criteria are found
        self.assertEqual(len(found_books), 5)
        self.assertEqual(found_books[0].book.book_id, 1)

    def test_search_no_books_found(self):
        # Search for books with author 'Author 3' which does not exist
        found_books = self.library.search(attribute='author', attribute_value='Author 3')

        # Ensure no books are found for the search criteria
        self.assertEqual(len(found_books), 0)


if __name__ == '__main__':
    unittest.main()
