import json
import logging
from typing import Any


# Logging configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# Type aliases

JsonObject = dict[str, Any]
JsonList = list[JsonObject]


# Load JSON file


def load_json_file(file_name: str) -> Any:
    """Load and return JSON data from a file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


# Find document

def find_document(
    documents: JsonList,
    document_id: str,
) -> JsonObject | None:
    """Find a document using its ID."""
    for document in documents:
        if document.get("_id") == document_id:
            return document

    return None


# Find pages for document


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


# Find Collateral Object List field

def find_collateral_field(
    extraction_fields: JsonList,
) -> JsonObject | None:
    """Find the Collateral Object List extraction field."""
    for field in extraction_fields:
        if (
            field.get("fieldName") == "Collateral"
            and field.get("fieldType") == "Object List"
        ):
            return field

    return None


# Find ADD and TAGGED records


def find_collateral_sub_fields(
    sub_extraction_fields: JsonList,
    collateral_id: str,
) -> JsonList:
    """Find all ADD and TAGGED Collateral records."""
    matching_records: JsonList = []

    for sub_field in sub_extraction_fields:
        if sub_field.get("extractionFieldId") != collateral_id:
            continue

        if sub_field.get("taggedStatus") not in {
            "ADD",
            "TAGGED",
        }:
            continue

        matching_records.append(sub_field)

    return matching_records


# Filter records having hidden == false


def filter_visible_records(
    records: JsonList,
) -> JsonList:
    """
    Return complete records containing at least one
    value where hidden is False.
    """
    final_records: JsonList = []

    for record in records:
        for value in record.get("values", []):
            if value.get("hidden") is False:
                final_records.append(record)
                break

    return final_records

# Build final request


def build_request(
    document: JsonObject,
    document_pages: JsonList,
    collateral_field: JsonObject,
    sub_extraction_fields: JsonList,
) -> JsonObject:
    """Build the final request body."""
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


# Main


def main() -> None:
    """Run the document reconstruction process."""

    # 1. Load all JSON files
    documents: JsonList = load_json_file(
        "document.json"
    )
    pages: JsonList = load_json_file(
        "page.json"
    )
    extraction_fields: JsonList = load_json_file(
        "extraction_field.json"
    )
    sub_extraction_fields: JsonList = load_json_file(
        "sub_extraction_field.json"
    )

    logger.info("All files loaded successfully")
    logger.info("Documents: %d", len(documents))
    logger.info("Pages: %d", len(pages))
    logger.info(
        "Extraction fields: %d",
        len(extraction_fields),
    )
    logger.info(
        "Sub extraction fields: %d",
        len(sub_extraction_fields),
    )

    # 2. Document ID
    document_id = (
        "14cdfdba-34d0-4209-bbf6-ebf771a5646e_document-1"
    )

    # 3. Find complete document
    document = find_document(
        documents,
        document_id,
    )

    if document is None:
        logger.error(
            "Document not found: %s",
            document_id,
        )
        return

    logger.info(
        "Document found: %s",
        document.get("_id"),
    )

    # 4. Find all pages
    document_pages = find_document_pages(
        pages,
        document_id,
    )

    logger.info(
        "Pages found: %d",
        len(document_pages),
    )

    for page in document_pages:
        logger.info(
            "Page: %s | Page Number: %s",
            page.get("_id"),
            page.get("pageNumber"),
        )

    # 5. Find Collateral Object List field
    collateral_field = find_collateral_field(
        extraction_fields
    )

    if collateral_field is None:
        logger.error(
            "Collateral Object List field not found"
        )
        return

    collateral_id = collateral_field.get("_id")

    if not isinstance(collateral_id, str):
        logger.error(
            "Collateral field does not have a valid ID"
        )
        return

    logger.info(
        "Collateral Object List field found"
    )
    logger.info(
        "Collateral ID: %s",
        collateral_id,
    )

    # 6. Find ADD and TAGGED records
    collateral_sub_fields = (
        find_collateral_sub_fields(
            sub_extraction_fields,
            collateral_id,
        )
    )

    logger.info(
        "Collateral ADD/TAGGED records found: %d",
        len(collateral_sub_fields),
    )

    for record in collateral_sub_fields:
        logger.info(
            "ID: %s | Status: %s",
            record.get("_id"),
            record.get("taggedStatus"),
        )

    # 7. Keep complete records with hidden == false
    final_sub_extraction_fields = (
        filter_visible_records(
            collateral_sub_fields
        )
    )

    logger.info(
        "Final sub-extraction records: %d",
        len(final_sub_extraction_fields),
    )

    for record in final_sub_extraction_fields:
        logger.info(
            "Selected record: %s | Status: %s",
            record.get("_id"),
            record.get("taggedStatus"),
        )

    # 8. Build final request
    original_request = build_request(
        document,
        document_pages,
        collateral_field,
        final_sub_extraction_fields,
    )

    logger.info("Final request body created")

    # 9. Save final request
    output_file = "final_request.json"

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            original_request,
            file,
            indent=4,
        )

    logger.info(
        "Final request saved to %s",
        output_file,
    )


if __name__ == "__main__":
    main()