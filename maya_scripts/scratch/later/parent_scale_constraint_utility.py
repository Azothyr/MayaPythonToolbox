import maya.cmds as cmds


def parent_scale_utility():
    primary_bgc = [0.2, 0.2, 0.35]
    secondary_bgc = [0.35, 0.3, 0.3]
    tertiary_bgc = [0.12, 0.12, 0.12]
    title_bgc = [0.6, 0.6, 0.6]
    odd_label_bgc = [0.4, 0.4, 0.4]
    even_label_bgc = [0.6, 0.6, 0.6]
    button_bgc = [0.5, 0, 0]

    if cmds.window("ParentScaleUtility", exists=True):
        cmds.deleteUI("ParentScaleUtility")
    cmds.window("ParentScaleUtility", title="Parent Scale Utility", widthHeight=(450, 150))

    cmds.columnLayout("base_layout", p="ParentScaleUtility", adj=True, bgc=primary_bgc)
    cmds.columnLayout("title_col", p="base_layout", adj=True, bgc=primary_bgc)
    cmds.rowColumnLayout(
        "columns_layout", nc=2, adj=2, p="base_layout", bgc=secondary_bgc,
        columnWidth=[(1, 225), (2, 225)]
    )
    cmds.columnLayout("col_1", p="columns_layout", adj=True, bgc=primary_bgc)
    cmds.columnLayout("col_2", p="columns_layout", adj=True, bgc=primary_bgc)

    cmds.text("tool_title", p="title_col", height=20, bgc=title_bgc,
              l="Constrain Selection (last object selected or last of the iterations in a group is constrained)")

    cmds.text("prefix_label", l="Prefix: ", p="col_1", height=20, bgc=odd_label_bgc, align="right")
    prefix_input = cmds.textField("prefix_input", p="col_2", height=20, bgc=tertiary_bgc)
    cmds.text("suffix_label", l="Suffix: ", p="col_1", height=20, bgc=odd_label_bgc, align="right")
    suffix_input = cmds.textField("suffix_input", p="col_2", height=20, bgc=tertiary_bgc)
    cmds.text("influence_count_label", l="Influences per iteration: ", p="col_1", height=20, bgc=odd_label_bgc,
              ann="Number of objects selected minus the object to be constrained", align="right")
    influence_count_input = cmds.intField("influence_count_input", p="col_2", height=20, v=1, bgc=tertiary_bgc)
    cmds.text("p_type_label", l="Parent Constraint Type: ", p="col_1", height=20, bgc=even_label_bgc, align="right")
    parent_type_input = cmds.radioButtonGrp(
        labelArray3=["Both", "Translation", "Rotation"], numberOfRadioButtons=3, p="col_2",
        sl=1, bgc=tertiary_bgc, cw3=[45, 80, 65], cal=[(1, "left"), (2, "left"), (3, "left")]
    )
    cmds.text("maintain_offset_label", l="Maintain Offset: ", p="col_1", height=20, bgc=odd_label_bgc, align="right")
    maintain_offset_input = cmds.checkBox("maintain_offset", l="", p="col_2", height=20, v=True, bgc=tertiary_bgc)

    def process_selection(constraint_type):
        possible_constraints = ["parent", "scale"]
        if constraint_type.lower() not in possible_constraints:
            cmds.warning(f"Constraint type must be one of: {', '.join(possible_constraints)}")
            return

        selection = cmds.ls(sl=True)
        if not selection:
            cmds.warning("No objects selected")
            return

        prefix = cmds.textField(prefix_input, query=True, text=True).strip().replace(" ", "_")
        suffix = cmds.textField(suffix_input, query=True, text=True).strip().replace(" ", "_")

        influence_count = cmds.intField(influence_count_input, query=True, value=True)
        if influence_count < 1:
            cmds.warning("Influence count must be at least 1")
            return
        if len(selection) % (influence_count + 1) != 0:
            cmds.warning("Selection count must be a multiple of the influence count + 1 (object to be constrained). Got"
                         f": {len(selection)} and {influence_count} respectively. Equaling a remainder of:"
                         f" {len(selection) % (influence_count + 1)}")
            return

        iterations = len(selection) // (influence_count + 1)

        parent_type = cmds.radioButtonGrp(parent_type_input, query=True, select=True)
        maintain_offset = cmds.checkBox(maintain_offset_input, query=True, value=True)
        p_type_text = ""

        for i in range(iterations):
            influences = selection[i * (influence_count+1): (i + 1) * (influence_count + 1)]
            obj_to_be_constrained = influences.pop(-1)
            print(f"Constraining: {obj_to_be_constrained} with {influences}")

            number = f"{i + 1}".zfill(2)
            name_scheme = f"{prefix}_{number}_{suffix}"

            if constraint_type == "parent":
                match parent_type:
                    case 1:
                        p_type_text = "FULL"
                        cmds.parentConstraint(
                            influences, obj_to_be_constrained, name=f"{name_scheme}__FULL__parentConstraint",
                            mo=maintain_offset)
                    case 2:
                        p_type_text = "TRANSLATION"
                        cmds.parentConstraint(
                            influences, obj_to_be_constrained, name=f"{name_scheme}__TRANSLATION__parentConstraint",
                            mo=maintain_offset, st=["x", "y", "z"])
                    case 3:
                        p_type_text = "ROTATION"
                        cmds.parentConstraint(
                            influences, obj_to_be_constrained, name=f"{name_scheme}__ROTATION__parentConstraint",
                            mo=maintain_offset, sr=["x", "y", "z"])

            if constraint_type == "scale":
                cmds.scaleConstraint(
                    influences, obj_to_be_constrained, name=f"{name_scheme}__FULL__scaleConstraint",
                    mo=maintain_offset)

    def on_parent_execute(*_):
        process_selection("parent")

    def on_scale_execute(*_):
        process_selection("scale")

    cmds.button(l="Perform Parent Constraint", p="col_1", c=on_parent_execute, bgc=button_bgc)
    cmds.button(l="Perform Scale Constraint", p="col_2", c=on_scale_execute, bgc=button_bgc)

    cmds.showWindow("ParentScaleUtility")


if __name__ == "__main__":
    parent_scale_utility()

