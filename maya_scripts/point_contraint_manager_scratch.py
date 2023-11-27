import maya.cmds as cmds


class UtilityNodeManager:
    @staticmethod
    def create_utility_node(node_type, name, **kwargs):
        if not cmds.objExists(name):
            return cmds.shadingNode(node_type, name=name, asUtility=True, **kwargs)
        return name

    @staticmethod
    def set_node_attribute(node, attr, value):
        if cmds.attributeQuery(attr, node=node, exists=True):
            cmds.setAttr(f"{node}.{attr}", value)

    @staticmethod
    def connect_to_utility_node(source, utility_node, utility_input, utility_output, destination):
        cmds.connectAttr(source, f"{utility_node}.{utility_input}", f=True)
        cmds.connectAttr(f"{utility_node}.{utility_output}", destination, f=True)

    @staticmethod
    def create_and_configure_node(node_type, name, initial_attrs=None):
        node = UtilityNodeManager.create_utility_node(node_type, name)
        if initial_attrs and isinstance(initial_attrs, dict):
            for attr, value in initial_attrs.items():
                UtilityNodeManager.set_node_attribute(node, attr, value)
        return node

    @staticmethod
    def disconnect_attribute(source, destination):
        if cmds.isConnected(source, destination):
            cmds.disconnectAttr(source, destination)

    @staticmethod
    def get_connected_nodes(attr):
        return cmds.listConnections(attr, destination=True, source=False) or []


class ConnectionManager:
    def __init__(self, input_src_attr=None, input_dest_attr=None):
        self.validate_and_connect(input_src_attr, input_dest_attr)

    def validate_and_connect(self, src_attr, dest_attr):
        src_obj, src_attr_name = self.split_attribute(src_attr)
        dest_obj, dest_attr_name = self.split_attribute(dest_attr)

        self.validate_object(src_obj)
        self.validate_object(dest_obj)
        self.validate_or_create_attribute(src_obj, src_attr_name)
        self.validate_or_create_attribute(dest_obj, dest_attr_name)
        self.establish_connection(src_attr, dest_attr)

    @staticmethod
    def split_attribute(attr):
        obj, attr_name = attr.split('.')
        return obj, attr_name

    @staticmethod
    def validate_object(obj):
        if not cmds.objExists(obj):
            raise ValueError(f"ERROR: {obj} does not exist.")

    def validate_or_create_attribute(self, obj, attr):
        if not cmds.attributeQuery(attr, node=obj, exists=True):
            self.create_attribute(obj, attr)

    @staticmethod
    def create_attribute(obj, attr, attr_type, **kwargs):
        if not cmds.attributeQuery(attr, node=obj, exists=True):
            cmds.addAttr(obj, longName=attr, attributeType=attr_type, **kwargs)
            cmds.setAttr(f"{obj}.{attr}", e=True, keyable=True)
            print(f"CREATED: --|  {attr}  |-- on --|  {obj}  |--")

    @staticmethod
    def get_attribute_value(obj, attr):
        if cmds.attributeQuery(attr, node=obj, exists=True):
            return cmds.getAttr(f"{obj}.{attr}")
        return None

    @staticmethod
    def set_attribute_value(obj, attr, value):
        if cmds.attributeQuery(attr, node=obj, exists=True):
            cmds.setAttr(f"{obj}.{attr}", value)

    @staticmethod
    def establish_connection(src, dest):
        if not cmds.isConnected(src, dest):
            cmds.connectAttr(src, dest, f=True)
            print(f"CONNECTED: --|  {src}  |-- to --|  {dest}  |--")
        else:
            print(f"CONFIRMED: --|  {src}  |-- is already on --|  {dest}  |--")

    @staticmethod
    def establish_connection_with_utility(src, dest, utility_type, utility_name, util_in_attr, util_out_attr):
        utility_node = UtilityNodeManager.create_utility_node(utility_type, utility_name)
        UtilityNodeManager.connect_to_utility_node(src, utility_node, util_in_attr, util_out_attr, dest)
        print(f"Connected {src} through {utility_node} to {dest}")

    @staticmethod
    def conditional_connect(source, condition, true_dest, false_dest=None):
        if condition:
            ConnectionManager.establish_connection(source, true_dest)
        elif false_dest:
            ConnectionManager.establish_connection(source, false_dest)

    @staticmethod
    def set_multiple_attributes(obj, attr_values):
        for attr, value in attr_values.items():
            ConnectionManager.set_attribute_value(obj, attr, value)

    @staticmethod
    def connect_multiple_sources(sources, destination):
        for src in sources:
            ConnectionManager.establish_connection(src, destination)

# class ConnectionManager:
#     def __init__(self, controller='Transform_Ctrl', attr=None):
#         if not cmds.objExists(controller):
#             raise ValueError(f"ERROR: The CONTROLLER of the RK system {controller} does not exist.")
#         self.controller = controller
#         self.attr = None
# 
#     def run(self):
#         self.create_attributes()
#         self.connect_attributes()
# 
#     def create_attributes(self):
#         # Createself.attributes on the controller if not already there
#         if not cmds.attributeQuery(self.attr, node=self.controller, exists=True):
#             cmds.addAttr(self.controller, ln=self.attr, at='float', min=0, max=1, dv=1)
#             cmds.setAttr('%s.%s' % (self.controller, self.attr), e=True, keyable=True)
# 
#         else:
#             print(f"WARNING: {self.attr} already exists on {self.controller}")
# 
#     @staticmethod
#     def create_constraints(fk_leader, ik_leader, constrained_rk):
#         if not cmds.objExists(fk_leader):
#             raise ValueError(f"WARNING: {fk_leader} or {ik_leader} does not exist.")
#         name = constrained_rk.split('_RK')[0]
#         parent_constraint = cmds.parentConstraint(fk_leader, ik_leader, constrained_rk,
#                                                   name=f'{name}_IKFK_Constraining_{constrained_rk}_TRANSLATION'
#                                                        f'_ROTATION__parent_constraint', mo=False, weight=1)[0]
# 
#         scale_constraint = cmds.scaleConstraint(fk_leader, ik_leader, constrained_rk,  # noqa
#                                                 name=f'{name}_IKFK_Constraining_{constrained_rk}_SCALE_'
#                                                      f'_parent_constraint', weight=1)[0]
# 
#         return parent_constraint, parent_constraint
    
    # def connect_attributes(self, part, constraints):
    #     if not cmds.objExists(f"{self.attr}_Rev"):
    #         rev_node = cmds.shadingNode('reverse', name=f"{self.attr}_Rev", asUtility=True)
    #     else:
    #         rev_node = f"{self.attr}_Rev"
    # 
    #     for constraint in constraints:
    #         print(f"Connecting {self.attr} to {constraint}")
    # 
    #         if not cmds.isConnected(f"{self.controller}.{self.attr}",  f"{constraint}.w0"):
    #             cmds.connectAttr(f"{self.controller}.{self.attr}", f"{constraint}.w0", f=True)
    # 
    #         if not cmds.isConnected(f"{self.controller}.{self.attr}", f"{rev_node}.inputX"):
    #             cmds.connectAttr(f"{self.controller}.{self.attr}", f"{rev_node}.inputX", f=True)
    # 
    #         if not cmds.isConnected(f"{rev_node}.outputX", f"{constraint}.w1"):
    #             cmds.connectAttr(f"{rev_node}.outputX", f"{constraint}.w1", f=True)
    # 
    #         if not cmds.isConnected(f"{self.controller}.{self.attr}", f'{part}_FK_Ctrl_Grp.visibility'):
    #             cmds.connectAttr(f"{self.controller}.{self.attr}", f'{part}_FK_Ctrl_Grp.visibility', f=True)
    # 
    #         if not cmds.isConnected(f"{rev_node}.outputX", f'{part}_IK_Ctrl_Grp.visibility'):
    #             cmds.connectAttr(f"{rev_node}.outputX", f'{part}_IK_Ctrl_Grp.visibility', f=True)


if __name__ == '__main__':
    def module_name():
        import inspect
        import os
        # Get the current frame and find the file name of the script
        frame = inspect.currentframe()
        filename = inspect.getfile(frame)
        return os.path.basename(filename).split('.')[0]


    print(f"{'-' * 10 + '|' + ' ' * 4} RUNNING {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 10}")

    # sel = cmds.ls(allPaths=True)
    # for item in sel:
    #     if "IKFK" in item:
    #         cmds.delete(item)

    leader = "TARGET"
    follower = "AIMED"
    up_object = "UP"

    cmds.aimConstraint(leader, follower, worldUpType="object", worldUpVector=(0, 1, 0), worldUpObject=up_object,
                       weight=1, name=f'{follower}_to_{leader}__aim_constraint')
    # aimConstraint -offset 0 0 0 -weight 1 -aimVector 1 0 0 -upVector 0 1 0 -worldUpType "object" -worldUpObject UP;

    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED {module_name()} DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")
