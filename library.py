from typing import List
from book_reader import get_book_list, Book_info
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="=> [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ]
)
Librarian_password = "987"


class User():
    role: str

    def __init__(self):
        self.role = "Basic"

    def login(self, password):
        if password == Librarian_password:
            self.role = "Librarian"
            logging.info("Librarian logged in")
            return
        logging.warning("Wrong password")


class Book():
    name: str
    ISBN: str
    author: str
    available: bool
    reserved: bool

    def __init__(self, name, ISBN, author):
        self.name = name
        self.ISBN = ISBN
        self.author = author
        self.available = True
        self.reserved = False

    def borrow_book(self):
        if not self.available:
            logging.warning("Book is not available")
            return

        if self.reserved:
            logging.warning("Book is reserved")
            return

        logging.info("Book borrowed")
        self.available = False

    def return_book(self):
        if self.available:
            logging.warning("Book is already available")
            return

        logging.info("Book returned")
        self.available = True

    def reserve_book(self):
        self.reserved = True
        logging.info(f'Book "{self.name} ({self.ISBN})" reserved')


class Shelf():
    books: List[Book]

    def __init__(self):
        self.books = []

    def show_catalog(self):
        available_books = []
        for book in self.books:
            if book.available:
                available_books.append(book)

        l_name = max([len(book.name) for book in available_books])
        l_author = max([len(book.author) for book in available_books])
        l_ISBN = max([len(str(book.ISBN)) for book in available_books])

        print(f"{'Name':<{l_name}} | {'Author':<{l_author}} | {'ISBN':<{l_ISBN}}")
        for book in available_books:
            print(
                f"{book.name:<{l_name}} | {book.author:<{l_author}} | {book.ISBN:<{l_ISBN}}")

    def add_book(self, book: Book):
        logging.info(f'Book "{book.name} ({book.ISBN})" added by librarian')
        self.books.append(book)

    def remove_book(self, ISBN):
        for book in self.books:
            if book.ISBN == ISBN:
                self.books.remove(book)
                logging.info(
                    f'Book "{book.name} ({book.ISBN})" removed by librarian')
                return
        logging.warning(f'Book with ISBN "{ISBN}" not found')

    def get_books_count(self):
        count = 0
        for book in self.books:
            if book.available:
                count += 1
        return count

    def populate_book(self, filename):
        if not os.path.exists(filename):
            logging.warning(f'File "{filename}" not found')
            return
        book_list = get_book_list(filename)
        for book in book_list:
            self.books.append(Book(book.name, book.ISBN, book.author))
        logging.info(f'{len(book_list)} Books imported from file "{filename}"')


def main():
    logging.info("Program started")

    user = User()
    shelf = Shelf()
    shelf.populate_book("default_books.xlsx")

    while True:
        choice = input(
            "\n1. Login\n2. Show catalog\n3. Add book\n4. Remove book\n5. Borrow book\n6. Return book\n7. Reserve book\n8. Show book count\n9. Import books from file\n10. Exit\nYour choice: ")
        if choice == "1":
            if user.role == "Librarian":
                logging.warning("User is already logged in")
                continue

            password = input("Enter password: ")
            user.login(password)

        elif choice == "2":
            shelf.show_catalog()

        elif choice == "3":
            if user.role != "Librarian":
                logging.warning("User is not a librarian")
                continue

            name = input("Enter name: ")
            ISBN = input("Enter ISBN: ")
            author = input("Enter author: ")
            shelf.add_book(Book(name, ISBN, author))

        elif choice == "4":
            if user.role != "Librarian":
                logging.warning("User is not a librarian")
                continue
            ISBN = input("Enter ISBN: ")
            shelf.remove_book(ISBN)

        elif choice == "5":
            ISBN = input("Enter ISBN: ")
            for book in shelf.books:
                if book.ISBN == ISBN:
                    book.borrow_book()
                    break
            else:
                logging.warning(f'Book with ISBN "{ISBN}" not found')

        elif choice == "6":
            ISBN = input("Enter ISBN: ")
            for book in shelf.books:
                if book.ISBN == ISBN:
                    book.return_book()
                    break
            else:
                logging.warning(f'Book with ISBN "{ISBN}" not found')

        elif choice == "7":
            if user.role != "Librarian":
                logging.warning("User is not a librarian")
                continue
            ISBN = input("Enter ISBN: ")
            for book in shelf.books:
                if book.ISBN == ISBN:
                    book.reserve_book()
                    break
            else:
                logging.warning(f'Book with ISBN "{ISBN}" not found')

        elif choice == "8":
            print(f"Books count: {shelf.get_books_count()}")

        elif choice == "9":
            if user.role != "Librarian":
                logging.warning("User is not a librarian")
                continue
            filename = input("Enter filename: ")
            shelf.populate_book(filename)

        elif choice == "10":
            logging.info("Program ended")
            break


if __name__ == '__main__':
    main()
