import maya.cmds as cmds
from functools import partial
from core.components import selection_renamer, parent_cmds, center_locator
from core.maya_managers.selection_manager import Select as sl
from core.components.joint_cmds import orient as orientation
from core.components.joint_cmds import create as creation
from core.components.joint_cmds import display_axis


class UiList:
    def __init__(self, parent_ui: str, name: str, mode_opts: list, width=300):
        # Variables
        self.name = name
        self.list = []
        self.mode_opts = mode_opts
        self.mode = None
        self.window_width = width

        # Top level UI
        self.form = f"ui_form_{name}"
        self.frame = f"frame_{name}"
        self.parent_ui = parent_ui

        # Sub UIs
        self.add_opt_section = f"{self.name}_add_section"
        self.add_selection = f"{self.name}_add_mode"
        self.upper_button_grp = f"{self.name}_upper_buttons"
        self.list_visual = f"{self.name}_list_vis"
        self.lower_button_grp = f"{self.name}_lower_buttons"
        
        # Sub UI Components
        self.input_columns = f"{self.name}_columns"
        self.list_label = f"{self.name}"
        self.count = "(%i):" % len(self.list)
        self.list_name = f"{self.name}_list"

        self._create_ui()
    
    def __call__(self):
        return self.list
    
    def __iter__(self):
        return iter(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value
    
    def get(self):
        return self.list

    def insert(self, index, value):
        self.list.insert(index, value)
        
    def _create_ui(self):
        cmds.formLayout(self.form, bgc=[.5, .5, .5], p=self.parent_ui)
        cmds.frameLayout(self.frame, label=self.name, collapsable=True, collapse=False, parent=self.form)
        self._setup_main_ui()
        self._setup_ui_components()
        
    def _setup_main_ui(self):
        cmds.columnLayout(self.add_opt_section, adjustableColumn=True, parent=self.frame)
        cmds.rowColumnLayout(self.upper_button_grp, numberOfColumns=3,
                             columnWidth=[
                                 (1, self.window_width / 3), (2, self.window_width / 3), (3, self.window_width / 3)],
                             adjustableColumn=True, enable=True, parent=self.frame)
        cmds.columnLayout(self.list_visual, adjustableColumn=True, parent=self.frame)
        cmds.rowColumnLayout(self.lower_button_grp, numberOfColumns=2,
                             columnWidth=[(1, self.window_width / 2), (2, self.window_width / 2)], adjustableColumn=True,
                             enable=True, parent=self.frame)
        
    def _setup_ui_components(self):
        cmds.radioButtonGrp(self.add_selection, label="Create at the center of:", bgc=[.3, 0, .3],
                            labelArray2=self.mode_opts,
                            numberOfRadioButtons=2, select=1, parent=self.add_opt_section)
        cmds.button(label="Add", command=self._add_mode_query, backgroundColor=[0, 0, 0], parent=self.upper_button_grp)
        cmds.button(label="Remove", command=self._remove, backgroundColor=[0, 0, 0],
                    parent=self.upper_button_grp)
        cmds.button(label="Clear", command=self._clear, backgroundColor=[0, 0, 0],
                    parent=self.upper_button_grp)
        cmds.text(self.list_label, label=f"{self.list_label} {self.count}", align="center", parent=self.list_visual)
        cmds.textScrollList(self.list_name, numberOfRows=6, parent=self.list_visual)
        cmds.button(label="Move Up", command=self._move_up,
                    backgroundColor=[0, 0, 0], parent=self.lower_button_grp)
        cmds.button(label="Move Down", command=self._move_down,
                    backgroundColor=[0, 0, 0], parent=self.lower_button_grp)
        
    def _add_mode_query(self, *_):
        self.mode = cmds.radioButtonGrp(self.add_selection, query=True, select=True)
        if self.mode == 1:
            self._add_mode_any_or_all()
        elif self.mode == 2:
            self._add_mode_iter()

    def _add_mode_any_or_all(self, passed_objs=None, *_):
        passed_objs = passed_objs if passed_objs else cmds.ls(sl=True)
        center = center_locator.get_center(passed_objs)
        text = "({:.3f}, {:.3f}, {:.3f})".format(*center)
        self.list.append(center)
        self.count = "(%i):" % len(self.list)
        cmds.textScrollList(self.list_name, edit=True, append=f"{self.count} {text}")
        cmds.text(self.list_label, edit=True, label=f"{self.list_label} {self.count}")

    def _add_mode_iter(self, *_):
        selection = sl()
        for item in selection:
            self._add_mode_any_or_all(item)

    def _update_list_to_ui(self, *_):
        self.count = "(%i):" % len(self.list)
        cmds.text(self.list_label, edit=True, label=f"{self.list_label} {self.count}")
        cmds.textScrollList(self.list_name, edit=True, removeAll=True)
        for i, item in enumerate(self.list):
            text = "({:.3f}, {:.3f}, {:.3f})".format(*item)
            cmds.textScrollList(self.list_name, edit=True, append=f"{i + 1}: {text}")

    def _get_selected_index(self):
        selected_items = cmds.textScrollList(self.list_name, query=True, selectIndexedItem=True)
        if selected_items:
            return selected_items[0]
        else:
            return None

    def _move_up(self, *_):
        index = self._get_selected_index()
        if index > 1:
            self.list[index - 2], self.list[index - 1] = (self.list[index - 1], self.list[index - 2])
            self._update_list_to_ui()
            cmds.textScrollList(self.list_name, edit=True, selectIndexedItem=index - 1)

    def _move_down(self, *_):
        index = self._get_selected_index()
        if index is not None and index < len(self.list):
            # Adjusting index for zero-based list
            adjusted_index = index - 1
            print("Adjusted index:", adjusted_index)
            self.list[adjusted_index], self.list[adjusted_index + 1] = (
                self.list[adjusted_index + 1], self.list[adjusted_index])
            self._update_list_to_ui()
            cmds.textScrollList(self.list_name, edit=True, selectIndexedItem=index + 1)

    def _remove(self, *_):
        index = self._get_selected_index()
        if index:
            cmds.textScrollList(self.list_name, edit=True, removeIndexedItem=index)
            self.list.pop(index - 1)
            self._update_list_to_ui()

    def _clear(self, *_):
        self.list.clear()
        cmds.textScrollList(self.list_name, edit=True, removeAll=True)
        self._update_list_to_ui()
        

class ParentMenu:
    def __init__(self, parent_ui: str, name: str):
        # Variables
        self.name = name
        self.selected_option = None

        # Top level UI
        self.form = f"ui_form_{name}"
        self.frame = f"frame_{name}"
        self.parent_ui = parent_ui

        # Sub UIs
        self.top_section = f"{self.name}_top"
        self.bot_section = f"{self.name}_bot"

        # Sub UI Components
        self.input_columns = f"{self.name}_columns"
        self.toggle = f"{self.name}_bool"
        self.menu = f"{self.name}_menu"

        self._create_ui()
        
    def __bool__(self):
        return cmds.checkBox(self.toggle, query=True, value=True)
        
    def get(self):
        return cmds.optionMenu(self.menu, query=True, value=True)
    
    def _create_ui(self):
        cmds.formLayout(self.form, bgc=[.5, .5, .5], p=self.parent_ui)
        cmds.frameLayout(self.frame, label=self.name, collapsable=True, collapse=False, parent=self.form)
        self._setup_main_ui()
        self._setup_ui_components()
        
    def _setup_main_ui(self):
        cmds.columnLayout(self.top_section, adjustableColumn=True, p=self.frame)
        cmds.columnLayout(self.bot_section, adjustableColumn=True, p=self.frame)
        cmds.rowColumnLayout(self.input_columns, numberOfColumns=3,
                             columnWidth=[(1, 80), (2, 80), (3, 80)],
                             columnAlign=[1, "center"],
                             columnSpacing=(30, 0),
                             adjustableColumn=True, bgc=[.3, .3, .3],
                             enable=False, parent=self.bot_section)
    
    def _setup_ui_components(self):
        cmds.checkBox(self.toggle, label="Parent Objects on Creation", value=False,
                      changeCommand=partial(grey_field, self.toggle, self.input_columns),
                      parent=self.top_section)
        
        scene_joints = cmds.ls(type="joint")
        
        cmds.text(label="Parent To:", parent=self.input_columns, align="right")
        self.selected_option: None = cmds.optionMenu(self.menu, bgc=[.5, .5, .5], parent=self.input_columns)
        cmds.menuItem(label="None", parent=self.menu)
        for joint in scene_joints:
            cmds.menuItem(label=joint, parent=self.menu)
        cmds.button(label="Update", command=self._update_menu,
                    backgroundColor=[.2, 1, .2], parent=self.input_columns)

    def _update_menu(self, *_):
        cmds.optionMenu(self.menu, edit=True, deleteAllItems=True)
        cmds.menuItem(label="None", parent=self.menu)
        scene_joints = cmds.ls(type="joint")
        for joint in scene_joints:
            cmds.menuItem(label=joint, parent=self.menu)

    def update(self, *_):
        self._update_menu()


def grey_field(enabler, dependant, *_):
        def update_input_enable():
            return cmds.checkBox(enabler, query=True, value=True)

        cmds.rowColumnLayout(dependant, edit=True,
                             enable=update_input_enable(), noBackground=update_input_enable())


def _ui_setup(parent_ui: str, tool: str) -> str:

    def update_name_field(selection):
        if selection == "User Input":
            cmds.textField("name_input_field", edit=True, enable=True)
        else:
            cmds.textField("name_input_field", edit=True, enable=False)

    # _tab = cmds.formLayout(f"{tool}_base", bgc=[.3, .5, .55], p=parent_ui)
    #
    # # Add your UI elements to the formLayout
    # description_frame = cmds.frameLayout("description_frame", label="Description", collapse=True, collapsable=True,
    #                                      parent=_tab)
    # settings_frame = cmds.frameLayout("settings_frame", label="Tool Settings", collapsable=True, parent=_tab)
    #
    # # Position the frames within the formLayout
    # cmds.formLayout(_tab, edit=True,
    #                 attachForm=[(description_frame, "top", 5), (description_frame, "left", 5),
    #                             (description_frame, "right", 5),
    #                             (settings_frame, "left", 5), (settings_frame, "right", 5)],
    #                 attachControl=(settings_frame, "top", 5, description_frame))

    _tab = cmds.columnLayout(f"{tool}_base", adj=True, bgc=[.3, .5, .55], p=parent_ui)

    cmds.frameLayout("description_frame", label="Description", collapsable=True,
                     collapse=True, parent=f"{tool}_base")
    cmds.text("This tool allows you to Create, Name, parent Joints", parent="description_frame",
              font="smallPlainLabelFont", backgroundColor=[0, 0, 0])
    cmds.frameLayout("settings_frame", label="Tool Settings", collapsable=True, parent=f"{tool}_base")
    cmds.columnLayout("ui_base", adjustableColumn=True, parent="settings_frame")
    cmds.columnLayout("pos_list_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("radius_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("naming_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("parent_block", adjustableColumn=True, p="ui_base")
    cmds.columnLayout("execute_block", adjustableColumn=True, parent="ui_base")
    cmds.columnLayout("naming_block_group", adjustableColumn=True, p="naming_block")
    cmds.columnLayout("naming_block_upper", adjustableColumn=True, p="naming_block")
    cmds.columnLayout("naming_block_lower", adjustableColumn=True, p="naming_block")
    cmds.rowColumnLayout("name_input_section", numberOfColumns=2, columnAttach=(1, "both", 20),
                         columnWidth=[(1, 125), (2, 175)], adjustableColumn=True, bgc=[0, 0, 0],
                         enable=False, parent="naming_block_lower")
    parent_ui = ParentMenu("parent_block", "parent_ui")
    loc_list = UiList("pos_list_block", "Creation_List", ["All Selected", "Each Selected"])
    cmds.text(l="Joint Radius:", bgc=[.7, .7, .7], p="radius_block")
    radius_input = cmds.textField("joint_radius", tx="1", bgc=[.1, .1, .1], p="radius_block")

    rename_bool = cmds.checkBox("name_bool", label="Name Joints", value=False,
                                changeCommand=partial(grey_field, "name_bool", "name_input_section"),
                                parent="naming_block_upper")
    cmds.text(label="Naming Scheme Input", parent="name_input_section")
    name_input = cmds.textField("name_input_field", parent="name_input_section", bgc=[.1, .1, .1])
    cmds.text(label="Naming Presets:", parent="name_input_section")
    naming_option = cmds.optionMenu("NamingOpMenu", changeCommand=update_name_field,
                                    backgroundColor=[.5, .5, .5], parent="name_input_section")
    cmds.menuItem(label="User Input", parent="NamingOpMenu")
    sequential_schemas = ["Spine", "Arm", "L_Arm", "R-Arm", "L_Clav", "R_Clav", "Finger_##",
                          "L_Finger_##", "R_Finger_##", "Leg", "L_Leg", "R_Leg", "L_FT_Leg",
                          "R_FT_Leg", "L_BK_Leg", "R_BK_Leg", "L_Toe", "R_Toe", "Head", "Neck", "Tail", "L_Tail",
                          "R_Tail", "Eye", "L_Eye", "R_Eye"]
    single_schemas = ["ROOT_JNT", "COG_Jnt", "Hip_Jnt"]
    for name in sequential_schemas:
        cmds.menuItem(label=f"{name}_##_Jnt", parent="NamingOpMenu")
    for name in single_schemas:
        cmds.menuItem(label=f"{name}", parent="NamingOpMenu")

    def on_execute(*_):
        # add a checkbox for clearing list on execute
        rename = cmds.checkBox(rename_bool, query=True, value=True)
        naming_input = cmds.textField(name_input, query=True, text=True)
        name_choice = cmds.optionMenu(naming_option, query=True, value=True)
        parent_bool = bool(parent_ui)
        parent_name = parent_ui.get()
        radius = float(cmds.textField(radius_input, query=True, text=True))

        if parent_name != "None" and parent_name is not None:
            loc_list.insert(0, parent_name)
        created_joints = creation(loc_list, radius, parent_bool)
        if parent_bool:
            orientation(created_joints)
        display_axis(created_joints)

        if rename:
            if name_choice == "User Input":
                name_schema = naming_input
            else:
                name_schema = name_choice
            if name_schema[0].isdigit() or name_schema.startswith("_"):
                cmds.error("Naming Schema starts with an invalid character.")
                cmds.delete(cmds.ls(sl=True))
            selection_renamer.perform_rename(name_schema, created_joints)

        parent_ui.update()

    cmds.button(label="Execute", command=on_execute, backgroundColor=[1, 0, 0], parent="execute_block")
    loc_list._clear()
    parent_ui.update()
    return _tab


def create_ui_window(manual_run=False):
    joint_ui_window = "joint_ui_window"
    if cmds.window(joint_ui_window, ex=True):
        cmds.deleteUI(joint_ui_window)
    cmds.window(joint_ui_window, t="Joint Tools", wh=(100, 50), mxb=False, mnb=True, rtf=True, nde=True)
    tabs_ui = cmds.tabLayout("tabs_ui", innerMarginWidth=5, innerMarginHeight=5)

    joint_tab = _ui_setup(tabs_ui, "joint")
    cmds.tabLayout(tabs_ui, e=True, tl=(joint_tab, "Joint Creator"))

    cmds.showWindow(joint_ui_window)


def main():
    create_ui_window(True)


if __name__ == "__main__":
    main()
