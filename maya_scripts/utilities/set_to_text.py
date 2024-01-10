import maya.cmds as cmds
import pyperclip


def joint_hierarchy_to_text(root="Skeleton", level=0):
    """
    Recursively formats the joint hierarchy starting from the root.

    :param root: The root transform to start listing joints from.
    :param level: The current level in the hierarchy for indentation purposes.
    :return: A string representing the formatted hierarchy.
    """
    hierarchy = ""
    # Use "|-- " for child joints and "|- " for the root
    prefix = "     " * level + ("|-- " if level > 0 else "|- ")

    # Find all children of the root that are joints
    children = cmds.listRelatives(root, children=True, type="joint") or []

    # Add the current joint to the hierarchy string
    hierarchy += prefix + root + "\n"

    # Recursively add children to the hierarchy string
    for child in children:
        hierarchy += joint_hierarchy_to_text(child, level + 1)

    return hierarchy


def copy_text_to_clipboard(text):
    """
    Copies the given text to the clipboard.

    :param text: The text to copy to the clipboard.
    """
    pyperclip.copy(text)


if __name__ == "__main__":
    cog = None
    for obj in cmds.ls():
        if "cog" in obj.lower() and cmds.nodeType(obj) == "joint":
            cog = str(obj)
            break

    if cog is None:
        raise RuntimeError("No COG joint found.")

    # Creates a Markdown code block in the output
    md_joint_hierarchy_text = f"```\n{joint_hierarchy_to_text(cog)}```"
    html_joint_hierarchy_text = f"<pre><code>{joint_hierarchy_to_text(cog)}</code></pre>"
    print(html_joint_hierarchy_text)
    # Copies the text to the clipboard
    copy_text_to_clipboard(html_joint_hierarchy_text)
