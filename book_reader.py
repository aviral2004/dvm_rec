from typing import NamedTuple, List
import openpyxl


class Book_info(NamedTuple):
    name: str
    ISBN: str
    author: str


def load_rows(filename):
    wb_obj = openpyxl.load_workbook(filename)
    sheet_obj = wb_obj.active
    return sheet_obj.rows


def get_book_list(filename) -> List[Book_info]:
    book_list = []
    row_generator = load_rows(filename)
    _ = next(row_generator)
    for row in row_generator:
        row_values = [cell_obj.value for cell_obj in row]
        if all(row_values):
            book_obj = Book_info(
                name=row_values[0],
                ISBN=row_values[1],
                author=row_values[2]
            )
            book_list.append(book_obj)
    return book_list
