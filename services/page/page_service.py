"""Services for finding document pages."""

from typing import Any


JsonObject = dict[str, Any]
JsonList = list[JsonObject]


def find_document_pages(
    pages: JsonList,
    document_id: str,
) -> JsonList:
    """Return all pages belonging to the document."""

    return [
        page
        for page in pages
        if page.get("documentId") == document_id
    ]