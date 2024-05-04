from services.library import Library


lib = Library()


print(lib.create_library(10))
print(lib.add_book("book1", 'the book 1', ["author1","author2","author3"], ["publisher1","publisher2"], [1, 2, 4, 3], color='red'))
print(lib.add_book("book2", 'the book 1', ["author1","author2","author3"], ["publisher1","publisher2"], [5, 6, 7, 8]))
print(lib.add_book("book1", 'the book 1', ["author1","author2","author3"], ["publisher1","publisher2"], [9, 10, 11, 12]))

print(lib.remove_book_copy(3))
print(lib.remove_book_copy(444))

print(lib.borrow_book("book1","user1","2022-05-23"))
print(lib.borrow_book("book1","user1","2022-05-23"))
print(lib.borrow_book("book1","user1","2022-05-23"))
print(lib.borrow_book("book1","user1","2022-05-23"))
print(lib.borrow_book("book1","user1","2022-05-23"))
print(lib.borrow_book("book1","user1","2022-05-23"))
print(lib.borrow_book("book1","user1","2022-05-23"))

print(lib.borrow_book_copy_by_id(7,'user1','2022-05-33'))
print(lib.borrow_book_copy_by_id(7,'user2','2022-05-33'))
print(lib.borrow_book_copy_by_id(7,'user2','2022-05-33'))

print(lib.return_book_copy(7))
print(lib.return_book_copy(7))
print(lib.return_book_copy(47))

print(lib.get_user_borrowed_book_copy('user1'))
print(lib.get_user_borrowed_book_copy('user2'))
print(lib.get_user_borrowed_book_copy('user3'))

book_copies = lib.search('book_id',"book1")
print([(copy.copy_id,copy.rack_no) for copy in book_copies])
print(lib.search('color', 'red'))


print(lib.modify_user_max_borrowed_books_allowed(10,'333'))
print(lib.modify_user_max_borrowed_books_allowed(-300,'user1'))
print(lib.borrow_book("book1","user1","2022-05-23"))

print(lib.modify_general_user_max_borrowed_books_allowed(-111))

book_copies = lib.search('publisher_id',"publisher1")
print(book_copies)
