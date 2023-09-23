import maya.cmds as cmds

try:
    class IkManager:

        def __init__(self):
            self.operation_data = IkDataFactory().create_operation_data()

        def __repr__(self):
            return f"IkManager: {''.join([f'{k}, {v}' for k, v in self.operation_data.items()])}"

        def create_ik(self, ik_type):
            pass


    class IkDataFactory:
        def __init__(self):
            self.namer = lambda x: NameParser(x).prefix
            self.selected_joints = SelectionOperator().get("joint")
            self.relation_manager = RelationshipManager()

        def create_operation_data(self):
            joint_data = {}

            if not self.selected_joints:
                raise Exception("No joints selected. Please select at least 1 joints.")
            if len(self.selected_joints) < 3:
                try:
                    for joint in self.selected_joints:
                        parent, child = self.relation_manager.get_relations(joint, "joint", _parent=True,
                                                                            _children=False)
                        if parent:




                            """
                            #   THIS IS WHERE YOU WERE WHEN YOU GOT OFF.
                            # 
                            # 
                            # 
                            # 
                            """
                            # self.selected_joints.append(parent)
                        if child:
                            # self.selected_joints.append(child)
                        self.relation_manager.get_relations(self.selected_joints[0], "joint", _parent=False,
                                                            _children=True)
                except Exception as err:
                    print(err)
                    raise Exception("Please select at least 3 joints.")

            def set_joint_tuples():
                if self.selected_joints:
                    count = 0
                    joint_tuples = []
                    _joint_tuple = []
                    for joint in self.selected_joints:
                        if count != 3:
                            _joint_tuple.append(joint)
                            count += 1

                        # When _joint_tuple has 3 items
                        if len(_joint_tuple) == 3:
                            parent, child1, child2 = _joint_tuple

                            actual_parent1, _ = self.relation_manager.get_relations(child1, "joint", _parent=True,
                                                                                    _children=False) or (None, None)
                            actual_parent2, _ = self.relation_manager.get_relations(child2, "joint", _parent=True,
                                                                                    _children=False) or (None, None)

                            # Check if the first and second children are actually children of the 'parent'.
                            if actual_parent1 != parent or actual_parent2 != parent:
                                # Correct the hierarchy here
                                print(f"Warning: {child1} and {child2} are not children of {parent}. Correcting...")

                            _joint_tuple = tuple(_joint_tuple)
                            joint_tuples.append(_joint_tuple)
                            count = 0
                            _joint_tuple = []
                    return joint_tuples

            for joint_tuple in set_joint_tuples():
                prefix = self.namer(str(joint_tuple[0]))
                joint_data[prefix] = {
                    "Base": ["_Ctrl_Grp", "_Ctrl", joint_tuple[0]],
                    "PV": ["_Ctrl_Grp", "_Ctrl", "_Offset", joint_tuple[1]],
                    "Tip": ["_Ctrl_Grp", "_Ctrl", "_IK_Handle", joint_tuple[2]]
                }
            return self.parse_operation_data(joint_data)

        @staticmethod
        def parse_operation_data(broken_data):
            op_data = {}
            for key, value in broken_data.items():

                main_group = key + "_IK_Ctrl_Grp"
                prefix = key + "_IK"
                for k, v in value.items():
                    center = f"_{k}"
                    group = prefix + center + v[0]
                    control = prefix + center + v[1]
                    joint = v[-1]

                    op_data[main_group] = {"group": group,
                                           "control": control,
                                           "joint": joint}

                    if "_Offset" in v:
                        offset_group = prefix + center + v[2]
                        op_data[main_group]["offset_group"] = offset_group
                    if "_IK_Handle" in v:
                        ik_handle = key + v[2]
                        op_data[main_group]["ik_handle"] = ik_handle
            return op_data


    class SelectionOperator:
        @staticmethod
        def __get_selection(_type=None, long=False):
            return cmds.ls(sl=True, type=_type, long=long)

        def get(self, _type: object):
            return self.__get_selected_type(_type)

        def count(self, _type: object):
            return self.get_selected_type_count(_type)

        def __get_selected_type(self, _type):
            match _type:
                case "joint": return self.__get_selection("joint")
                case "control": return self.__get_selection("transform")
                case "mesh": return self.__get_selection("mesh")
                case "curve": return self.__get_selection("nurbsCurve")
                case "transform": return self.__get_selection("transform")
                case "all": return self.__get_selection()
                case "long": return self.__get_selection(long=True)
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


    class ControlCreator: pass


    class XformHandler: pass


    class Duplicator: pass


    class GroupCreator: pass


    class RelationshipManager:
        @staticmethod
        def check_IK_hierarchy(*args):
            def _get_parent(_object):
                return cmds.listRelatives(_object, parent=True)

            # def _get_child(_object):
            if len(args) % 3 == 0:

                parent, child1, child2 = args
                actual_parent1, _ = RelationshipManager.get_relations(child1, "joint", _parent=True, _children=False) or (None, None)
                actual_parent2, _ = RelationshipManager.get_relations(child2, "joint", _parent=True, _children=False) or (None, None)

                # Check if the first and second children are actually children of the 'parent'.
                if actual_parent1 != parent or actual_parent2 != parent:
                    # Correct the hierarchy here
                    print(f"Warning: {child1} and {child2} are not children of {parent}. Correcting...")

        @staticmethod
        def get_relations(_object, _type, _parent=False, _children=False, count=1):
            parent = cmds.listRelatives(_object, parent=True) if _parent else None
            if _children:
                children = cmds.listRelatives(_object, children=True, type=_type)[0:count] if count > 1 else\
                    cmds.listRelatives(_object, children=True, type=_type)
            else:
                children = None
            return {"parent": parent, "children": children}


    class NameParser:
        def __init__(self, item: str, splitter: str = "_"):
            self.item = item
            self.split_symbol = splitter
            self.prefix = self.__parse_string()

        def __parse_string(self):
            parts = self.item.split(self.split_symbol)
            prefix = f"{parts[0]}_{parts[1]}"
            return prefix


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

        def create_point_constraint(self):
            cmds.pointConstraint(self.leader, self.follower, name=self.name)

        def create_orient_constraint(self):
            cmds.orientConstraint(self.leader, self.follower, name=self.name)

        def create_parent_constraint(self):
            cmds.parentConstraint(self.leader, self.follower, name=self.name)

        def create_aim_constraint(self):
            cmds.aimConstraint(self.leader, self.follower, name=self.name)


    class IkCreator:
        def __init__(self, name: str, base_joint: object, tip_joint: object, ik_type: str):
            self.name = name
            self.base = base_joint
            self.tip = tip_joint
            self.ik_type = ik_type

        def create_ik(self):
            match self.ik_type:
                case "ik":
                    self.create_ik_handle()
                case "pole":
                    self.create_pole_vector()
                case "spring":
                    self.create_spring_ik()
                case "stretchy":
                    self.create_stretchy_ik()
                case "stretchy_spline":
                    self.create_stretchy_spline_ik()
                case _:
                    pass

        def create_ik_handle(self):
            cmds.ikHandle(startJoint=self.base, endEffector=self.tip)

        def create_pole_vector(self):
            pass

        def create_spring_ik(self):
            pass

        def create_stretchy_ik(self):
            pass

        def create_stretchy_spline_ik(self):
            pass

except Exception as e:
    print(f"IkManager {e} {e.__traceback__.tb_lineno}")
    raise e

if __name__ == "__main__":
    ik = IkManager()
    print(ik)
