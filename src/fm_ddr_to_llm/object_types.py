"""SPEC-001: DDR XML Object Type Registry.

Defines FileMaker object types and their XML tag patterns for ID extraction.
Each entry maps an object type to:
- tag: The XML element name in the DDR
- id_attr: The attribute containing the internal FM object ID
- name_attr: The attribute containing the human-readable name
- parent_catalog: The enclosing catalog element (for context)
- extra_attrs: Additional attributes worth extracting
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectTypeDef:
    """Definition of a FileMaker object type and how to extract it from DDR XML."""

    type_name: str
    tag: str
    id_attr: str = "id"
    name_attr: str = "name"
    parent_catalog: str = ""
    extra_attrs: tuple[str, ...] = ()

    def build_pattern(self) -> re.Pattern[str]:
        """Build a regex pattern that extracts id, name, and extra attrs from an opening tag.

        Returns a compiled regex with named groups: 'id', 'name', and any extra attr names.
        """
        # Match the opening tag with id and name attributes in any order.
        # We capture each attribute individually since XML attribute order varies.
        return re.compile(
            rf"<{re.escape(self.tag)}\s+"
            rf'(?=[^>]*\b{re.escape(self.id_attr)}="(?P<id>[^"]*)")'
            rf'(?=[^>]*\b{re.escape(self.name_attr)}="(?P<name>[^"]*)")'
            rf"[^>]*?>",
            re.DOTALL,
        )


# The canonical registry of FM object types in DDR XML.
# Order matches the DDR XML grammar (FileMaker Pro 19+).
OBJECT_TYPES: dict[str, ObjectTypeDef] = {}


def _register(*defs: ObjectTypeDef) -> None:
    for d in defs:
        OBJECT_TYPES[d.type_name] = d


_register(
    ObjectTypeDef(
        type_name="base_table",
        tag="BaseTable",
        parent_catalog="BaseTableCatalog",
        extra_attrs=("records",),
    ),
    ObjectTypeDef(
        type_name="field",
        tag="Field",
        parent_catalog="FieldCatalog",
        extra_attrs=("fieldType", "dataType"),
    ),
    ObjectTypeDef(
        type_name="table_occurrence",
        tag="Table",
        parent_catalog="TableList",
        extra_attrs=("baseTable", "baseTableId"),
    ),
    ObjectTypeDef(
        type_name="relationship",
        tag="Relationship",
        parent_catalog="RelationshipList",
        # Relationships only have id, no name attr in the tag.
        # We'll handle name extraction separately.
    ),
    ObjectTypeDef(
        type_name="layout",
        tag="Layout",
        parent_catalog="LayoutCatalog",
        extra_attrs=("includeInMenu",),
    ),
    ObjectTypeDef(
        type_name="script",
        tag="Script",
        parent_catalog="ScriptCatalog",
        extra_attrs=("includeInMenu",),
    ),
    ObjectTypeDef(
        type_name="script_step",
        tag="Step",
        parent_catalog="StepList",
        extra_attrs=("enable",),
    ),
    ObjectTypeDef(
        type_name="value_list",
        tag="ValueList",
        parent_catalog="ValueListCatalog",
    ),
    ObjectTypeDef(
        type_name="custom_function",
        tag="CustomFunction",
        parent_catalog="CustomFunctionCatalog",
        extra_attrs=("parameters", "visible"),
    ),
    ObjectTypeDef(
        type_name="custom_menu",
        tag="CustomMenu",
        parent_catalog="CustomMenuCatalog",
    ),
    ObjectTypeDef(
        type_name="custom_menu_set",
        tag="CustomMenuSet",
        parent_catalog="CustomMenuSetCatalog",
    ),
    ObjectTypeDef(
        type_name="account",
        tag="Account",
        parent_catalog="AccountCatalog",
        extra_attrs=("status",),
    ),
    ObjectTypeDef(
        type_name="privilege_set",
        tag="PrivilegeSet",
        parent_catalog="PrivilegeCatalog",
    ),
    ObjectTypeDef(
        type_name="extended_privilege",
        tag="ExtendedPrivilege",
        parent_catalog="ExtendedPrivilegeCatalog",
    ),
    ObjectTypeDef(
        type_name="external_data_source",
        tag="ExternalDataSource",
        parent_catalog="ExternalDataSourcesCatalog",
    ),
    ObjectTypeDef(
        type_name="layout_group",
        tag="Group",
        parent_catalog="LayoutCatalog",
    ),
    ObjectTypeDef(
        type_name="script_group",
        tag="Group",
        parent_catalog="ScriptCatalog",
    ),
)
