import maya.cmds as cmds
print("IkManager.py")

try:
    class IkManager:
        print("IkManager")

        def __init__(self):
            print("IkManager")
            print(SelectionOperator().get("joint"))

            self.selected_joints = SelectionOperator().get("joint")
            print(self.selected_joints)
            self.namer = lambda x: NameParser(x)
            print(self.namer)
            self.operation_data = self.create_work_dict()
            print(self.operation_data)

        def create_ik(self, ik_type):
            pass

        def create_work_dict(self):
            print("Creating work dict")
            joint_data = {}
            for joint_tuple in self.selected_joints:
                prefix = self.namer(joint_tuple[0])
                joint_data[prefix] = {
                    "Base": ["_Ctrl_Grp", "_Ctrl", joint_tuple[0]],
                    "PV": ["_Ctrl_Grp", "_Offset", "_Ctrl", joint_tuple[1]],
                    "Tip": ["_Ctrl_Grp", "_Ctrl", "_IK_Handle", joint_tuple[2]]
                }
            return joint_data


    class SelectionOperator:
        @staticmethod
        def __get_selection(_type=None): return cmds.ls(sl=True, type=_type)

        def get(self, _type: object): return self.__get_selected_type(_type)

        def count(self, _type: object): return self.get_selected_type_count(_type)

        def __get_selected_type(self, _type):
            print(f"Getting selected type: {_type}")
            match _type:
                case "joint": return self.__get_selection("joint")
                case "control": return self.__get_selection("transform")
                case "mesh": return self.__get_selection("mesh")
                case "curve": return self.__get_selection("nurbsCurve")
                case "transform": return self.__get_selection("transform")
                case "all": return self.__get_selection()
                case _: return None

        def get_selected_type_count(self, _type):
            match _type:
                case "joint": return len(self.__get_selection("joint"))
                case "control": return len(self.__get_selection("transform"))
                case "mesh": return len(self.__get_selection("mesh"))
                case "curve": return len(self.__get_selection("nurbsCurve"))
                case "transform": return len(self.__get_selection("transform"))
                case "all": return len(self.__get_selection())
                case _: return None


    class ControlCreator:
        pass


    class XformHandler:
        pass


    class Duplicator:
        pass


    class GroupCreator:
        pass


    class RelationshipManager:
        def __init__(self):
            pass

        @staticmethod
        def get_relations(_object, _type):
            parent = cmds.listRelatives(_object, parent=True)
            children = cmds.listRelatives(_object, children=True, type=_type)
            return parent, children


    class NameParser:
        def __init__(self, item: str, splitter: str = "_"):
            self.item = item
            self.split_symbol = splitter
            self.prefix = self.__parse_string()

        def __parse_string(self):
            parts = self.item.split(self.split_symbol)
            prefix = f"{parts[0]}_{parts[1]}"
            return prefix

    """
    class Constrainer:
        def __init__(self, name: str, leader: object, follower: object, constraint_type: str):
            self.name = name
            self.leader = leader
            self.follower = follower
            self.constraint_type = constraint_type

        def create_constraint(self):
            match self.constraint_type:
                case "point": self.create_point_constraint()
                case "orient": self.create_orient_constraint()
                case "parent": self.create_parent_constraint()
                case "aim": self.create_aim_constraint()
                case _: pass

        def create_point_constraint(self): cmds.pointConstraint(self.leader, self.follower, name=self.name)

        def create_orient_constraint(self): cmds.orientConstraint(self.leader, self.follower, name=self.name)

        def create_parent_constraint(self): cmds.parentConstraint(self.leader, self.follower, name=self.name)

        def create_aim_constraint(self): cmds.aimConstraint(self.leader, self.follower, name=self.name)
    """
    """
    class IkCreator:
        def __init__(self, name: str, base_joint: object, tip_joint: object, ik_type: str):
            self.name = name
            self.base = base_joint
            self.tip = tip_joint
            self.ik_type = ik_type

        def create_ik(self):
            match self.ik_type:
                case "ik": self.create_ik_handle()
                case "pole": self.create_pole_vector()
                case "spring": self.create_spring_ik()
                case "stretchy": self.create_stretchy_ik()
                case "stretchy_spline": self.create_stretchy_spline_ik()
                case _: pass

        def create_ik_handle(self):
            cmds.ikHandle(startJoint=self.base, endEffector=self.tip)

        def create_pole_vector(self): pass

        def create_spring_ik(self): pass

        def create_stretchy_ik(self): pass

        def create_stretchy_spline_ik(self): pass
    """
except Exception as e:
    print(e)
    print("IkManager")
    raise e
