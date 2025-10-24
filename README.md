# Quick Trigger Pie Menu (QT-Pie 🥧)
A simple Blender addon that adds a pie menu across editors for faster, left-hand access to common actions.
* This add-on replaces Blender's Quick Favorites hotkey with an easily accessible pie menu.
* The default entries target actions whose default hotkeys are awkward to hit with the left hand while the right hand stays on the mouse (e.g., Ctrl-P, O, Insert Keyframe).
* In the Settings of the add-on, you can edit each of the 8 slices with either **Label**, **Operator** (`category.operator`), or optional **Icon** to add your own custom entry to the Pie Menu.

<img width="813" height="498" alt="QT-Pie_v1 0 3 png" src="https://github.com/user-attachments/assets/f73a74b8-7bbd-44ee-bb12-4584209af04d" />


## Requirements

* Blender **4.5+**

## How to install

1. Go to **Edit → Preferences → Add-ons**
2. In the top-right corner, click the small drop-down arrow 🔽
3. Select `Install from Disk...`
4. Find and select the downloaded .py file `QT-Pie_v*.py` (latest release [here](https://github.com/polyfjord/QT-Pie/releases/))
5. The addon will be enabled with an icon ✅ next to it

## How to use

Once installed, press the hotkey **Q** to open the pie menu.

### Default pie entries (8 slices)

* ⬅️ Set Parent To Object
* ➡️ Pivot → 3D Cursor
* ⬆️ Pivot → Median Point
* ⬇️ Pivot → Individual Origins
* ↗️ Toggle Proportional Editing
* ↖️ View Render (F11)
* ↙️ Render Image (F12)
* ↘️ Insert Keys

## Settings

* In **Edit → Preferences → Add-ons → QT-Pie**, open **Settings (Advanced)** to edit any of the 8 slices with either **Label**, **Operator** (`category.operator` like `view3d.cursor3d`), or optional **Icon**. Includes a **Reset** button to restore default pie entries. 

<img width="909" height="595" alt="2025-10-23 13_20_21-Preferences" src="https://github.com/user-attachments/assets/6ef0f2e9-dba1-47ff-b603-bd2002334522" />

## Collaborations
If you are a developer and want to improve this project, please feel free to open a PR or create an issue.

Also, if you know your way around Blender/python/web apps/LLMs and want to brainstorm or collab on creative tools, please feel free to send me a DM on  [instagram](https://www.instagram.com/polyfjord/) or [bluesky](https://bsky.app/profile/polyfjord.com) with some of your work or ideas, and perhaps maybe we can make something cool together! 💡
