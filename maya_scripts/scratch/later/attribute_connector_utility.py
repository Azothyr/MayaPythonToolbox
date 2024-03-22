import maya.cmds as cmds
import re


def connection_utility():
    primary_bgc = [0.2, 0.2, 0.35]
    secondary_bgc = [0.35, 0.3, 0.3]
    tertiary_bgc = [0, 0.05, 0.05]
    label_bgc = [0.1, 0.1, 0.1]
    button_bgc = [0.5, 0, 0]

    if cmds.window("ConnectionUtility", exists=True):
        cmds.deleteUI("ConnectionUtility")
    cmds.window("ConnectionUtility", title="Connection Utility", widthHeight=(300, 100))

    cmds.columnLayout("base_layout", p="ConnectionUtility", adj=True, bgc=primary_bgc)
    cmds.rowColumnLayout(
        "columns_layout", nc=2, adj=2, p="base_layout", bgc=secondary_bgc,
        columnWidth=[(1, 150), (2, 200)]
    )
    cmds.columnLayout("col_1", p="columns_layout", adj=True, bgc=primary_bgc)
    cmds.columnLayout("col_2", p="columns_layout", adj=True, bgc=primary_bgc)
    cmds.columnLayout("button_col", p="base_layout", adj=True, bgc=primary_bgc)

    cmds.text("controller_label", l="Controller: ", p="col_1", height=20, bgc=label_bgc, align="right")
    cmds.text("controller_attr_label", l="From Attribute: ", p="col_1", height=20, bgc=label_bgc, align="right")
    cmds.text("follower_attr_label", l="To Selection's Attribute: ", p="col_1", height=20, bgc=label_bgc,
              align="right")
    cmds.text("action_label", l="Action: ", p="col_1", height=20, bgc=label_bgc,
              align="right")
    controller_input = cmds.textField("controller_input", p="col_2", bgc=tertiary_bgc)
    controller_attr_input = cmds.textField("controller_attr_input", p="col_2", bgc=tertiary_bgc)
    follower_attr_input = cmds.textField("follower_attr_input", p="col_2", bgc=tertiary_bgc)
    action_type_input = cmds.radioButtonGrp(
        labelArray2=["Add", "Remove"], numberOfRadioButtons=2, p="col_2",
        sl=1, bgc=tertiary_bgc, cw2=[60, 60], cal=[(1, "left"), (2, "left")]
    )

    def on_execute(*_, **__):
        print("EXECUTING CONNECTION UTILITY...")
        selection = cmds.ls(sl=True)
        controller = cmds.textField(controller_input, query=True, text=True).strip().replace(" ", "_")
        controller_attr = cmds.textField(controller_attr_input, query=True, text=True).strip().replace(" ", "_")
        follower_attr = cmds.textField(follower_attr_input, query=True, text=True).strip().replace(" ", "_")
        iter_attr = follower_attr
        action_type = cmds.radioButtonGrp(action_type_input, query=True, sl=True)

        override_pattern = re.compile(r"override", re.IGNORECASE)
        confirm_override = True if override_pattern.search(follower_attr) else False
        attr_search_pattern = re.compile(r"#+")
        name_search_pattern = re.compile(r"\d+")

        if not selection:
            cmds.warning("No objects selected")
            return
        if not cmds.objExists(controller):
            cmds.warning(f"{controller} does not exist")
            return
        if not cmds.attributeQuery(controller_attr, node=controller, exists=True):
            cmds.warning(f"{controller_attr} does not exist on {controller}")
            return
        for count, obj in enumerate(selection, start=1):
            if obj == controller:
                cmds.warning(f"{obj} is the controller, skipping...")
                continue

            print(f"Working on OBJECT: {obj}, SELECTION INDEX: {count - 1}")

            attr_match = attr_search_pattern.search(follower_attr)
            if attr_match:
                hash_sequence = attr_match.group()
                name_match = name_search_pattern.search(str(obj))
                digit_sequence = name_match.group()
                if len(digit_sequence) != len(hash_sequence):
                    cmds.warning(f"Sequence length mismatch for {obj}, skipping...")
                    continue
                count = int(digit_sequence.replace("0", ""))
                print(f"ATTRIBUTE MATCH: {attr_match.group()}, NAME MATCH: {name_match.group()}, COUNT: {count}")
                iter_attr = follower_attr.replace(hash_sequence, str(count).zfill(len(hash_sequence)))

            match action_type:
                case 1:
                    print(f'ACTION: ADD')
                    if confirm_override:
                        print(f'CONFIRMING OVERRIDE ENABLED: {obj}')
                        if not cmds.getAttr(f"{obj}.overrideEnabled"):
                            cmds.setAttr(f"{obj}.overrideEnabled", 1)
                            print(f'OVERRIDE FOR: {obj} \n---- SET TO: {cmds.getAttr(f"{obj}.overrideEnabled")}')
                    print(f'CHECKING CONNECTIONS: {obj}.{iter_attr}')
                    if not cmds.isConnected(f"{controller}.{controller_attr}", f"{obj}.{iter_attr}"):
                        cmds.connectAttr(f"{controller}.{controller_attr}", f"{obj}.{iter_attr}", force=True)
                        print(f'CONNECTED: {controller}.{controller_attr} TO {obj}.{iter_attr}')
                    else:
                        connections = '\n'.join(cmds.listConnections(f"{obj}.{iter_attr}"))
                        print(f'CONNECTION ALREADY EXISTS: {obj}.{iter_attr}\n'
                              f'CURRENT CONNECTIONS: \n{connections}')
                case 2:
                    print(f'ACTION: REMOVE')
                    if cmds.listConnections(f"{obj}.{iter_attr}"):
                        cmds.disconnectAttr(f"{controller}.{controller_attr}", f"{obj}.{iter_attr}")
                        print(f'DISCONNECTED: {controller}.{controller_attr} FROM {obj}.{iter_attr}')
            print()
        print("COMPLETED EXECUTION")

    cmds.button(l="Execute", p="button_col", c=on_execute, bgc=button_bgc)

    cmds.showWindow("ConnectionUtility")


if __name__ == "__main__":
    connection_utility()
