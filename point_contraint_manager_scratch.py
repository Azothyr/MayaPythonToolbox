import maya.cmds as cmds


class ConnectionManager:
    def __init__(self, input_src_attr=None, input_dest_attr=None):
        src_obj = input_src_attr.split('.')[0]
        src_attr = input_src_attr.split('.')[1]
        dest_obj = input_dest_attr.split('.')[0]
        dest_attr = input_dest_attr.split('.')[1]
        
        try:
            if not cmds.objExists(src_obj):
                err = ValueError(f"ERROR: {src_obj} does not exist.")
                raise err
            if not cmds.objExists(dest_obj):
                err = ValueError(f"ERROR: {dest_obj} does not exist.")
                raise err
            if not cmds.attributeQuery(src_attr, node=src_obj, exists=True):
                err = ValueError(f"ERROR: {input_src_attr} is not connected to {input_dest_attr}")
            if not cmds.attributeQuery(src_attr, node=src_obj, exists=True):
                err = ValueError(f"ERROR: {input_src_attr} is not connected to {input_dest_attr}")
            if not cmds.isConnected(input_src_attr, input_dest_attr):
                err = ValueError(f"ERROR: {source} is not connected to {destination}")
                raise err
        except ValueError as err:
            raise err
        
    @staticmethod
    def create_attribute(obj, attr, **kwargs):
        if not cmds.attributeQuery(attr, node=obj, exists=True):
            cmds.addAttr(obj, ln=attr, **kwargs)
            cmds.setAttr(f"{obj}.{attr}", e=True, keyable=True)

        if cmds.attributeQuery(attr, node=obj, exists=True):
            print(f"CONFIRMED: --|  {attr}  |-- is on --|  {obj}  |--")
            return True
        return False

    @staticmethod
    def connect_attributes(source, destination):
        if not cmds.isConnected(source, destination):
            cmds.connectAttr(source, destination, f=True)
        
        if cmds.isConnected(source, destination):
            print(f"CONFIRMED: --|  {source}  |-- is connected to --|  {destination}  |--")
            return True
        return False


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
