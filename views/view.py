from services.library import library_service

lib = library_service()


def create_library(no_of_rack, **kwargs):
    no_of_rack, error = lib.create_library(no_of_rack, **kwargs)

    if error:
        print(error)
        return
    print(f'Created library with {no_of_rack} racks')


def add_book_to_library(book_id, title, authors, publishers, book_copy_ids, **kwargs):
    rack_no_list, error = lib.add_book(book_id, title, authors, publishers, book_copy_ids, **kwargs)

    if error:
        print("Error Adding Books")
        return

    cleaned_rack_no_list = [rack_no for rack_no in rack_no_list if rack_no is not None]

    if cleaned_rack_no_list:
        comma_separated_rack_no = ', '.join(map(str, cleaned_rack_no_list))
        print(f"Added Book to racks: {comma_separated_rack_no}")

    if None in rack_no_list:
        print("Rack not available")


def remove_book_copy_from_library(copy_id):
    result, error = lib.remove_book_copy(copy_id)
    if error:
        print(error)
        return
    book_copy, rack_no = result
    print(f"Removed book copy: {book_copy.copy_id} from rack: {rack_no}")


def borrow_book_from_library(book_id,user_id,due_date):
    rack_no, error = lib.borrow_book(book_id,user_id,due_date)
    if error:
        print(error)
        return

    print(f"Borrowed Book from rack: {rack_no}")


def borrow_book_copy_from_library(copy_id,user_id,due_date):
    rack_no, error = lib.borrow_book_copy_by_id(copy_id,user_id,due_date)

    if error:
        print(error)
        return

    print(f"Borrowed Book Copy from rack: {rack_no}")


def return_book_copy_to_library(copy_id):
    rack_info, error = lib.return_book_copy(copy_id)
    if error:
        print(error)
        return
    print(rack_info)


def print_borrowed_book_copy_by_user(user_id):
    book_copies = lib.get_user_borrowed_book_copy(user_id)

    for book_copy in book_copies:
        print(f"Book Copy: {book_copy.copy_id} {book_copy.due_date}")


def search_library_for_book_by_attribute(attribute,attribute_value):
    book_copies = lib.search(attribute,attribute_value)

    for book_copy in book_copies:
        comma_separated_author = ', '.join(map(str, book_copy.book.author_id))
        comma_separated_publisher = ', '.join(map(str, book_copy.book.publisher_id))
        rack_no = book_copy.rack_no if not book_copy.borrowed_by else -1
        print(f"Book Copy: {book_copy.copy_id} {book_copy.book.book_id} {book_copy.book.title} {comma_separated_author} {comma_separated_publisher} {rack_no} {book_copy.borrowed_by if rack_no == -1 else ''} {book_copy.due_date if rack_no == -1 else ''}")

#
# create_library(10)
#
# add_book_to_library(1, 'the book 1', ["author1","author2","author3"], ["publisher1","publisher2"], [1, 2, 4, 3,5,6,7], color='red')
#
# remove_book_copy_from_library(2)
#
# borrow_book_from_library(1,'user1',"2023-12-23")
# borrow_book_from_library(1,'user1',"2023-12-23")
# borrow_book_from_library(1,'user1',"2023-12-23")
# borrow_book_from_library(1,'user1',"2023-12-23")
# borrow_book_from_library(1,'user1',"2023-12-23")
# borrow_book_from_library(1,'user1',"2023-12-23")
# borrow_book_from_library(1,'user1',"2023-12-23")
#
# borrow_book_copy_from_library(7,'user2',"2023-12-12")
#
# return_book_copy_to_library(4)
#
# print_borrowed_book_copy_by_user('user1')
#
# search_library_for_book_by_attribute('authors','author2')
