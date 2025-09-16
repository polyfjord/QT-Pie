# QT-Pie 🥧
A simple Blender addon that adds a pie menu across editors for faster, left-hand access to common actions.
* This add-on replaces Blender's Quick Favorites hotkey with an easily accessible pie menu.
* The default entries target actions whose stock hotkeys are awkward to hit with the left hand while the right hand stays on the mouse (e.g., Ctrl-P, O, Insert Keyframe)
* Planned: an in-Blender UI to customize pie entries (similar to the current implementation of Quick Favorites).

# Quick Trigger Pie Menu (QT-Pie)

## Requirements

* Blender **4.5+**

## How to install

1. `Edit → Preferences → Add-ons → Install…`
2. Select `Quick_Trigger_Pie_Menu_QT-Pie_v1_0.py`
3. Enable the add-on.

## How to use

* Once installed, press the hotkey **Q** to open the pie menu.

### Pie entries (8-way)

* **Left:** Set Parent To…
* **Right:** Pivot → 3D Cursor
* **Up:** Pivot → Median Point
* **Down:** Pivot → Individual Origins
* **Up-Right:** Toggle Proportional Editing
* **Up-Left:** View Render (F11)
* **Down-Left:** Render Image (F12)
* **Down-Right:** Insert Keyframe Menu

> Note: Some entries are context-sensitive (e.g., parenting requires a valid 3D selection).

## Editors

Works in the 3D View and other editors including: **Image**, **Node**, **Graph**, **Dopesheet**, **NLA**, **Sequencer**, **Movie Clip**, **Outliner**, **Properties**, **Text**, **Console**.
