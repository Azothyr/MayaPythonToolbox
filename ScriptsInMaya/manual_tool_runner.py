from maya_scripts.utilities.global_var import GlobalVar

center_locations = GlobalVar('center_locations', value=[0.0, 1, 2])
print(len(center_locations))
for val in center_locations:
    print(val)
