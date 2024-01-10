import maya.cmds as cmds
from ui.components.modular_blocks.basic_mod.form_base import BaseUI


class MainUI(BaseUI):
    def __init__(self, parent_ui: str, name: str, width: int, mode_callbacks: dict, text_format: str = "{}",
                 **kwargs):
        super_args = [parent_ui, name, width]
        super().__init__(*super_args)

        self.list = []
        self.mode_callbacks = mode_callbacks
        self.text_format = text_format

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

        if kwargs.get("create", kwargs.get("cr", kwargs.get("c", False))):
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

    def pop(self, index=-1):
        return self.list.pop(index)

    def _setup_main_ui(self):
        top_b_width = int(self.window_width / 3)
        bot_b_width = int(self.window_width / 2)

        cmds.columnLayout(self.add_opt_section, adjustableColumn=True, parent=self.frame)
        cmds.rowColumnLayout(self.upper_button_grp, numberOfColumns=3,
                             columnWidth=[
                                 (1, top_b_width), (2, top_b_width), (3, top_b_width)],
                             adjustableColumn=True, enable=True, parent=self.frame)
        cmds.columnLayout(self.list_visual, adjustableColumn=True, parent=self.frame)
        cmds.rowColumnLayout(self.lower_button_grp, numberOfColumns=2,
                             columnWidth=[(1, bot_b_width), (2, bot_b_width)],
                             adjustableColumn=True, enable=True, parent=self.frame)

    def _setup_ui_components(self):
        self.add_selection = cmds.radioButtonGrp(label="Create at the center of:", bgc=[.3, 0, .3],
                                                 numberOfRadioButtons=len(self.mode_callbacks),
                                                 labelArray2=list(self.mode_callbacks.keys()),
                                                 select=1, parent=self.add_opt_section)
        cmds.button(label="Add", command=self._add_mode_query, backgroundColor=[0, 0, 0], parent=self.upper_button_grp)
        cmds.button(label="Remove", command=self._remove, backgroundColor=[0, 0, 0],
                    parent=self.upper_button_grp)
        cmds.button(label="Clear", command=self.clear, backgroundColor=[0, 0, 0],
                    parent=self.upper_button_grp)
        cmds.text(self.list_label, label=f"{self.readable_name} {self.count}", align="center", parent=self.list_visual)
        cmds.textScrollList(self.list_name, numberOfRows=6, parent=self.list_visual)
        cmds.button(label="Move Up", command=self._move_up,
                    backgroundColor=[0, 0, 0], parent=self.lower_button_grp)
        cmds.button(label="Move Down", command=self._move_down,
                    backgroundColor=[0, 0, 0], parent=self.lower_button_grp)

    def _add_mode_query(self, *_):
        # Determine the selected mode using the index and execute the corresponding callback function
        selected_index = cmds.radioButtonGrp(self.add_selection, query=True, select=True)
        mode_name = list(self.mode_callbacks)[selected_index - 1]  # Adjust for 1-based index
        callback_func = self.mode_callbacks[mode_name]
        callback_func()  # Execute the callback function

    def _update_list_to_ui(self, *_):
        self.count = "(%i):" % len(self.list)
        cmds.text(self.list_label, edit=True, label=f"{self.readable_name} {self.count}")
        cmds.textScrollList(self.list_name, edit=True, removeAll=True)
        for i, item in enumerate(self.list):
            list_text = self.text_format.format(*item)
            cmds.textScrollList(self.list_name, edit=True, append=f"{i + 1}: {list_text}")

    def _get_selected_index(self):
        selected_items = cmds.textScrollList(self.list_name, query=True, selectIndexedItem=True)
        if selected_items:
            return selected_items[0]
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

    def clear(self, *_):
        self.list.clear()
        cmds.textScrollList(self.list_name, edit=True, removeAll=True)
        self._update_list_to_ui()


if __name__ == "__main__":
    # Example usage:
    def mode1_callback():
        print("Mode 1 selected")

    def mode2_callback():
        print("Mode 2 selected")

    mode_callbacks = {
        "Mode 1": mode1_callback,
        "Mode 2": mode2_callback
    }
    if cmds.window("main_window", exists=True):
        cmds.deleteUI("main_window")
    cmds.window("main_window")
    cmds.showWindow("main_window")

    ui_instance = MainUI("main_window", "test_ui", 300, mode_callbacks)
    print("DUNDER COMPLETED")
