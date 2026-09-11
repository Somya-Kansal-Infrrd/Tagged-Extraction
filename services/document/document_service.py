"""Services for finding document information."""

from typing import Any


JsonObject = dict[str, Any]
JsonList = list[JsonObject]


def find_document(
    documents: JsonList,
    document_id: str,
) -> JsonObject | None:
    """Find a document using its ID."""

    for document in documents:
        if document.get("_id") == document_id:
            return document

    return None