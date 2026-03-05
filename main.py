from fastapi import FastAPI
from models import Notebook
from pydantic import BaseModel

class NoteIn(BaseModel):
    title: str
    content: str
    author: str

app = FastAPI(title="Notes API")
notebook = Notebook()

@app.get("/notes")
def get_notes():
    """
    Возвращает список всех заметок
    """
    notes = notebook.get_all_notes()
    return [note.to_dict() for note in notes]

@app.post("/notes")
def create_note(note_data: NoteIn):
    """
    Создание новой заметки
    """
    note = notebook.add_note(
        title=note_data.title,
        content=note_data.content,
        author=note_data.author
    )
    if note is None:
        return {"error": "Note is not valid (title/author empty or content too long)"}
    return note.to_dict()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
