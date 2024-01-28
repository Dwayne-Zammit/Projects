import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

coords_file_path = os.path.join(parent_directory, "walker/walker/coords.txt")



def get_list_of_path_coords(start_line):
    with open(coords_file_path, "r") as coords_file:
        # Read all lines from the file
        all_lines = coords_file.readlines()
        # Extract lines from start_line to end_line
        path_coords = all_lines[start_line - 1:start_line+40]
        return path_coords


def check_if_change_plane_soon(current_line_z):
    path = (get_list_of_path_coords(start_line=current_line_z))
    print(path)
    # try:
    for line in path:
        line_z = line.strip().split(",")[2]
        if line_z != current_line_z:
            print("Need to change plane")
            return True
    # except:
        # print("error....")        
    # print("")    
    return False
