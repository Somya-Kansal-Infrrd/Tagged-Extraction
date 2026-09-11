"""Services for building and saving the final request."""

import json
from typing import Any


JsonObject = dict[str, Any]
JsonList = list[JsonObject]


def build_request(
    document: JsonObject,
    document_pages: JsonList,
    collateral_field: JsonObject,
    sub_extraction_fields: JsonList,
) -> JsonObject:
    """Build the final tagged extraction request."""

    return {
        "requestId": document.get("requestId", ""),
        "status": document.get("status", ""),
        "documents": [
            {
                **document,
                "pages": document_pages,
                "extractionField": collateral_field,
                "subExtractionFields": sub_extraction_fields,
            }
        ],
    }


def save_request(
    request_data: JsonObject,
    file_name: str = "final_request.json",
) -> None:
    """Save the final request to a JSON file."""

    with open(
        file_name,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            request_data,
            file,
            indent=4,
        )