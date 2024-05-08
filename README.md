### Library Management System

A command line application for a library management system built using python

### Uml Diagrams

- Use Case Diagram

![LBMS Use Case vpd](https://github.com/Team-Panthers/library-management-sys/assets/119736310/5df7006e-dd67-4344-a3e3-0a7f891caf0f)


- Class Diagram

![Photo from Fola](https://github.com/Team-Panthers/library-management-sys/assets/119736310/65756cff-4576-497b-9e3a-8f8314daf2e2)


- Sequence diagram
![Sequence diagram LBS (2)](https://github.com/Team-Panthers/library-management-sys/assets/119736310/24d93275-3539-46c5-8493-8c7e093f2930)





### Details about the Library

- The library will have one or more copies of multiple books

- The library will have multiple racks and each rack can contain at most one copy of any book.

Each book will have the following properties

- Book ID
- Title
- Authors
- Publishers
- Details about Book Copies

There could be multiple copies of the same book.
- Each book copy will have a unique ID.
- Each book copy will be placed on a rack.
- Each book copy can be borrowed by a user with a specific due date.

Every rack will have a unique rack number (numbered serially from 1 to n where n is the total number of racks).

Details about User:
- User details: User ID, Name
- A user can borrow a maximum of 5 books.


The functions that the library management system can do:
- Create a library.
- Add a book to the library. The book should be added to the first available rack.
- Remove a book copy from the library.
- Allow a user to borrow a book copy given the book id, user id, and due date. The first available copy based on the rack number should be provided.
- Allow a user to borrow a book copy given the book copy id, user id, and due date.
- Allow a user to return a book copy given the book copy id. The book should be added to the first available rack.
- Allow a user to print the book copy ids of all the books borrowed by them.
- Allow a user to search for books using few book properties (Book ID, Title, Author, Publisher). Searching should return details about all the book copies that match the search query.
