# URDF & XACRO 3D Visualization and Customization Tool

An interactive, GUI-driven Python tool designed to parse, visualize, and edit 3D joint coordinate frames of mobile robots directly from URDF or XACRO files.

---

## 🤖 New to URDF & XACRO? Read This First!

If you are new to robotics, these concepts are essential:

| Concept | Explanation |
| :--- | :--- |
| **URDF** | **Unified Robot Description Format**. An XML file that describes a robot's physical structure—its shape, weight, visual meshes, and how its parts connect. |
| **XACRO** | **XML Macros**. An upgraded, modular version of URDF that allows variables, formulas, and reusable components. |
| **Link** | A rigid body component of the robot (e.g., base chassis, wheel, LiDAR body). |
| **Joint** | The connection point between two links (e.g., a wheel motor axle attached to the chassis). |
| **Origin (XYZ)** | The 3D coordinate space $(X, Y, Z)$ defining where a joint is attached relative to its parent link. |

---

## 🛠️ What This Tool Does

1. **Scans & Parses:** Reads any `.xacro` or `.urdf` file to extract joint origin coordinates.
2. **Interactive GUI:** Uses native Zenity pop-ups to let you select which joint to modify and preview its current origin values.
3. **Custom Export:** Automatically generates a customized `.xacro` file (`scuttle_custom.xacro`) with your updated parameters.
4. **Interactive 3D Visualizer:** Opens an interactive 3D plot displaying coordinate axes (Red=X, Green=Y, Blue=Z) for all robot joints with mouse rotation and zoom support.

---

## 🚀 Quick Start Guide

### Prerequisites
* Windows 10/11 with **WSL2** (Ubuntu environment) installed **or** Ubuntu 20 - 26.
* Python 3.8+

### 1. Installation & Cloning
Clone the repository directly into your home directory (`/home/$USER/URDF-Visualizer-Editor`) and run the setup script:

```bash
# Clone directly into your home directory
git clone https://github.com/ADMiNZ17/URDF-Visualizer-Editor.git ~/URDF-Visualizer-Editor

# Navigate to the project folder
cd ~/URDF-Visualizer-Editor

# Run automated setup script for dependencies and virtual environment
chmod +x dependency.sh
./dependency.sh
```

---

### 2. Running the Tool
Activate your virtual environment and launch the main Python script:

```bash
source venv/bin/activate
python3 mplot3d.py
```

### 3. Usage Workflow
1. **Select File:** A pop-up will ask you to choose a `.xacro` or `.urdf` file (e.g., `AMR01.xacro`).
2. **Select Joint:** Choose the joint you wish to edit from the list.
3. **Enter Offsets:** Enter new $X$, $Y$, or $Z$ offset values in meters (or leave blank to retain original values).
4. **View Output:** The script saves `scuttle_custom.xacro` and launches the 3D mouse-interactive plot.

## 📂 Repository Structure
```
URDF-Visualizer-Editor/
├── Example.xacro         # Sample robot model file
├── dependency.sh         # Shell script to auto-install dependencies & setup venv
├── mplot3d.py            # Main application logic and 3D rendering pipeline
├── scuttle_custom.xacro  # Auto-generated customized output file
└── README.md             # Documentation
```
