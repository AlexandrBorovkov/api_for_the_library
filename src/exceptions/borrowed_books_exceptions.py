from fastapi import HTTPException


class BorrowedBookException(HTTPException):

    status_code = 400
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BookNotAvailableException(BorrowedBookException):
    detail="Этой книги нет в наличии"

class LimitationNumberBooksException(BorrowedBookException):
    detail="Читатель уже имеет 3 книги"

class LimitPerInstanceException(BorrowedBookException):
    detail="Читатель уже имеет экземпляр данной книги"

class ActiveIssueWasNotFoundException(BorrowedBookException):
    detail="Запись о выдаче не найдена"
