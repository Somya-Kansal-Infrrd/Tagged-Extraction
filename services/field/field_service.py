"""Services for finding and filtering extraction fields."""

from typing import Any


JsonObject = dict[str, Any]
JsonList = list[JsonObject]


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


def filter_visible_records(
    records: JsonList,
) -> JsonList:
    """Keep records having at least one value with hidden=False."""

    final_records: JsonList = []

    for record in records:
        for value in record.get("values", []):
            if value.get("hidden") is False:
                final_records.append(record)
                break

    return final_records