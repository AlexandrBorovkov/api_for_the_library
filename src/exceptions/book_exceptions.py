from fastapi import HTTPException


class BookException(HTTPException):

    status_code = 400
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BookNotAvailableException(BookException):
    detail="Этой книги нет в наличии"

class LimitationNumberBooksException(BookException):
    detail="Читатель уже имеет 3 книги"

class LimitPerInstanceException(BookException):
    detail="Читатель уже имеет экземпляр данной книги"

class ActiveIssueWasNotFoundException(BookException):
    detail="Запись о выдаче не найдена"

class TheBookWasNotFoundException(BookException):
    detail="Книга не найдена"

class UniqueISBNException(BookException):
    detail="Такой ISBN уже существует"
