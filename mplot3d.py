import xml.etree.ElementTree as ET
import subprocess
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

# Helper function to run Zenity and suppress libEGL/MESA warnings in WSL
def run_zenity(cmd):
    try:
        # stderr=subprocess.DEVNULL hides the WSL graphical backend warnings
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

# 1. Trigger Zenity Pop-up to Select File
def select_xacro_file():
    cmd = [
        'zenity', '--file-selection',
        '--title=Select XACRO/URDF File',
        '--file-filter=*.xacro *.urdf'
    ]
    filepath = run_zenity(cmd)
    if not filepath:
        print("File selection cancelled. Exiting.")
        sys.exit(0)
    return filepath

# 2. Parse Joint Coordinate Vectors from URDF File
def parse_urdf_joints(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    joints = {}
    for joint in root.findall('joint'):
        name = joint.get('name')
        origin = joint.find('origin')
        if origin is not None and 'xyz' in origin.attrib:
            xyz = [float(val) for val in origin.attrib['xyz'].split()]
            joints[name] = xyz
    return joints, root, tree

# 3. Select Joint to Modify
def select_joint(joints):
    cmd = [
        'zenity', '--list', 
        '--title=Select Joint', 
        '--text=Choose a joint to modify:', 
        '--column=Joint Name'
    ]
    cmd.extend(joints.keys())
    
    joint_name = run_zenity(cmd)
    if not joint_name:
        print("Joint selection cancelled. Exiting.")
        sys.exit(0)
    return joint_name

# 4. Trigger Zenity Pop-up to Collect Custom Parameters
def get_user_parameters(joint_name, orig_xyz):
    cmd = [
        'zenity', '--forms',
        f'--title=Modify {joint_name}',
        f'--text=Original Origin:\nX: {orig_xyz[0]} | Y: {orig_xyz[1]} | Z: {orig_xyz[2]}\n\nEnter new offsets (leave blank to keep original):',
        '--add-entry=New X',
        '--add-entry=New Y',
        '--add-entry=New Z'
    ]
    
    result = run_zenity(cmd)
    if not result:
        print("Parameter modification cancelled. Exiting.")
        sys.exit(0)
        
    # Parse inputs and fallback to original values if left blank
    inputs = result.split('|')
    new_x = float(inputs[0]) if inputs[0].strip() else orig_xyz[0]
    new_y = float(inputs[1]) if inputs[1].strip() else orig_xyz[1]
    new_z = float(inputs[2]) if inputs[2].strip() else orig_xyz[2]
    
    return [new_x, new_y, new_z]

# 5. Interactive 3D Vector Visualization
def visualize_joints(joints):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    for name, (x, y, z) in joints.items():
        ax.scatter(x, y, z, color='blue', s=40)
        ax.text(x, y, z + 0.02, name, fontsize=8)
        
        arrow_length = 0.05
        ax.quiver(x, y, z, arrow_length, 0, 0, color='r', alpha=0.8)
        ax.quiver(x, y, z, 0, arrow_length, 0, color='g', alpha=0.8)
        ax.quiver(x, y, z, 0, 0, arrow_length, color='b', alpha=0.8)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Interactive Joint Coordinate Frames (Drag mouse to rotate)')
    
    # Suppress output from matplotlib backend
    try:
        plt.show()
    except Exception as e:
        print(f"Matplotlib rendering closed: {e}")

# 6. Generate New Custom .xacro File
def generate_xacro(tree, root, joint_name, new_xyz, output_filename="scuttle_custom.xacro"):
    for joint in root.findall('joint'):
        if joint.get('name') == joint_name:
            origin = joint.find('origin')
            if origin is not None:
                origin.set('xyz', f"{new_xyz[0]} {new_xyz[1]} {new_xyz[2]}")
                
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)
    print(f"Successfully generated new XACRO file: {output_filename}")

if __name__ == "__main__":
    # Select File
    filepath = select_xacro_file()
    print(f"Selected file: {filepath}")
    
    # Parse existing data
    joints_dict, urdf_root, urdf_tree = parse_urdf_joints(filepath)
    
    # Select target joint
    target_joint = select_joint(joints_dict)
    
    # Get new coordinates based on original
    new_xyz = get_user_parameters(target_joint, joints_dict[target_joint])
    
    # Update dict and save XML
    joints_dict[target_joint] = new_xyz
    generate_xacro(urdf_tree, urdf_root, target_joint, new_xyz, "scuttle_custom.xacro")
    
    # Render 3D map
    visualize_joints(joints_dict)