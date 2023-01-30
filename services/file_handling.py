BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

#Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple:
    result_text = text[start:][:size]
    separator = [',', '.', '!', '?', ';', ':']

    if result_text[-1] not in separator:
        for i in range(len(result_text) - 1, 1, -1):
            if result_text[i] in separator:
                result_text = result_text[:i + 1]
                break
    elif result_text[-1] == '.' and ( result_text[-2] == '.' or text[len(result_text)] == '.'):
        for i in range(len(result_text) - 3, 1, -1):
            if result_text[i] in separator:
                result_text = result_text[:i + 1]
                break

    return result_text, len(result_text)

#Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, encoding='utf-8') as file:
        read_file: str = file.read()
        start: int = 0
        counter: int = 1

        while start < len(read_file) - PAGE_SIZE:
            formatted_text: tuple = _get_part_text(read_file, start=start, size=PAGE_SIZE)
            book[counter] = formatted_text[0].lstrip()
            start += formatted_text[1]
            counter += 1
        
        last_string = _get_part_text(read_file, start=start, size=len(read_file) - start)
        book[counter] = last_string[0].lstrip()


#Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(BOOK_PATH)
