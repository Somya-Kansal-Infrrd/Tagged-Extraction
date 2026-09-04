import json

# 1. Load all JSON files

with open("document.json", "r") as file:
    documents = json.load(file)

with open("page.json", "r") as file:
    pages = json.load(file)

with open("extraction_field.json", "r") as file:
    extraction_fields = json.load(file)

with open("sub_extraction_field.json", "r") as file:
    sub_extraction_fields = json.load(file)


print("All files loaded successfully")

print("Documents:", len(documents))
print("Pages:", len(pages))
print("Extraction fields:", len(extraction_fields))
print(
    "Sub extraction fields:",
    len(sub_extraction_fields)
)

# 2. Document ID
document_id = (
    "14cdfdba-34d0-4209-bbf6-ebf771a5646e_document-1"
)

# 3. Find the complete document

document = None

for item in documents:
    if item.get("_id") == document_id:
        document = item
        break


if document:
    print("\nDocument found:")
    print(document)
else:
    print("\nDocument not found")


# 4. Find all pages for this document

document_pages = []

for page in pages:
    if page.get("documentId") == document_id:
        document_pages.append(page)


print("\nPages found:", len(document_pages))

for page in document_pages:
    print(
        "Page:",
        page.get("_id"),
        "| Page Number:",
        page.get("pageNumber")
    )

# 5. Find Collateral Object List field

collateral_field = None

for field in extraction_fields:
    if (
        field.get("fieldName") == "Collateral"
        and field.get("fieldType") == "Object List"
    ):
        collateral_field = field
        break


if collateral_field:
    print("\nCollateral Object List field found:")
    print(collateral_field)

    collateral_id = collateral_field.get("_id")

    print("\nCollateral _id:", collateral_id)

else:
    print("\nCollateral Object List field not found")
    collateral_id = None


# 6. Find all ADD and TAGGED sub-extraction records
#    for the Collateral field

collateral_sub_fields = []

if collateral_id:

    for sub_field in sub_extraction_fields:

        # Same extraction field
        if sub_field.get("extractionFieldId") != collateral_id:
            continue

        # Only ADD and TAGGED records
        if sub_field.get("taggedStatus") not in [
            "ADD",
            "TAGGED"
        ]:
            continue

        collateral_sub_fields.append(sub_field)


print(
    "\nCollateral ADD/TAGGED records found:",
    len(collateral_sub_fields)
)

for record in collateral_sub_fields:
    print(
        "ID:",
        record.get("_id"),
        "| Status:",
        record.get("taggedStatus")
    )

# 7. Take the COMPLETE record if it contains
#    at least one value where hidden == false


final_sub_extraction_fields = []

for record in collateral_sub_fields:

    has_visible_value = False

    for value in record.get("values", []):

        if value.get("hidden") is False:
            has_visible_value = True
            break

    if has_visible_value:
        # Take the COMPLETE record
        final_sub_extraction_fields.append(record)



# 8. Print final records

print(
    "\nFinal sub-extraction records:",
    len(final_sub_extraction_fields)
)

for record in final_sub_extraction_fields:

    print("\n----------------------------------------")

    print("Record ID:", record.get("_id"))

    print(
        "Tagged Status:",
        record.get("taggedStatus")
    )

    print(
        "Extraction Field ID:",
        record.get("extractionFieldId")
    )

    print(
        "Document ID:",
        record.get("documentId")
    )

    print(
        "Object ID:",
        record.get("objectId")
    )

    print("Complete Record:")

    print(
        json.dumps(
            record,
            indent=4
        )
    )


# 9. Build final request body


original_request = {
    "requestId": document.get("requestId", ""),
    "status": document.get("status", ""),
    "documents": [
        {
            # Complete document
            **document,

            # All pages
            "pages": document_pages,

            # Complete Collateral extraction field
            "extractionField": collateral_field,

            # All matching ADD/TAGGED sub-extraction records
            "subExtractionFields": final_sub_extraction_fields
        }
    ]
}


# 10. Print final request body


print("\nFinal request body:")

print(
    json.dumps(
        original_request,
        indent=4
    )
)

# 11. Save final request body to a separate file


with open("final_request.json", "w") as file:
    json.dump(
        original_request,
        file,
        indent=4
    )

print("\nFinal request saved to final_request.json")