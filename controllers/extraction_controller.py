"""Controller for tagged extraction."""

from flask import jsonify, request

from services.data.data_service import load_json_file
from services.document.document_service import find_document
from services.field.field_service import (
    filter_visible_records,
    find_collateral_field,
    find_collateral_sub_fields,
)
from services.page.page_service import find_document_pages
from services.reconstruction.reconstruction_service import (
    build_request,
    save_request,
)


def tagged_extraction():
    """Process a document and return the reconstructed request."""

    data = request.get_json()

    if not data or "documentId" not in data:
        return jsonify({
            "error": "documentId is required"
        }), 400

    document_id = data["documentId"]

    documents = load_json_file("document.json")
    pages = load_json_file("page.json")
    extraction_fields = load_json_file(
        "extraction_field.json"
    )
    sub_extraction_fields = load_json_file(
        "sub_extraction_field.json"
    )

    document = find_document(
        documents,
        document_id,
    )

    if document is None:
        return jsonify({
            "error": f"Document not found: {document_id}"
        }), 404

    document_pages = find_document_pages(
        pages,
        document_id,
    )

    collateral_field = find_collateral_field(
        extraction_fields
    )

    if collateral_field is None:
        return jsonify({
            "error": "Collateral Object List field not found"
        }), 404

    collateral_id = collateral_field.get("_id")

    if not isinstance(collateral_id, str):
        return jsonify({
            "error": "Collateral field does not have a valid ID"
        }), 400

    collateral_sub_fields = find_collateral_sub_fields(
        sub_extraction_fields,
        collateral_id,
    )

    final_sub_extraction_fields = filter_visible_records(
        collateral_sub_fields
    )

    original_request = build_request(
    document,
    document_pages,
    collateral_field,
    final_sub_extraction_fields,
)

    save_request(original_request)

    return jsonify(original_request), 200