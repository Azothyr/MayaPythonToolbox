import maya.cmds as cmds
from ui.components.utils.enable_handler import toggle_layouts


def get_directional_attrs(obj, rotation_plane=None, translate_axis=None, all=True):
    rotation_plane = rotation_plane.lower() if rotation_plane else "xyz"
    translate_axis = translate_axis.lower() if translate_axis else "x"

    if all:
        rotation_plane = "xyz"
        translate_axis = "xyz"
        for attr in rotation_plane:
            yield f"{obj}.r{attr}"
        for attr in translate_axis:
            yield f"{obj}.t{attr}"
    else:
        for attr in rotation_plane:
            yield f"{obj}.r{attr}"
        yield f"{obj}.t{translate_axis}"


def set_keyframes(obj, primary_attr, translation_dir="x"):
    for attr in [f"{obj}.r{axis}" for axis in "xyz"] + [f"{obj}.t{translation_dir}"]:
        if attr != primary_attr:
            original_value = cmds.getAttr(attr)
            cmds.setAttr(attr, original_value)
        cmds.setKeyframe(attr)


def set_keyframes_for_weight_painting(
        obj, rotation_amount: tuple = (45, 45, 45), translation_amount: float = 25, translation_dir: str = "x",
        interval: int = 15):
    sub_interval = interval
    if interval < 4:
        interval = 4
    if interval % 3 == 0:
        sub_interval += 1
    interval *= 3
    interval += 1

    time = 0
    cmds.currentTime(time)
    set_keyframes(obj, None, translation_dir)
    time += interval
    for attr in [f"{obj}.r{axis}" for axis in "xyz"] + [f"{obj}.t{translation_dir}"]:
        count = 0
        original_value = cmds.getAttr(attr)
        if attr.split(".")[1].startswith("r"):
            axis = attr.split(".")[1][1]
            idx = "xyz".index(axis)
            cmds.currentTime(time)
            set_keyframes(obj, axis, translation_dir)
            cmds.currentTime(time - sub_interval * 2)
            cmds.setAttr(attr, rotation_amount[idx])
            set_keyframes(obj, axis, translation_dir)
            cmds.currentTime(time - sub_interval)
            cmds.setAttr(attr, -rotation_amount[idx])
            set_keyframes(obj, axis, translation_dir)
            cmds.currentTime(time)
            cmds.setAttr(attr, original_value)
            set_keyframes(obj, axis, translation_dir)
            if idx == 2:
                time += sub_interval
            else:
                time += interval
            count += 1
        elif attr.split(".")[1].startswith("t"):
            cmds.currentTime(time - sub_interval)
            set_keyframes(obj, attr, translation_dir)
            cmds.currentTime(time)
            cmds.setAttr(attr, translation_amount + original_value)
            set_keyframes(obj, attr, translation_dir)
    time = 0
    cmds.currentTime(time)


def remove_keyframes(obj, interval):
    cmds.currentTime(0)
    end_time = interval * 100 + 1
    for attr in get_directional_attrs(obj, all=True):
        keyframes = cmds.keyframe(attr, q=True, time=(-10, end_time))
        if keyframes:
            cmds.cutKey(attr, time=(keyframes[0], keyframes[-1]))


def ui():
    def execute(*_):
        selection = cmds.ls(sl=True)
        if not selection:
            cmds.warning("No object selected.")
            return

        mode = cmds.radioButtonGrp("options", q=True, select=True)
        interval = cmds.intFieldGrp("interval", q=True, value1=True)
        translation_dir = cmds.radioButtonGrp("trans_dir", q=True, select=True)
        translation_amount = cmds.floatFieldGrp("translation_amount", q=True, value=True)[0]
        rotation_amount = cmds.floatFieldGrp("rotation_amount", q=True, value=True)

        for obj in selection:
            if mode == 1:
                set_keyframes_for_weight_painting(
                    obj,
                    interval=interval,
                    translation_dir="xyz"[translation_dir - 1],
                    rotation_amount=(rotation_amount[0], rotation_amount[1], rotation_amount[2]),
                    translation_amount=translation_amount
                )
            elif mode == 2:
                remove_keyframes(
                    obj,
                    interval
                )

    if cmds.window("wpu_win", exists=True):
        cmds.deleteUI("wpu_win", window=True)
    window = cmds.window("wpu_win", title="weight Painting utility Tool", wh=(200, 100),
                         resizeToFitChildren=True, sizeable=False)
    cmds.rowColumnLayout("main_column", adj=True, p=window)
    option_column = cmds.rowColumnLayout(
        "option_col", adj=True, numberOfColumns=2, columnWidth=[[1, 150], [2, 200]],
        columnSpacing=[[1, 1], [2, 1]], columnAlign=[[1, "center"], [2, "center"]],
        bgc=[0.2, 0.2, 0.3], p="main_column")
    text_spacer_col = cmds.columnLayout("text_spacer_col", adj=True, p="main_column")
    set_column = cmds.columnLayout("set_col", adj=1, p="main_column", bgc=(0.2, 0.2, 0.3))
    button_column = cmds.columnLayout("rem_col", adj=True, manage=True, p="main_column")
    mode_selection = cmds.radioButtonGrp(
        "options",
        numberOfRadioButtons=2,
        label="Mode:  ",
        labelArray2=["Set", "Remove"],
        columnWidth3=[50, 50, 50],
        select=1,
        p=option_column,
        changeCommand=lambda *_: toggle_layouts(
            {set_column: cmds.radioButtonGrp(mode_selection, q=True, select=True) == 1}
        )
    )
    cmds.intFieldGrp(
        "interval",
        label="Interval: ",
        numberOfFields=1,
        value1=15,
        columnWidth2=[60, 60],
        columnAlign2=["left", "left"],
        annotation="Interval",
        p=option_column
    )
    cmds.text(label="Select an object to run the tool on.", bgc=(0, 0, 0), p=text_spacer_col)
    cmds.radioButtonGrp(
        "trans_dir",
        label="Translation Direction",
        numberOfRadioButtons=3,
        labelArray3=["X", "Y", "Z"],
        columnWidth4=[140, 35, 35, 35],
        select=1,
        p=set_column
    )
    set_2_col = cmds.rowColumnLayout("set_2_col", numberOfColumns=2, p=set_column,
                                     columnWidth=[(1, 250), (2, 250)]
                                     )
    cmds.floatFieldGrp(
        "translation_amount",
        numberOfFields=1,
        label="Translation Amount: ",
        value1=15.0,
        step=1.0,
        precision=1.0,
        annotation="Translation Amount",
        p=set_2_col
    )
    cmds.floatFieldGrp(
        "rotation_amount",
        numberOfFields=3,
        label="Rotation Amount: ",
        value1=30.0,
        value2=30.0,
        value3=30.0,
        precision=0.01,
        annotation="Rotation Amount",
        p=set_column
    )

    cmds.button(
        label="Execute",
        command=execute,
        p=button_column,
        bgc=(0.2, 0.3, 0.2)
    )

    cmds.showWindow(window)


if __name__ == "__main__":
    ui()
