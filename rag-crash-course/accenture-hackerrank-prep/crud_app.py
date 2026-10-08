from __future__ import annotations

from itertools import count
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)


class DocumentPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None


class DocumentOut(DocumentIn):
    id: int


class DocumentRepository:
    """In-memory store; swap for a DB-backed repo without touching routes."""

    def __init__(self) -> None:
        self._items: dict[int, DocumentOut] = {}
        self._ids = count(1)

    def list(self, tag: str | None = None) -> list[DocumentOut]:
        docs = list(self._items.values())
        return [d for d in docs if tag in d.tags] if tag else docs

    def get(self, doc_id: int) -> DocumentOut | None:
        return self._items.get(doc_id)

    def create(self, data: DocumentIn) -> DocumentOut:
        doc = DocumentOut(id=next(self._ids), **data.model_dump())
        self._items[doc.id] = doc
        return doc

    def replace(self, doc_id: int, data: DocumentIn) -> DocumentOut:
        doc = DocumentOut(id=doc_id, **data.model_dump())
        self._items[doc_id] = doc
        return doc

    def delete(self, doc_id: int) -> bool:
        return self._items.pop(doc_id, None) is not None


_repo = DocumentRepository()


def get_repo() -> DocumentRepository:
    return _repo


Repo = Annotated[DocumentRepository, Depends(get_repo)]
app = FastAPI(title="Documents API")


def _require(repo: DocumentRepository, doc_id: int) -> DocumentOut:
    doc = repo.get(doc_id)
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"document {doc_id} not found")
    return doc


@app.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def create_document(body: DocumentIn, repo: Repo) -> DocumentOut:
    return repo.create(body)


@app.get("/documents", response_model=list[DocumentOut])
def list_documents(repo: Repo, tag: str | None = None) -> list[DocumentOut]:
    return repo.list(tag)


@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: int, repo: Repo) -> DocumentOut:
    return _require(repo, doc_id)


@app.put("/documents/{doc_id}", response_model=DocumentOut)
def replace_document(doc_id: int, body: DocumentIn, repo: Repo) -> DocumentOut:
    _require(repo, doc_id)
    return repo.replace(doc_id, body)


@app.patch("/documents/{doc_id}", response_model=DocumentOut)
def patch_document(doc_id: int, body: DocumentPatch, repo: Repo) -> DocumentOut:
    current = _require(repo, doc_id)
    merged = current.model_copy(update=body.model_dump(exclude_unset=True))
    return repo.replace(doc_id, DocumentIn(**merged.model_dump(exclude={"id"})))


@app.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, repo: Repo) -> None:
    if not repo.delete(doc_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"document {doc_id} not found")


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    c = TestClient(app)
    r = c.post("/documents", json={"title": "RAG", "content": "chunk, embed, retrieve", "tags": ["ai"]})
    assert r.status_code == 201 and r.json()["id"] == 1
    c.post("/documents", json={"title": "SQL", "content": "joins"})
    assert len(c.get("/documents").json()) == 2
    assert [d["title"] for d in c.get("/documents", params={"tag": "ai"}).json()] == ["RAG"]
    assert c.patch("/documents/1", json={"title": "RAG 101"}).json()["content"] == "chunk, embed, retrieve"
    assert c.put("/documents/1", json={"title": "X", "content": "Y"}).json()["tags"] == []
    assert c.post("/documents", json={"title": "", "content": "x"}).status_code == 422
    assert c.get("/documents/99").status_code == 404
    assert c.delete("/documents/1").status_code == 204
    assert c.delete("/documents/1").status_code == 404
    print("CRUD tests passed.")
