import maya.cmds as cmds
from functools import partial
from ui.components.utils.query_ui_value import query
from ui.components.utils.enable_handler import toggle_state
from ui.components.utils.enable_handler import toggle_layouts
from ui.components.modular_blocks import FormBase


class MainUI(FormBase):
    def __init__(self, parent_ui: str, name: str, width=300, **kwargs):
        super_args = [parent_ui, name, width]
        # SUPER: self.name, self.readable_name, self.window_width, self.form, self.frame, self.parent_ui
        super().__init__(*super_args)

        # Static Options
        self.input_collection = [
            "preset",
            "single field",
            "user assisted",
        ]
        self.text_look_options = [
            "capitalize",
            "lowercase",
            "uppercase"
        ]
        self.side_options = [
            "l",
            "r",
        ]
        self.prefix_options = [
            "root",
            "cog",
            "head",
            "neck",
            "eye",
            "spine",
            "clav",
            "arm",
            "pelvis",
            "leg",
            "front leg",
            "back leg",
            "tail",
            "finger",
            "finger ##",
            "toe",
            "toe ##",
        ]
        self.singles = [
            "root",
            "cog",
        ]
        self.type_options = [
            "FK",
            "IK",
            "RK",
            "FK, IK, RK",
            "helper",
            "twist",
            "corrective",
        ]
        self.suffix_options = [
            "jnt",
        ]

        # Variables
        self.single_bool = False
        self.active_layout = None
        self._look = None
        self._schema = None
        self._side = None
        self._prefix = None
        self._suffix = None
        self._joint_type = None

        # Sub UIs
        self.enable_section = f"{self.name}_enable"
        self.top_section = f"{self.name}_top"
        self.mid_section = f"{self.name}_mid"
        self.bot_section = f"{self.name}_bot"

        # Sub UI Components
        self.single_input_columns = f"{self.name}_single_input_columns"
        self.assisted_input_columns = f"{self.name}_assisted_input_columns"
        self.preset_columns = f"{self.name}_preset_columns"
        self.output_row = f"{self.name}_output_row"

        self.toggle = f"{self.name}_bool"
        self.collection_type_grp = f"{self.name}_c_type_menu"
        self.look_menu_grp = f"{self.name}_l_type_menu"
        self.side_menu = f"{self.name}_side_menu"
        self.prefix_menu = f"{self.name}_pre_menu"
        self.joint_type_menu = f"{self.name}_j_type_menu"
        self.suffix_menu = f"{self.name}_suf_menu"
        self.example_text = f"{self.name}_example_text"

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
            self._create_ui()

    def __str__(self):
        return self._schema

    def __bool__(self):
        return query(self.toggle, "checkbox")

    def _get_collection_type(self):
        return query(self.collection_type_grp, "radioButtonGrp")

    def _get_look_type(self):
        return query(self.look_menu_grp, "radioButtonGrp")

    def _set_look_type(self, *_):
        self._look = self._get_look_type()

    @staticmethod
    def _get_value(item, type, *_):
        return query(item, type)

    def _set_side(self, *_):
        item = self.side_menu
        type = "menu"
        self._side = self._get_value(item, type)
        if self._side != "_":
            self._side = self._apply_look(self._side)
            self._side = f"{self._side}"
        else:
            self._side = ""

    def _set_prefix(self, *_):
        item = self.prefix_menu
        type = "menu"
        self._prefix = self._get_value(item, type)
        if self._prefix != "_":
            self._prefix = self._apply_look(self._prefix)
            start = "." if self._side and "." not in self._side else ""
            self._prefix = f"{start}{self._prefix}"
        else:
            self._prefix = ""

    def _set_type(self, *_):
        item = self.joint_type_menu
        type = "menu"
        self._joint_type = self._get_value(item, type)
        if self._joint_type != "_":
            self._joint_type = self._apply_look(self._joint_type)
            start = "." if self._prefix else "." if self._side and "." not in self._side else ""
            self._joint_type = f"{start}{self._joint_type}"
        else:
            self._joint_type = ""

    def _set_suffix(self, *_):
        item = self.suffix_menu
        type = "menu"
        self._suffix = self._get_value(item, type)
        if self._suffix != "_":
            self._suffix = self._apply_look(self._suffix)
            start = "." if self._joint_type else "." if self._side and "." not in self._side else ""
            self._suffix = f"{start}{self._suffix}"
            if self.single_bool is False:
                start = ".##." if self._suffix and "." not in self._suffix else ".##"
                self._suffix = f"{start}{self._suffix}" if self._suffix != "" else "##"
            if not self._side and not self._prefix and not self._joint_type and self._suffix:
                self._suffix = self._apply_look("joint_##")
        else:
            self._suffix = ""

    def _apply_look(self, text, *_):
        text = text.replace(".", " ")
        match self._look:
            case 1:
                if text.lower() in ["fk", "ik", "rk"]:
                    return text.upper()
                return text.capitalize()
            case 2:
                return text.lower()
            case 3:
                return text.upper()

        if self._look == 1:
            self._side = self._side.capitalize()
            self._prefix = self._prefix.capitalize()

    def _get_schema(self):
        self._update_variables()

        self._schema = f"{self._side}{self._prefix}{self._joint_type}{self._suffix}".replace('.', '_')

    def _update_variables(self, *_):
        self._set_look_type()
        self._set_side()
        self._set_prefix()
        self._set_type()
        self._set_suffix()

    def _reset_variables(self, *_):
        self.prefix_menu = cmds.optionMenu(self.prefix_menu, edit=True, select=1)
        self.joint_type_menu = cmds.optionMenu(self.joint_type_menu, edit=True, select=1)
        self.suffix_menu = cmds.optionMenu(self.suffix_menu, edit=True, select=1)
        self.side_menu = cmds.optionMenu(self.side_menu, edit=True, select=1)
        self._update_example_text()

    def _update_example_text(self, *_):
        self._get_schema()
        cmds.text(self.example_text, edit=True, label=f"Example Output:\t\t\t{self._schema}")

    def _toggle_block(self, *_):
        self._reset_variables()
        partial(toggle_state, self.toggle, self.top_section)()
        partial(toggle_state, self.toggle, self.mid_section)()
        partial(toggle_state, self.toggle, self.bot_section)()

    def _setup_main_ui(self):
        self.enable_section = cmds.columnLayout(self.enable_section, adjustableColumn=True, p=self.frame)
        self.top_section = cmds.columnLayout(self.top_section, adjustableColumn=True, p=self.frame, enable=False)
        self.mid_section = cmds.columnLayout(self.mid_section, adjustableColumn=True, p=self.frame, enable=False)
        self.bot_section = cmds.columnLayout(self.bot_section, adjustableColumn=True, p=self.frame, enable=False)
        self.single_input_columns = cmds.rowColumnLayout(self.single_input_columns, numberOfColumns=3,
                                                         columnWidth=[(1, 80), (2, 80), (3, 80)],
                                                         columnAlign=[1, "center"],
                                                         columnSpacing=(30, 0),
                                                         adjustableColumn=True, bgc=[.3, .3, .3],
                                                         parent=self.mid_section)

        self.assisted_input_columns = cmds.rowColumnLayout(self.assisted_input_columns, numberOfColumns=3,
                                                           columnWidth=[(1, 80), (2, 80), (3, 80)],
                                                           columnAlign=[1, "center"],
                                                           columnSpacing=(30, 0),
                                                           adjustableColumn=True, bgc=[.3, .3, .3],
                                                           parent=self.mid_section)

        self.preset_columns = cmds.rowColumnLayout(self.preset_columns, numberOfColumns=8,
                                                   columnWidth=[(1, 40), (2, 80), (3, 40), (4, 80),
                                                                (5, 40), (6, 80), (7, 40), (8, 80)],
                                                   columnSpacing=[(1, 0), (2, 0), (3, 0), (4, 0),
                                                                  (5, 0), (6, 0), (7, 0), (8, 0)],
                                                   # rowSpacing=[(1, 50), (2, 50)],
                                                   bgc=[.3, .3, .3],
                                                   parent=self.mid_section)

        self.output_row = cmds.rowColumnLayout(self.output_row, numberOfColumns=1,
                                               columnWidth=[(1, 500)],
                                               columnAlign=[1, "center"],
                                               columnSpacing=[(1, 20)],
                                               bgc=[.3, .3, .3],
                                               parent=self.bot_section)

    def _setup_ui_components(self):
        cmds.checkBox(self.toggle, label="Name Joints?", value=False,
                      bgc=[.4, .4, .4],
                      changeCommand=self._toggle_block,
                      parent=self.enable_section)
        self._create_radio_ui(self.top_section)
        self._create_preset_ui(self.preset_columns)
        self._create_single_input_ui(self.single_input_columns)
        self._create_input_fields_ui(self.assisted_input_columns)
        self.example_text = cmds.text(self.example_text, label="Example Output:", align="left", parent=self.output_row)

    def _create_radio_ui(self, parent):
        self.collection_type_grp = cmds.radioButtonGrp(self.collection_type_grp, label="Layouts: ",
                                                       bgc=[.3, .3, .3],
                                                       numberOfRadioButtons=len(self.input_collection),
                                                       labelArray3=[idx.title() for idx in self.input_collection],
                                                       select=1, parent=parent,
                                                       onCommand=self._update_layout)

        self.look_menu_grp = cmds.radioButtonGrp(self.look_menu_grp, label="Text Look: ",
                                                 bgc=[.4, .4, .4],
                                                 numberOfRadioButtons=len(self.text_look_options),
                                                 labelArray3=[idx.title() for idx in self.text_look_options],
                                                 select=1, parent=parent,
                                                 onCommand=self._update_example_text)

    def _create_single_input_ui(self, parent):
        pass

    def _create_input_fields_ui(self, parent):
        pass

    @staticmethod
    def _create_text_fields(name: str, parent_section: str) -> object:
        return cmds.textField(name, backgroundColor=[.1, .1, .1], parent=parent_section)

    def _create_preset_ui(self, parent):
        self.side_menu = self._create_option_menu(self.side_menu, "Side:", self.side_options,
                                                  self._update_example_text, parent)
        self.prefix_menu = self._create_option_menu(self.prefix_menu, "Prefix:", self.prefix_options,
                                                    self._update_example_text, parent)
        self.joint_type_menu = self._create_option_menu(self.joint_type_menu, "Type:", self.type_options,
                                                        self._update_example_text, parent)
        self.suffix_menu = self._create_option_menu(self.suffix_menu, "Suffix:", self.suffix_options,
                                                    self._update_example_text, parent)

    @staticmethod
    def _create_option_menu(name: str, label: str, option_list: list[str], callback: object,
                            parent_section: str) -> object:
        option_list.insert(0, "_")
        cmds.text(label=label, backgroundColor=[0, 0, 0], parent=parent_section)
        result = cmds.optionMenu(name, backgroundColor=[.1, .2, .4], parent=parent_section,
                                 changeCommand=callback)
        for item in option_list:
            cmds.menuItem(label=item, parent=name)
        return result

    def _update_layout(self, *_):
        layouts = {
            1: self.preset_columns,
            2: self.single_input_columns,
            3: self.assisted_input_columns,
        }
        current = self._get_collection_type()
        conditions = {layout: (label == current) for label, layout in layouts.items()}
        self.active_layout = toggle_layouts(conditions)

    def result(self, passed_objs: list[str], *_):
        self._get_schema()
        if self._schema[0].isdigit() or self._schema.startswith("_"):
            cmds.error("Naming Schema starts with an invalid character.")
            cmds.delete(passed_objs)
            return
        return self._schema


if __name__ == "__main__":
    if cmds.window("test_win", exists=True):
        cmds.deleteUI("test_win")
    win = cmds.window("test_win")
    cmds.showWindow(win)
    test = MainUI(win, "test_win", create=True)
