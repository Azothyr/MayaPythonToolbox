import sys
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' in sys.path:
    sys.path.remove('C:/GitRepos/MayaPythonToolbox/maya_scripts')
if 'C:/GitRepos/MayaPythonToolbox/maya_scripts' not in sys.path:
    sys.path.append('C:/GitRepos/MayaPythonToolbox/maya_scripts')
import maya.cmds as cmds
from pprint import pprint
import re
from managers.base_maya_objects.joint_manager import JointManager


def get_part_names(data):
    output = []
    exclude = ['COG', 'HELPER', 'Unknown']
    base_part = [x for x in data.keys() if x not in exclude]
    object_names = []
    [object_names.extend(data[x]['joints']) for x in base_part]

    for name in object_names:
        # Split the name at _FK, _RK, _IK, or _Jnt
        split_name = re.split(r'_FK_|_RK_|_IK_|_Jnt', name)
        output.append(split_name[0])  # Take the first part before these suffixes

    return output


class BrokenGeoConstrainer:
    def __init__(self):
        self.joint_manager = JointManager()
        self.data = get_part_names(self.joint_manager.data)

    def get_corresponding_mesh(self):
        mesh_list = cmds.ls(type="mesh")
        mesh_names = [item.split("|")[-1].split("Shape")[0] for item in mesh_list]
        pprint(f"Mesh: {mesh_names}")
        joint_to_mesh_map = {}

        for joint_base_name in self.data:
            # Find meshes that start with the joint base name
            matched_meshes = [mesh for mesh in mesh_names if mesh.startswith(joint_base_name)]
            if matched_meshes:
                joint_to_mesh_map[joint_base_name] = matched_meshes

        return joint_to_mesh_map

    def run(self):
        # Get the mesh to joint mapping
        mesh_to_joint_mapping = self.get_corresponding_mesh()
        pprint(f"Mesh to Joint Mapping: {mesh_to_joint_mapping}")

        # Constrain each mesh to its corresponding joint
        for joint_base, meshes in mesh_to_joint_mapping.items():
            joint_name = f"{joint_base}_Jnt"  # or however the actual joint name is formed
            # for mesh in meshes:
            #     cmds.parentConstraint(joint_name, mesh, mo=True)


if __name__ == "__main__":
    print(f"{'-' * 10 + '|' + ' ' * 4} RUNNING DUNDER MAIN {' ' * 4 + '|' + '-' * 10}")
    geo_constrainer = BrokenGeoConstrainer()
    geo_constrainer.run()
    print(f"{'-' * 25 + '|' + ' ' * 4} COMPLETED DUNDER MAIN {' ' * 4 + '|' + '-' * 25}")

