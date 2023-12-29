import maya.cmds as cmds


class ConnectionCmds:
    @staticmethod
    def is_connected(src_attr, dest_attr):
        """Check if an attribute is already connected to another attribute."""
        connections = cmds.listConnections(dest_attr, plugs=True, source=True, destination=False)
        return src_attr in connections if connections else False