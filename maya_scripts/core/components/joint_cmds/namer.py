from core.components.selection_renamer import perform_rename


def rename_joints(joints: list[str], schema: str) -> None:
    """
    renames joints based on the schema.
    :param joints: list of joints to rename
    :param schema: schema to rename joints with
    :return None:
    """
    perform_rename(schema, joints)
