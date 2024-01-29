import maya.cmds as cmds
from core.components.joint_cmds import create_joints, orient_joints, rename_joints, display_axis
from ui.components.joint_ui_components import PositionListBlock, ParentBlock, NamingBlock
from ui.components.modular_blocks import WindowAdv, DescriptionFrame, LabeledTextField


class JointUI(WindowAdv):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

        # Variables
        self.name_block: NamingBlock
        self.parent_bool: bool
        self.parent_name: str
        self.radius: float
        self.loc_list: PositionListBlock
        self.settings_frame: str

    def _window_setup(self):
        super()._window_setup()

    def resize(self, cls, width, height):
        cls.resize(width, height)
        self.update_window_size()

    def _ui_setup(self):
        cmds.columnLayout(self.window_base, e=True, bgc=[.35, .5, .5])
        cmds.text(label="Joint Creation Tool", font="boldLabelFont", parent=self.window_base)

        block_kwargs = {"marginWidth": 1, "marginHeight": 1, "width": self.window_width, "create": True,
                        "color": [0.3, 0.3, 0.3],}
        tool_controls_kwargs = {"collapsable": False, "collapsed": False}

        desc = DescriptionFrame(
            self.window_base,
            collapsable=True,
            collapsed=True,
            height=25,
            **block_kwargs
        )
        desc.original_height = 40
        desc("This tool creates joints at the selected locations.")
        self.loc_list = PositionListBlock(
            self.window_base,
            "Creation_List",
            height=200,
            **block_kwargs,
            **tool_controls_kwargs,
        )
        self.radius_input = LabeledTextField(
            self.window_base,
            "Joint Radius",
            1,
            height=50,
            **block_kwargs,
            **tool_controls_kwargs,
        )
        self.name_block = NamingBlock(
            self.window_base,
            "name_choice",
            height=150,
            **block_kwargs,
            **tool_controls_kwargs,
        )
        self.parent_options = ParentBlock(
            self.window_base,
            "parent_opt_menu",
            height=75,
            **block_kwargs,
            **tool_controls_kwargs,
        )

        cmds.button(label="Execute", command=self.on_execute, backgroundColor=[1, 0, 0], parent=self.window_base)
        self.loc_list.clear()
        self.parent_options.update()
        super()._ui_setup()

    def on_execute(self, *_):
        rename = bool(self.name_block)
        name_schema = self.name_block.result(len(self.loc_list))
        parent_bool = bool(self.parent_options)
        parent_name = None if self.parent_options.get() == "None" else self.parent_options.get()
        radius = float(self.radius_input.get())

        if "fk ik rk" in name_schema.lower():
            self.name_block.check_count(len(self.loc_list) * 3)
            for type in ["FK", "IK", "RK"]:
                to_replace = ""
                for piece in name_schema.split("_"):
                    if piece.lower() == "fk ik rk":
                        to_replace = piece
                        break
                name = name_schema.replace(to_replace, type)

                created_joints = create_joints(self.loc_list, radius, parent_bool, parent_name)

                if parent_bool:
                    orient_joints(created_joints)
                display_axis(created_joints)

                if rename:
                    rename_joints(created_joints, name)
        else:
            created_joints = create_joints(self.loc_list, radius, parent_bool, parent_name)

            if parent_bool:
                orient_joints(created_joints)
            display_axis(created_joints)

            if rename:
                rename_joints(created_joints, name_schema)

        self.parent_options.update()


if __name__ == "__main__":
    print("RUNNNING FROM JOINT UI CORE DUNDER MAIN")
    JointUI("Joint Tool", width=500, height=550, create=True)
    # "test_win",
    # label = "Bold Test Frame",
    # font = "boldLabelFont",
    # width = 100,
    # height = 10,
    # border = True,
    # marginWidth = 5,
    # marginHeight = 5,
    # visible = True,
    # collapsable = True,
    # collapsed = True,
    # title_color = [0.6, 0.5, 0.6],
    # secondary_color = [0, 0.3, 0],
    # annotation = "This is a test frame.",
    # create = True)
