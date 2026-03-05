import datetime
import json
from tkinter.ttk import Notebook

class Note:
    """
    Класс заметок с заголовками, содержанием и автором
    """
    def __init__(self, title: str, content: str, author: str) -> None:
        self.id = None
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.datetime.now().isoformat()

    def is_valid(self) -> bool:
        """
        Проверка на правильность заполнения:
        title и author не пустые, а длина содержимого не более 300 символов.
        :return: Bool
        """
        if self.title == "" or len(self.content) > 300 or self.author == "":
            return False
        else:
            return True

    def to_dict(self) -> dict:
        """
        Возвращает объект класса в виде словаря
        :return: dict
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at
        }


class Notebook:
    """
    Класс представляет собой коллекцию заметок.
    Автоматически присваивает номер новой заметке.
    """
    def __init__(self):
        self._next_id = 1
        self.notes_list = []

    def add_note(self, title: str, content: str, author: str) -> Note | None:
        """
        Добавляет новую заметку в коллекцию.
        Перед добавлением проверяет на правильность заполнения.
        :param title: название заметки
        :param content: содержание заметки
        :param author: автор заметки
        :return: возвращает либо новую заметку, либо ничего
        """
        note = Note(title, content, author)
        if note.is_valid():
            note.id = self._next_id
            self._next_id += 1
            self.notes_list.append(note)
            return note
        else:
            return None

    def get_all_notes(self) -> list[Note]:
        """
        Получение полного списка заметок
        :return: возвращает список добавленных заметок
        """
        return self.notes_list

    def find_by_author(self, author: str) -> list[Note] | None:
        """
        Ищет все заметки указанного автора.
        :param author: имя автора
        :return: возвращает либо список заметок, либо ничего.
        """
        found_notes = []
        for note in self.notes_list:
            if author == note.author:
                found_notes.append(note)
        if len(found_notes) == 0:
            return None
        else:
            return found_notes

    def delete_note(self, note_id: int) -> bool:
        """
        Функция удаления заметки с заданным id.
        :param note_id: номер по порядку заметки
        :return: возвращает true в случае удаления
        """
        for note in self.notes_list:
            if note.id == note_id:
                self.notes_list.remove(note)
                return True
        return False

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет список заметок в JSON файл
        :param filename: путь к файлу
        :return: ничего, просто сохраняет данные
        """
        notes_to_save = []
        for note in self.notes_list:
            notes_to_save.append(note.to_dict())
        with open(filename, "w") as file:
            json.dump(notes_to_save, file)

    def load_from_file(self, filename: str) -> None:
        """
        Из списка словарей создает заметку по каждому
        :param filename: путь к файлу
        :return: None
        """
        self.notes_list = []
        with open(filename, "r") as file:
            data = json.load(file)

        max_id = 0

        for note_data in data:
            note = Note(note_data["title"], note_data["content"], note_data["author"])
            note.id = note_data["id"]
            note.created_at = note_data["created_at"]
            self.notes_list.append(note)
            if note.id > max_id:
                max_id = note.id

        self._next_id = max_id + 1


# Создаем и наполняем заметками
notebook = Notebook()
notebook.add_note("Купить продукты", "Молоко, хлеб", "Иван")
notebook.add_note("Заметка 2", "Какой-то контент", "Иван")
notebook.add_note("Список книг", "1984, Скотный двор", "Петр")

# Сохраняем
notebook.save_to_file("notes.json")
print("Заметки сохранены")

# Создаем новую пустую записную книжку
notebook2 = Notebook()
print(f"Заметок до загрузки: {len(notebook2.get_all_notes())}")  # 0

# Загружаем
notebook2.load_from_file("notes.json")
print(f"Заметок после загрузки: {len(notebook2.get_all_notes())}")  # 3

# Проверяем ID и следующий счетчик
print(f"ID загруженных заметок: {[note.id for note in notebook2.get_all_notes()]}")
# Должно быть [1, 2, 3]

# Добавляем новую заметку в загруженную книжку
note4 = notebook2.add_note("Новая заметка", "После загрузки", "Иван")
print(f"ID новой заметки: {note4.id}")  # Должно быть 4
