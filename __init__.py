bl_info = {
    "name": "QT-Pie",
    "author": "polyfjord",
    "version": (1, 2, 0),
    "blender": (4, 5, 0),
    "location": "Everywhere",
    "description": "Rapid access to commands with customizable pie menus and unlimited sub-menus.",
    "category": "Interface",
}

import bpy
from bpy.props import (
    StringProperty,
    EnumProperty,
    CollectionProperty,
    IntProperty,
    BoolProperty,
)

ARROW_LABELS = {
    "N": "↑",
    "S": "↓",
    "E": "→",
    "W": "←",
    "NE": "↗",
    "NW": "↖",
    "SE": "↘",
    "SW": "↙",
}

SLOT_ITEMS = [
    ("W", ARROW_LABELS["W"], "West/Left segment of the pie"),
    ("E", ARROW_LABELS["E"], "East/Right segment of the pie"),
    ("S", ARROW_LABELS["S"], "South/Bottom segment of the pie"),
    ("N", ARROW_LABELS["N"], "North/Top segment of the pie"),
    ("NW", ARROW_LABELS["NW"], "North-West segment of the pie"),
    ("NE", ARROW_LABELS["NE"], "North-East segment of the pie"),
    ("SW", ARROW_LABELS["SW"], "South-West segment of the pie"),
    ("SE", ARROW_LABELS["SE"], "South-East segment of the pie"),
]

SLOT_ORDER = [slot for slot, _, _ in SLOT_ITEMS]

HOTKEY_ITEMS = [
    ("Q", "Q", "Q key"),
    ("W", "W", "W key"),
    ("E", "E", "E key"),
    ("R", "R", "R key"),
    ("T", "T", "T key"),
    ("Y", "Y", "Y key"),
    ("U", "U", "U key"),
    ("I", "I", "I key"),
    ("O", "O", "O key"),
    ("P", "P", "P key"),
    ("A", "A", "A key"),
    ("S", "S", "S key"),
    ("D", "D", "D key"),
    ("F", "F", "F key"),
    ("G", "G", "G key"),
    ("H", "H", "H key"),
    ("J", "J", "J key"),
    ("K", "K", "K key"),
    ("L", "L", "L key"),
    ("Z", "Z", "Z key"),
    ("X", "X", "X key"),
    ("C", "C", "C key"),
    ("V", "V", "V key"),
    ("B", "B", "B key"),
    ("N", "N", "N key"),
    ("M", "M", "M key"),
    ("ZERO", "0", "0 key"),
    ("ONE", "1", "1 key"),
    ("TWO", "2", "2 key"),
    ("THREE", "3", "3 key"),
    ("FOUR", "4", "4 key"),
    ("FIVE", "5", "5 key"),
    ("SIX", "6", "6 key"),
    ("SEVEN", "7", "7 key"),
    ("EIGHT", "8", "8 key"),
    ("NINE", "9", "9 key"),
    ("SPACE", "Space", "Spacebar"),
    ("TAB", "Tab", "Tab key"),
    ("SEMI_COLON", ";", "Semicolon key"),
    ("PERIOD", ".", "Period key"),
    ("COMMA", ",", "Comma key"),
    ("F1", "F1", "F1 key"),
    ("F2", "F2", "F2 key"),
    ("F3", "F3", "F3 key"),
    ("F4", "F4", "F4 key"),
    ("F5", "F5", "F5 key"),
    ("F6", "F6", "F6 key"),
    ("F7", "F7", "F7 key"),
    ("F8", "F8", "F8 key"),
    ("F9", "F9", "F9 key"),
    ("F10", "F10", "F10 key"),
    ("F11", "F11", "F11 key"),
    ("F12", "F12", "F12 key"),
    ("F13", "F13", "F13 key"),
    ("F14", "F14", "F14 key"),
    ("F15", "F15", "F15 key"),
    ("F16", "F16", "F16 key"),
    ("F17", "F17", "F17 key"),
    ("F18", "F18", "F18 key"),
    ("F19", "F19", "F19 key"),
    ("F20", "F20", "F20 key"),
    ("F21", "F21", "F21 key"),
    ("F22", "F22", "F22 key"),
    ("F23", "F23", "F23 key"),
    ("F24", "F24", "F24 key"),
    ("LEFT_ARROW", "Left Arrow", "Left Arrow key"),
    ("RIGHT_ARROW", "Right Arrow", "Right Arrow key"),
    ("UP_ARROW", "Up Arrow", "Up Arrow key"),
    ("DOWN_ARROW", "Down Arrow", "Down Arrow key"),
    ("HOME", "Home", "Home key"),
    ("END", "End", "End key"),
    ("PAGE_UP", "Page Up", "Page Up key"),
    ("PAGE_DOWN", "Page Down", "Page Down key"),
    ("INSERT", "Insert", "Insert key"),
    ("DELETE", "Delete", "Delete key"),
    ("BACK_SPACE", "Backspace", "Backspace key"),
    ("RET", "Enter", "Enter/Return key"),
    ("ESC", "Escape", "Escape key"),
    ("NUMPAD_0", "Numpad 0", "Numpad 0"),
    ("NUMPAD_1", "Numpad 1", "Numpad 1"),
    ("NUMPAD_2", "Numpad 2", "Numpad 2"),
    ("NUMPAD_3", "Numpad 3", "Numpad 3"),
    ("NUMPAD_4", "Numpad 4", "Numpad 4"),
    ("NUMPAD_5", "Numpad 5", "Numpad 5"),
    ("NUMPAD_6", "Numpad 6", "Numpad 6"),
    ("NUMPAD_7", "Numpad 7", "Numpad 7"),
    ("NUMPAD_8", "Numpad 8", "Numpad 8"),
    ("NUMPAD_9", "Numpad 9", "Numpad 9"),
    ("NUMPAD_PERIOD", "Numpad .", "Numpad Period"),
    ("NUMPAD_SLASH", "Numpad /", "Numpad Slash"),
    ("NUMPAD_ASTERIX", "Numpad *", "Numpad Asterisk"),
    ("NUMPAD_MINUS", "Numpad -", "Numpad Minus"),
    ("NUMPAD_PLUS", "Numpad +", "Numpad Plus"),
    ("NUMPAD_ENTER", "Numpad Enter", "Numpad Enter"),
    ("LEFT_BRACKET", "[", "Left Bracket"),
    ("RIGHT_BRACKET", "]", "Right Bracket"),
    ("LEFT_CTRL", "Left Ctrl", "Left Control key"),
    ("RIGHT_CTRL", "Right Ctrl", "Right Control key"),
    ("LEFT_ALT", "Left Alt", "Left Alt key"),
    ("RIGHT_ALT", "Right Alt", "Right Alt key"),
    ("LEFT_SHIFT", "Left Shift", "Left Shift key"),
    ("RIGHT_SHIFT", "Right Shift", "Right Shift key"),
    ("OSKEY", "OS Key", "OS Key (Windows/Cmd)"),
    ("GRLESS", "\\", "Backslash key"),
    ("ACCENT_GRAVE", "`", "Backtick/Grave accent key"),
    ("MINUS", "-", "Minus key"),
    ("EQUAL", "=", "Equals key"),
    ("SLASH", "/", "Slash key"),
    ("QUOTE", "'", "Quote key"),
]

DEFAULT_MENU_ENTRIES = {
    "W": {"label": "Set Parent to Object", "operator": "view3d.qtpie_parent_set_object", "icon": "CON_CHILDOF"},
    "E": {"label": "Pivot: Cursor", "operator": "view3d.qtpie_set_pivot", "icon": ""},
    "S": {"label": "Pivot: Individual Origins", "operator": "view3d.qtpie_set_pivot", "icon": ""},
    "N": {"label": "Pivot: Median Point", "operator": "view3d.qtpie_set_pivot", "icon": ""},
    "NW": {"label": "View Render", "operator": "view3d.qtpie_view_render", "icon": "RENDER_RESULT"},
    "NE": {"label": "Toggle Proportional Edit", "operator": "view3d.toggle_proportional_edit_smart", "icon": "PROP_ON"},
    "SW": {"label": "Render Image", "operator": "view3d.qtpie_render_image", "icon": "RENDER_STILL"},
    "SE": {"label": "Insert Keys", "operator": "view3d.qtpie_insert_keys", "icon": "KEY_HLT"},
}


def _module_name_candidates():
    names = [__name__]
    base = __name__.partition(".")[0]
    if base and base not in names:
        names.append(base)
    addon_name = bl_info.get("name")
    if addon_name:
        if addon_name not in names:
            names.append(addon_name)
        underscored = addon_name.replace(" ", "_")
        if underscored not in names:
            names.append(underscored)
    return names


def get_addon_preferences(context=None, ensure_defaults=True):
    ctx = context or bpy.context
    for name in _module_name_candidates():
        addon = ctx.preferences.addons.get(name)
        if addon:
            prefs = addon.preferences
            if ensure_defaults:
                ensure = getattr(prefs, "ensure_defaults", None)
                if ensure:
                    ensure()
            return prefs
    return None


def _get_hotkey_display_name(hotkey_value):
    """Get display name for hotkey enum value."""
    for key, display, _ in HOTKEY_ITEMS:
        if key == hotkey_value:
            return display
    return hotkey_value


def _entry_update_callback(self, context):
    """Update storage when entries change."""
    if context:
        prefs = get_addon_preferences(context, ensure_defaults=False)
        if prefs:
            # Delay sync to avoid issues during property updates
            def sync_and_save():
                prefs.sync_current_entries()
                # Force save preferences
                bpy.ops.wm.save_userpref()
                return None
            bpy.app.timers.register(sync_and_save, first_interval=0.01)


def _update_hotkey(self, context):
    """Update keymap when hotkey preference changes."""
    # Unregister old keymap
    for km, kmi in addon_keymaps[:]:
        try:
            km.keymap_items.remove(kmi)
        except Exception:
            pass
    addon_keymaps.clear()
    
    # Re-register with new hotkey
    wm = getattr(context, "window_manager", None) if context else getattr(bpy.context, "window_manager", None)
    kc = wm.keyconfigs.addon if wm else None
    if kc:
        for name, space in SPACE_KEYMAPS:
            _add_keymap(kc, name, space)
    
    # Save preferences immediately
    try:
        bpy.ops.wm.save_userpref()
    except Exception:
        pass


class QTPieMenuEntry(bpy.types.PropertyGroup):
    slot: EnumProperty(
        name="Slot",
        description="Pie slice this entry occupies",
        items=SLOT_ITEMS,
        default="W",
    )
    label: StringProperty(
        name="Label",
        description="Text shown for this entry in the pie menu",
        default="",
        update=_entry_update_callback,
    )
    operator: StringProperty(
        name="Operator",
        description="Operator identifier (e.g. view3d.cursor3d)",
        default="",
        update=_entry_update_callback,
    )
    icon: StringProperty(
        name="Icon",
        description="Blender icon identifier (e.g. RENDER_RESULT)",
        default="",
        update=_entry_update_callback,
    )


class QTPieSubMenu(bpy.types.PropertyGroup):
    name: StringProperty(
        name="Name",
        description="Name of this sub-menu",
        default="Sub Menu",
    )
    menu_id: IntProperty(
        name="Menu ID",
        description="Unique identifier for this sub-menu",
        default=0,
    )


class QTPiePreferences_UL_entries(bpy.types.UIList):
    bl_idname = "QTPiePreferences_UL_entries"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            split = layout.split(factor=0.2)
            arrow = ARROW_LABELS.get(item.slot, item.slot or "?")
            split.label(text=arrow)
            split.label(text=item.label or "Empty")
        elif self.layout_type == "GRID":
            layout.alignment = 'CENTER'
            arrow = ARROW_LABELS.get(item.slot, item.slot or "?")
            layout.label(text=arrow)


class QTPiePreferences_UL_submenus(bpy.types.UIList):
    bl_idname = "QTPiePreferences_UL_submenus"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=f"{item.name} (ID: {item.menu_id})", icon="MENU_PANEL")
        elif self.layout_type == "GRID":
            layout.alignment = 'CENTER'
            layout.label(text=str(item.menu_id), icon="MENU_PANEL")


class QTPiePreferences_OT_reset_entries(bpy.types.Operator):
    bl_idname = "qtpie.reset_entries"
    bl_label = "Reset Pie Entries"
    bl_description = "Restore the original entries for the current menu."
    bl_options = {"INTERNAL"}

    def execute(self, context):
        prefs = get_addon_preferences(context)
        if not prefs:
            self.report({'WARNING'}, "QT-Pie preferences not available")
            return {'CANCELLED'}
        prefs.reset_to_defaults()
        self.report({'INFO'}, "QT-Pie pie menu entries reset")
        return {'FINISHED'}


class QTPiePreferences_OT_clear_entry(bpy.types.Operator):
    bl_idname = "qtpie.clear_entry"
    bl_label = "Clear Entry"
    bl_description = "Clear the selected entry from the current menu"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        prefs = get_addon_preferences(context, ensure_defaults=False)
        if not prefs:
            self.report({'ERROR'}, "QT-Pie preferences not available")
            return {'CANCELLED'}

        if prefs.entries and 0 <= prefs.entries_index < len(prefs.entries):
            entry = prefs.entries[prefs.entries_index]
            entry.label = ""
            entry.operator = ""
            entry.icon = ""
            self.report({'INFO'}, "Entry cleared")
        else:
            self.report({'WARNING'}, "QT-Pie: No entry selected")
        
        return {'FINISHED'}


class QTPiePreferences_OT_add_submenu(bpy.types.Operator):
    bl_idname = "qtpie.add_submenu"
    bl_label = "Add Sub-Menu"
    bl_description = "Create a new custom sub-menu"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        prefs = get_addon_preferences(context, ensure_defaults=False)
        if not prefs:
            self.report({'ERROR'}, "QT-Pie preferences not available")
            return {'CANCELLED'}
        
        try:
            used_ids = {submenu.menu_id for submenu in prefs.submenus}
            next_id = 0
            while next_id in used_ids:
                next_id += 1
            
            new_submenu = prefs.submenus.add()
            new_submenu.name = f"Custom Menu {next_id}"
            new_submenu.menu_id = next_id
            
            # Initialize entries for this submenu
            for slot in SLOT_ORDER:
                entry = prefs.submenu_entries.add()
                entry.slot = slot
                entry.label = ""
                entry.operator = ""
                entry.icon = ""
                entry.submenu_id = next_id
            
            prefs.submenus_index = len(prefs.submenus) - 1
            
            # Force save preferences
            try:
                bpy.ops.wm.save_userpref()
            except:
                pass
            
            for area in context.screen.areas:
                area.tag_redraw()
            
            try:
                register_submenu_classes()
                register_submenu_operators()
            except Exception as e:
                self.report({'ERROR'}, f"QT-Pie: Failed to register sub-menu: {e}")
            
            self.report({'INFO'}, f"Sub-menu created with ID {next_id}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"QT-Pie: Error adding sub-menu: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


class QTPiePreferences_OT_remove_submenu(bpy.types.Operator):
    bl_idname = "qtpie.remove_submenu"
    bl_label = "Remove Sub-Menu"
    bl_description = "Delete the selected sub-menu"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        prefs = get_addon_preferences(context, ensure_defaults=False)
        if not prefs:
            self.report({'ERROR'}, "QT-Pie preferences not available")
            return {'CANCELLED'}
        
        try:
            index = prefs.submenus_index
            
            if 0 <= index < len(prefs.submenus):
                menu_id = prefs.submenus[index].menu_id
                
                # Remove entries for this submenu (remove in reverse order)
                indices_to_remove = [i for i, entry in enumerate(prefs.submenu_entries) if entry.submenu_id == menu_id]
                for i in reversed(indices_to_remove):
                    prefs.submenu_entries.remove(i)
                
                prefs.submenus.remove(index)
                prefs.submenus_index = max(0, min(prefs.submenus_index, len(prefs.submenus) - 1))
                
                if prefs.editing_submenu_index == index:
                    prefs.editing_submenu_index = -1
                elif prefs.editing_submenu_index > index:
                    prefs.editing_submenu_index -= 1
                
                # Force save preferences
                try:
                    bpy.ops.wm.save_userpref()
                except:
                    pass
                
                try:
                    register_submenu_classes()
                    register_submenu_operators()
                except Exception as e:
                    self.report({'ERROR'}, f"QT-Pie: Failed to re-register menus: {e}")
                
                self.report({'INFO'}, "Sub-menu removed")
            else:
                self.report({'WARNING'}, "QT-Pie: No sub-menu selected")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"QT-Pie: Error removing sub-menu: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}


class QTPiePreferences_OT_edit_main_menu(bpy.types.Operator):
    bl_idname = "qtpie.edit_main_menu"
    bl_label = "Edit Main Menu"
    bl_description = "Switch to editing the main menu"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        prefs = get_addon_preferences(context, ensure_defaults=False)
        if not prefs:
            return {'CANCELLED'}
        # Save current entries before switching
        prefs.sync_current_entries()
        prefs.editing_submenu_index = -1
        prefs.sync_entries_list()
        return {'FINISHED'}


class QTPiePreferences_OT_edit_submenu(bpy.types.Operator):
    bl_idname = "qtpie.edit_submenu"
    bl_label = "Edit Sub-Menu"
    bl_description = "Switch to editing the selected sub-menu"
    bl_options = {"INTERNAL"}

    index: IntProperty()

    def execute(self, context):
        prefs = get_addon_preferences(context, ensure_defaults=False)
        if not prefs:
            return {'CANCELLED'}
        # Save current entries before switching
        prefs.sync_current_entries()
        prefs.editing_submenu_index = self.index
        prefs.sync_entries_list()
        return {'FINISHED'}


class QTPiePreferences_OT_open_icon_docs(bpy.types.Operator):
    bl_idname = "qtpie.open_icon_docs"
    bl_label = "Open Icon Documentation"
    bl_description = "Open Blender icon list in web browser"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        import webbrowser
        url = "https://docs.blender.org/manual/en/latest/contribute/manual/guides/icons.html"
        try:
            webbrowser.open(url)
        except Exception:
            self.report({'ERROR'}, f"QT-Pie: Could not open browser. Visit: {url}")
        return {'FINISHED'}


class QTPieSubMenuEntry(bpy.types.PropertyGroup):
    slot: EnumProperty(
        name="Slot",
        description="Pie slice this entry occupies",
        items=SLOT_ITEMS,
        default="W",
    )
    label: StringProperty(
        name="Label",
        description="Text shown for this entry in the pie menu",
        default="",
    )
    operator: StringProperty(
        name="Operator",
        description="Operator identifier (e.g. view3d.cursor3d)",
        default="",
    )
    icon: StringProperty(
        name="Icon",
        description="Blender icon identifier (e.g. RENDER_RESULT)",
        default="",
    )
    submenu_id: IntProperty(
        name="Submenu ID",
        description="ID of the submenu this entry belongs to",
        default=-1,
    )


class QTPieMainMenuStorage(bpy.types.PropertyGroup):
    """Persistent storage for main menu entries."""
    slot: EnumProperty(
        name="Slot",
        description="Pie slice this entry occupies",
        items=SLOT_ITEMS,
        default="W",
    )
    label: StringProperty(
        name="Label",
        description="Text shown for this entry in the pie menu",
        default="",
    )
    operator: StringProperty(
        name="Operator",
        description="Operator identifier (e.g. view3d.cursor3d)",
        default="",
    )
    icon: StringProperty(
        name="Icon",
        description="Blender icon identifier (e.g. RENDER_RESULT)",
        default="",
    )


class QTPieAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    show_advanced: BoolProperty(
        name="Settings (Advanced)",
        description="Show or hide advanced pie menu customization options",
        default=False,
    )
    hotkey: EnumProperty(
        name="Hotkey",
        description="Keyboard key to open the QT-Pie menu",
        items=HOTKEY_ITEMS,
        default="Q",
        update=lambda self, context: _update_hotkey(self, context),
    )
    entries: CollectionProperty(type=QTPieMenuEntry)
    entries_index: IntProperty(default=0)
    
    # Persistent storage for main menu (never cleared)
    main_menu_storage: CollectionProperty(type=QTPieMainMenuStorage)
    
    submenus: CollectionProperty(type=QTPieSubMenu)
    submenus_index: IntProperty(default=0)
    submenu_entries: CollectionProperty(type=QTPieSubMenuEntry)
    
    editing_submenu_index: IntProperty(
        default=-1,
        description="Index of the submenu being edited. -1 for main menu."
    )
    
    def save_main_menu_to_storage(self):
        """Save current entries to persistent main menu storage."""
        # Clear and rebuild storage
        self.main_menu_storage.clear()
        for entry in self.entries:
            stored = self.main_menu_storage.add()
            stored.slot = entry.slot
            stored.label = entry.label
            stored.operator = entry.operator
            stored.icon = entry.icon
        # Force save to userpref.blend
        try:
            bpy.ops.wm.save_userpref()
        except:
            pass  # May fail if called during registration
    
    def load_main_menu_from_storage(self):
        """Load main menu entries from persistent storage."""
        self.entries.clear()
        
        # Build dict from storage
        storage_by_slot = {e.slot: e for e in self.main_menu_storage}
        
        # Populate entries list with all slots
        for slot in SLOT_ORDER:
            entry = self.entries.add()
            entry.slot = slot
            if slot in storage_by_slot:
                stored = storage_by_slot[slot]
                entry.label = stored.label
                entry.operator = stored.operator
                entry.icon = stored.icon
            else:
                # No stored data, use defaults
                defaults = DEFAULT_MENU_ENTRIES[slot]
                entry.label = defaults["label"]
                entry.operator = defaults["operator"]
                entry.icon = defaults["icon"]
    
    def get_submenu_entries(self, menu_id):
        """Get entries for a specific submenu."""
        return [e for e in self.submenu_entries if e.submenu_id == menu_id]
    
    def save_submenu_entries(self, menu_id, entries_list):
        """Save entries for a specific submenu."""
        # Remove old entries for this submenu
        indices_to_remove = [i for i, entry in enumerate(self.submenu_entries) if entry.submenu_id == menu_id]
        for i in reversed(indices_to_remove):
            self.submenu_entries.remove(i)
        # Add current entries
        for entry in entries_list:
            submenu_entry = self.submenu_entries.add()
            submenu_entry.slot = entry.slot
            submenu_entry.label = entry.label
            submenu_entry.operator = entry.operator
            submenu_entry.icon = entry.icon
            submenu_entry.submenu_id = menu_id
        # Force save to userpref.blend
        try:
            bpy.ops.wm.save_userpref()
        except:
            pass  # May fail if called during registration
    
    def load_submenu_entries(self, menu_id):
        """Load entries for a specific submenu into entries list."""
        self.entries.clear()
        submenu_entries = self.get_submenu_entries(menu_id)
        entries_by_slot = {e.slot: e for e in submenu_entries}
        
        # Populate entries list with all slots
        for slot in SLOT_ORDER:
            entry = self.entries.add()
            entry.slot = slot
            if slot in entries_by_slot:
                e = entries_by_slot[slot]
                entry.label = e.label
                entry.operator = e.operator
                entry.icon = e.icon
            else:
                entry.label = ""
                entry.operator = ""
                entry.icon = ""

    def reset_to_defaults(self):
        if self.editing_submenu_index == -1:
            # Reset main menu
            self.entries.clear()
            for slot in SLOT_ORDER:
                defaults = DEFAULT_MENU_ENTRIES[slot]
                entry = self.entries.add()
                entry.slot = slot
                entry.label = defaults["label"]
                entry.operator = defaults["operator"]
                entry.icon = defaults["icon"]
            self.save_main_menu_to_storage()
            self.entries_index = 0
        else:
            # Reset current submenu
            menu_id = self.submenus[self.editing_submenu_index].menu_id
            for entry in self.submenu_entries:
                if entry.submenu_id == menu_id:
                    entry.label = ""
                    entry.operator = ""
                    entry.icon = ""
            self.save_submenu_entries(menu_id, self.entries)

    def ensure_defaults(self):
        """Ensure main menu storage has defaults if empty."""
        if len(self.main_menu_storage) == 0:
            # Initialize with defaults
            self.main_menu_storage.clear()
            for slot in SLOT_ORDER:
                defaults = DEFAULT_MENU_ENTRIES[slot]
                stored = self.main_menu_storage.add()
                stored.slot = slot
                stored.label = defaults["label"]
                stored.operator = defaults["operator"]
                stored.icon = defaults["icon"]
        
        # Ensure entries list matches storage when editing main menu
        if self.editing_submenu_index == -1:
            if len(self.entries) != len(SLOT_ORDER):
                self.load_main_menu_from_storage()
            else:
                # Ensure ordering matches SLOT_ORDER
                needs_reorder = any(self.entries[index].slot != slot for index, slot in enumerate(SLOT_ORDER) if index < len(self.entries))
                if needs_reorder:
                    preserved = {entry.slot: (entry.label, entry.operator, entry.icon) for entry in self.entries}
                    self.entries.clear()
                    for slot in SLOT_ORDER:
                        entry = self.entries.add()
                        entry.slot = slot
                        if slot in preserved:
                            entry.label, entry.operator, entry.icon = preserved[slot]
                        else:
                            defaults = DEFAULT_MENU_ENTRIES[slot]
                            entry.label = defaults["label"]
                            entry.operator = defaults["operator"]
                            entry.icon = defaults["icon"]

        if self.entries:
            self.entries_index = max(0, min(self.entries_index, len(self.entries) - 1))
        else:
            self.entries_index = 0

    def sync_entries_list(self):
        """Sync the entries list based on what menu is being edited."""
        if self.editing_submenu_index == -1:
            # Editing main menu - load from storage
            self.load_main_menu_from_storage()
        else:
            # Editing submenu - populate entries from submenu_entries
            if 0 <= self.editing_submenu_index < len(self.submenus):
                menu_id = self.submenus[self.editing_submenu_index].menu_id
                self.load_submenu_entries(menu_id)
            else:
                # Invalid submenu index, clear entries
                self.entries.clear()
                for slot in SLOT_ORDER:
                    entry = self.entries.add()
                    entry.slot = slot
                    entry.label = ""
                    entry.operator = ""
                    entry.icon = ""

    def sync_current_entries(self):
        """Save current entries to the appropriate storage based on editing mode."""
        if self.editing_submenu_index == -1:
            # Save main menu
            self.save_main_menu_to_storage()
        else:
            # Save submenu
            if 0 <= self.editing_submenu_index < len(self.submenus):
                menu_id = self.submenus[self.editing_submenu_index].menu_id
                self.save_submenu_entries(menu_id, self.entries)

    def draw(self, context):
        self.ensure_defaults()
        
        # Sync entries list when opening preferences
        if not self.entries or (self.editing_submenu_index == -1 and len(self.entries) != len(SLOT_ORDER)):
            self.sync_entries_list()

        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        # Hotkey setting (always visible)
        hotkey_row = layout.row()
        hotkey_row.prop(self, "hotkey", text="Hotkey")

        header = layout.row()
        icon = "TRIA_DOWN" if self.show_advanced else "TRIA_RIGHT"
        header.prop(self, "show_advanced", text="", icon=icon, emboss=False)
        header.label(text="Settings (Advanced)")

        if not self.show_advanced:
            return

        advanced = layout.box()

        # Sub-menus section
        box = advanced.box()
        box.label(text="Sub-Menus", icon="MENU_PANEL")
        row = box.row()
        row.template_list(
            "QTPiePreferences_UL_submenus",
            "",
            self,
            "submenus",
            self,
            "submenus_index",
            rows=3,
        )
        col = row.column(align=True)
        col.operator("qtpie.add_submenu", text="", icon="ADD")
        col.operator("qtpie.remove_submenu", text="", icon="REMOVE")

        if 0 <= self.submenus_index < len(self.submenus):
            submenu_item = self.submenus[self.submenus_index]
            box.prop(submenu_item, "name", text="Name")
            op_text = f"view3d.qtpie_open_submenu_{submenu_item.menu_id}"
            box.label(text=f"Operator: {op_text}", icon="FILE_TEXT")
            
            if self.editing_submenu_index != self.submenus_index:
                op = box.operator("qtpie.edit_submenu", text=f"Edit {submenu_item.name}", icon="GREASEPENCIL")
                op.index = self.submenus_index

        # Current menu editing section
        box = advanced.box()
        row = box.row()
        if self.editing_submenu_index == -1:
            hotkey_display = _get_hotkey_display_name(self.hotkey)
            row.label(text=f"Editing: Main Menu ({hotkey_display})", icon="MENU_PANEL")
        elif 0 <= self.editing_submenu_index < len(self.submenus):
            row.label(text=f"Editing: {self.submenus[self.editing_submenu_index].name}", icon="EDITMODE_HLT")
            row.operator("qtpie.edit_main_menu", text="Back to Main Menu", icon="BACK")

        info_box = box.box()
        info_box.label(text="Select a slice to edit its label, operator, and optional icon.")
        info_box.label(text="Operators use category.operator syntax; clear the operator to hide the slice.")

        row = box.row()
        row.template_list(
            "QTPiePreferences_UL_entries",
            "",
            self,
            "entries",
            self,
            "entries_index",
            rows=8,
        )
        col = row.column(align=True)
        col.operator("qtpie.reset_entries", text="", icon="RECOVER_LAST")
        col.operator("qtpie.clear_entry", text="", icon="X")

        if not self.entries:
            return

        entry = self.entries[self.entries_index]
        entry_box = box.box()
        slot_row = entry_box.row()
        slot_row.enabled = False
        slot_row.prop(entry, "slot", text="Slice")
        entry_box.prop(entry, "label")
        entry_box.prop(entry, "operator")
        icon_row = entry_box.row()
        icon_row.prop(entry, "icon")
        icon_row.operator("qtpie.open_icon_docs", text="Browse Icons", icon="URL")


def _operator_exists(operator_id):
    if not operator_id or "." not in operator_id:
        return False
    category, name = operator_id.split(".", 1)
    container = getattr(bpy.ops, category, None)
    return bool(container and hasattr(container, name))


def _invoke_pie_operator(pie, operator_id, text, icon="NONE", *, context_override=None, properties=None, depress=False):
    icon_name = icon or "NONE"
    if not operator_id:
        pie.separator()
        return None
    if not _operator_exists(operator_id):
        pie.label(text=f"Missing operator: {operator_id}")
        return None

    prev_context = pie.operator_context
    if context_override:
        pie.operator_context = context_override
    try:
        op = pie.operator(operator_id, text=text, icon=icon_name, depress=depress)
        if properties:
            for attr, value in properties.items():
                try:
                    setattr(op, attr, value)
                except AttributeError:
                    pass
        return op
    except Exception:
        pie.label(text=f"Failed to add: {operator_id}")
        return None
    finally:
        if context_override:
            pie.operator_context = prev_context


# --------------------------- Pivot helpers ------------------------------------

def _find_pivot_owner_and_prop(context):
    """Return (owner, prop_name) where pivot is stored for the *current editor*.

    Many editors keep their own pivot setting on space_data (e.g. Graph/Image/Clip/VSE),
    while 3D View uses tool_settings.transform_pivot_point. This function finds the
    most specific property to modify for the active area.
    """
    sd = getattr(context, "space_data", None)

    # Prefer per-editor setting when available
    if sd and hasattr(sd, "pivot_point"):
        return sd, "pivot_point"
    if sd and hasattr(sd, "transform_pivot_point"):
        # Some editors expose this naming
        return sd, "transform_pivot_point"

    # Fallback to global/tool_settings (3D View & generic fallback)
    ts = context.tool_settings
    return ts, "transform_pivot_point"


def _enum_items_for(owner, prop_name):
    try:
        return [it.identifier for it in owner.bl_rna.properties[prop_name].enum_items]
    except Exception:
        return []


def _icon_for_identifier(ident):
    return {
        "CURSOR": "PIVOT_CURSOR",
        "INDIVIDUAL_ORIGINS": "PIVOT_INDIVIDUAL",
        "INDIVIDUAL_CENTER": "PIVOT_INDIVIDUAL",
        "INDIVIDUAL_CENTERS": "PIVOT_INDIVIDUAL",
        "MEDIAN_POINT": "PIVOT_MEDIAN",
        "BOUNDING_BOX_CENTER": "PIVOT_BOUNDBOX",
    }.get(ident, "PIVOT_MEDIAN")


def _label_for_identifier(area_type, ident):
    if ident == "CURSOR":
        return "Pivot: 3D Cursor" if area_type == "VIEW_3D" else "Pivot: 2D Cursor"
    if ident in {"INDIVIDUAL_ORIGINS", "INDIVIDUAL_CENTER", "INDIVIDUAL_CENTERS"}:
        return "Pivot: Individual Origins" if area_type == "VIEW_3D" else "Pivot: Individual Centers"
    if ident == "MEDIAN_POINT":
        return "Pivot: Median Point"
    if ident == "BOUNDING_BOX_CENTER":
        return "Pivot: Bounding Box Center"
    # Fallback – show the raw identifier (unlikely to surface)
    return f"Pivot: {ident.replace('_', ' ').title()}"


def _choose_identifiers(area_type, supported_idents):
    """Pick three identifiers (E, S, N slots) that make sense for the current editor.

    Preference strategy:
      - E (Right): Cursor (2D/3D)
      - S (Down): Individual (Origins/Centers)
      - N (Up): Median Point; if not present, use Bounding Box Center
    """
    def pick(preferred):
        for p in preferred:
            if p in supported_idents:
                return p
        # last resort – pick *something* if the list isn't empty
        return supported_idents[0] if supported_idents else None

    e_ident = pick(["CURSOR"])
    s_ident = pick(["INDIVIDUAL_ORIGINS", "INDIVIDUAL_CENTERS", "INDIVIDUAL_CENTER"])
    n_ident = pick(["MEDIAN_POINT", "BOUNDING_BOX_CENTER"])
    return e_ident, s_ident, n_ident


# --- Helper: toggle proportional editing (object & edit) ----------------------
class VIEW3D_OT_toggle_proportional_edit_smart(bpy.types.Operator):
    bl_idname = "view3d.toggle_proportional_edit_smart"
    bl_label = "Toggle Proportional Editing"
    bl_description = "Enable/disable Proportional Editing (auto-detects Object/Edit mode)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ts = context.tool_settings
        mode = context.mode

        if mode == 'OBJECT':
            # Object mode has its own boolean flag
            current = bool(getattr(ts, "use_proportional_edit_objects", False))
            ts.use_proportional_edit_objects = not current
            return {'FINISHED'}

        # Edit modes: Blender 4.5 uses 'use_proportional_edit' (bool).
        # Older builds exposed 'proportional_edit' (enum).
        if hasattr(ts, "use_proportional_edit"):
            ts.use_proportional_edit = not bool(getattr(ts, "use_proportional_edit", False))
            return {'FINISHED'}

        # Fallback for older enum-based API (kept for compatibility)
        pe = getattr(ts, "proportional_edit", None)
        if pe is not None:
            ts.proportional_edit = 'DISABLED' if pe != 'DISABLED' else 'ENABLED'
            return {'FINISHED'}

        # Ultimate fallback: let Blender handle it
        try:
            bpy.ops.transform.proportional_edit_toggle()
        except Exception:
            return {'CANCELLED'}
        return {'FINISHED'}


# --- Helper: delayed render operators (to avoid 'sticky' behavior) -----------
class VIEW3D_OT_qtpie_render_image(bpy.types.Operator):
    bl_idname = "view3d.qtpie_render_image"
    bl_label = "Render Image"
    bl_description = "Render the current frame (opens the Render window)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        def _delayed():
            try:
                bpy.ops.render.render('INVOKE_DEFAULT')
            except Exception:
                pass
            return None
        bpy.app.timers.register(_delayed, first_interval=0.0)
        return {'FINISHED'}


class VIEW3D_OT_qtpie_view_render(bpy.types.Operator):
    bl_idname = "view3d.qtpie_view_render"
    bl_label = "View Render"
    bl_description = "Show the most recent render result"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        def _delayed():
            try:
                bpy.ops.render.view_show('INVOKE_DEFAULT')
            except Exception:
                pass
            return None
        bpy.app.timers.register(_delayed, first_interval=0.0)
        return {'FINISHED'}


# --- Wrapper operators to provide meaningful tooltips -------------------------
class VIEW3D_OT_qtpie_parent_set_object(bpy.types.Operator):
    bl_idname = "view3d.qtpie_parent_set_object"
    bl_label = "Set Parent to Object"
    bl_description = "Parent selected objects to the active object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        except Exception:
            return {'CANCELLED'}
        return {'FINISHED'}


class VIEW3D_OT_qtpie_insert_keys(bpy.types.Operator):
    bl_idname = "view3d.qtpie_insert_keys"
    bl_label = "Insert Keys"
    bl_description = "Insert keyframes using current keying settings"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            bpy.ops.anim.keyframe_insert()
        except Exception:
            return {'CANCELLED'}
        return {'FINISHED'}


class VIEW3D_OT_qtpie_set_pivot(bpy.types.Operator):
    bl_idname = "view3d.qtpie_set_pivot"
    bl_label = "Set Pivot"
    bl_options = {"INTERNAL"}

    # IMPORTANT: value must be a *real* RNA enum identifier that exists
    # on the target pivot property for the current editor (e.g. CURSOR,
    # MEDIAN_POINT, INDIVIDUAL_CENTERS, BOUNDING_BOX_CENTER, ...).
    value: bpy.props.StringProperty(
        name="Pivot Identifier",
        options={'HIDDEN'}
    )

    @classmethod
    def description(cls, context, props):
        ident = getattr(props, "value", "")
        area_type = getattr(getattr(context, "area", None), "type", "VIEW_3D")
        return _label_for_identifier(area_type, ident)

    def execute(self, context):
        owner, prop_name = _find_pivot_owner_and_prop(context)
        try:
            setattr(owner, prop_name, self.value)
        except Exception:
            return {'CANCELLED'}
        return {'FINISHED'}


def draw_pie_menu(context, pie, entries, menu_id=0):
    """Draw a pie menu based on entries. Only shows entries that have operators set."""
    def entry_data(slot):
        entry = entries.get(slot)
        if entry and entry.operator and entry.operator.strip():
            label = (entry.label or "").strip()
            operator_id = entry.operator.strip()
            icon = (entry.icon or "").strip()
            return entry, label, operator_id, icon
        return None, "", "", ""

    mode = context.mode
    is_object = (mode == "OBJECT")
    is_edit = mode.startswith("EDIT")

    owner, prop_name = _find_pivot_owner_and_prop(context)
    supported = _enum_items_for(owner, prop_name)
    current_value = getattr(owner, prop_name, "MEDIAN_POINT")
    area_type = getattr(getattr(context, "area", None), "type", "VIEW_3D")

    ident_e, ident_s, ident_n = _choose_identifiers(area_type, supported)

    ts = context.tool_settings
    if is_object:
        prop_on = bool(getattr(ts, "use_proportional_edit_objects", False))
    elif is_edit:
        if hasattr(ts, "use_proportional_edit"):
            prop_on = bool(getattr(ts, "use_proportional_edit", False))
        else:
            prop_on = getattr(ts, "proportional_edit", "DISABLED") != "DISABLED"
    else:
        prop_on = False

    # Process each slot in order: W, E, S, N, NW, NE, SW, SE
    for slot in SLOT_ORDER:
        entry, label, operator_id, icon = entry_data(slot)
        
        # Skip if no operator defined
        if not operator_id:
            pie.separator()
            continue

        # Special handling for specific operators
        if slot == "W" and operator_id == "view3d.qtpie_parent_set_object":
            if is_object:
                _invoke_pie_operator(
                    pie, operator_id, label, icon, context_override="EXEC_DEFAULT"
                )
            else:
                pie.separator()
        
        elif slot == "E" and operator_id == "view3d.qtpie_set_pivot":
            if ident_e:
                display_label = label if label else _label_for_identifier(area_type, ident_e)
                display_icon = icon or _icon_for_identifier(ident_e)
                _invoke_pie_operator(
                    pie,
                    operator_id,
                    display_label,
                    display_icon,
                    properties={"value": ident_e},
                    depress=(current_value == ident_e),
                )
            else:
                pie.separator()
        
        elif slot == "S" and operator_id == "view3d.qtpie_set_pivot":
            if ident_s:
                display_label = label if label else _label_for_identifier(area_type, ident_s)
                display_icon = icon or _icon_for_identifier(ident_s)
                _invoke_pie_operator(
                    pie,
                    operator_id,
                    display_label,
                    display_icon,
                    properties={"value": ident_s},
                    depress=(current_value == ident_s),
                )
            else:
                pie.separator()
        
        elif slot == "N" and operator_id == "view3d.qtpie_set_pivot":
            if ident_n:
                display_label = label if label else _label_for_identifier(area_type, ident_n)
                display_icon = icon or _icon_for_identifier(ident_n)
                _invoke_pie_operator(
                    pie,
                    operator_id,
                    display_label,
                    display_icon,
                    properties={"value": ident_n},
                    depress=(current_value == ident_n),
                )
            else:
                pie.separator()
        
        elif slot == "NE" and operator_id == "view3d.toggle_proportional_edit_smart":
            if is_object or is_edit:
                _invoke_pie_operator(
                    pie, operator_id, label, icon, depress=prop_on
                )
            else:
                pie.separator()
        
        elif slot == "SE" and operator_id == "view3d.qtpie_insert_keys":
            if is_object:
                _invoke_pie_operator(
                    pie, operator_id, label, icon, context_override="EXEC_DEFAULT"
                )
            else:
                pie.separator()
        
        else:
            # Generic operator call
            _invoke_pie_operator(pie, operator_id, label, icon)


# --- The pie menu (Object layout preserved; other modes use separators) -------
class VIEW3D_MT_qtpie_menu(bpy.types.Menu):
    bl_label = "QT-Pie Menu"
    bl_idname = "VIEW3D_MT_qtpie_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        pie = layout.menu_pie()

        prefs = get_addon_preferences(context)
        entries_by_slot = {}
        if prefs:
            # Always use main menu storage for the main pie menu
            for stored in prefs.main_menu_storage:
                if stored.slot and stored.slot not in entries_by_slot:
                    # Create a temporary entry-like object
                    class Entry:
                        pass
                    entry = Entry()
                    entry.slot = stored.slot
                    entry.label = stored.label
                    entry.operator = stored.operator
                    entry.icon = stored.icon
                    entries_by_slot[stored.slot] = entry

        draw_pie_menu(context, pie, entries_by_slot, menu_id=0)


# Dynamic sub-menu class generator
def create_submenu_class(menu_id):
    """Create a dynamic pie menu class for a sub-menu."""
    class DynamicSubMenu(bpy.types.Menu):
        bl_label = f"QT-Pie Sub Menu {menu_id}"
        bl_idname = f"VIEW3D_MT_qtpie_submenu_{menu_id}"
        
        def draw(self, context):
            layout = self.layout
            layout.operator_context = "INVOKE_DEFAULT"
            pie = layout.menu_pie()
            
            prefs = get_addon_preferences(context)
            entries_by_slot = {}
            if prefs:
                for entry in prefs.submenu_entries:
                    if entry.submenu_id == menu_id and entry.slot and entry.slot not in entries_by_slot:
                        entries_by_slot[entry.slot] = entry
            
            draw_pie_menu(context, pie, entries_by_slot, menu_id=menu_id)
            
            # Fallback if menu not found
            if not entries_by_slot:
                for _ in range(8):
                    pie.separator()
    
    DynamicSubMenu.__name__ = f"VIEW3D_MT_qtpie_submenu_{menu_id}"
    return DynamicSubMenu


# Dynamic sub-menu operator generator
def create_submenu_operator(menu_id):
    """Create a dynamic operator class for opening a sub-menu."""
    class DynamicSubMenuOperator(bpy.types.Operator):
        bl_idname = f"view3d.qtpie_open_submenu_{menu_id}"
        bl_label = f"Open Sub-Menu {menu_id}"
        bl_description = f"Open QT-Pie sub-menu {menu_id}"
        bl_options = {"REGISTER", "UNDO"}
        
        def execute(self, context):
            menu_name = f"VIEW3D_MT_qtpie_submenu_{menu_id}"
            try:
                bpy.ops.wm.call_menu_pie(name=menu_name)
            except Exception:
                self.report({'ERROR'}, f"QT-Pie: Failed to open menu: {menu_name}")
                return {'CANCELLED'}
            return {'FINISHED'}
    
    DynamicSubMenuOperator.__name__ = f"VIEW3D_OT_qtpie_open_submenu_{menu_id}"
    return DynamicSubMenuOperator


# Store dynamically created classes
_registered_submenu_classes = []
_registered_submenu_operators = []


def register_submenu_classes():
    """Register all sub-menu classes based on preferences."""
    unregister_submenu_classes()
    
    prefs = get_addon_preferences(ensure_defaults=False)
    if not prefs:
        return
    
    for submenu in prefs.submenus:
        menu_id = submenu.menu_id
        menu_cls = create_submenu_class(menu_id)
        try:
            bpy.utils.register_class(menu_cls)
            _registered_submenu_classes.append(menu_cls)
        except Exception:
            pass


def unregister_submenu_classes():
    """Unregister all dynamically created sub-menu classes."""
    for menu_cls in _registered_submenu_classes:
        try:
            bpy.utils.unregister_class(menu_cls)
        except Exception:
            pass
    _registered_submenu_classes.clear()


def register_submenu_operators():
    """Register all sub-menu operator classes based on preferences."""
    unregister_submenu_operators()
    
    prefs = get_addon_preferences(ensure_defaults=False)
    if not prefs:
        return
    
    for submenu in prefs.submenus:
        operator_cls = create_submenu_operator(submenu.menu_id)
        try:
            bpy.utils.register_class(operator_cls)
            _registered_submenu_operators.append(operator_cls)
        except Exception:
            pass


def unregister_submenu_operators():
    """Unregister all dynamically created sub-menu operator classes."""
    for op_cls in _registered_submenu_operators:
        try:
            bpy.utils.unregister_class(op_cls)
        except Exception:
            pass
    _registered_submenu_operators.clear()


# --- Keymap handling: Q across Blender (unchanged) ----------------------------
addon_keymaps = []
SPACE_KEYMAPS = [
    ("Window", 'EMPTY'),
]

classes = (
    QTPieMenuEntry,
    QTPieSubMenu,
    QTPieSubMenuEntry,
    QTPieMainMenuStorage,
    QTPiePreferences_UL_entries,
    QTPiePreferences_UL_submenus,
    QTPiePreferences_OT_reset_entries,
    QTPiePreferences_OT_clear_entry,
    QTPiePreferences_OT_add_submenu,
    QTPiePreferences_OT_remove_submenu,
    QTPiePreferences_OT_edit_main_menu,
    QTPiePreferences_OT_edit_submenu,
    QTPiePreferences_OT_open_icon_docs,
    QTPieAddonPreferences,
    VIEW3D_OT_toggle_proportional_edit_smart,
    VIEW3D_OT_qtpie_render_image,
    VIEW3D_OT_qtpie_view_render,
    VIEW3D_OT_qtpie_parent_set_object,
    VIEW3D_OT_qtpie_insert_keys,
    VIEW3D_OT_qtpie_set_pivot,
    VIEW3D_MT_qtpie_menu,
)


def _add_keymap(kc, name, space_type):
    try:
        if addon_keymaps:
            return
        prefs = get_addon_preferences(ensure_defaults=False)
        hotkey = prefs.hotkey if prefs else 'Q'
        km = kc.keymaps.new(name=name, space_type=space_type)
        kmi = km.keymap_items.new("wm.call_menu_pie", hotkey, 'PRESS')
        kmi.properties.name = "VIEW3D_MT_qtpie_menu"
        kmi.repeat = True
        addon_keymaps.append((km, kmi))
    except Exception:
        pass


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prefs = get_addon_preferences()
    if prefs:
        # Ensure defaults are initialized on first load
        prefs.ensure_defaults()
        # Make sure entries list is synced
        if prefs.editing_submenu_index == -1:
            prefs.sync_entries_list()

    register_submenu_classes()
    register_submenu_operators()

    wm = getattr(bpy.context, "window_manager", None)
    kc = wm.keyconfigs.addon if wm else None
    if kc:
        for name, space in SPACE_KEYMAPS:
            _add_keymap(kc, name, space)


def unregister():
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except Exception:
            pass
    addon_keymaps.clear()

    unregister_submenu_classes()
    unregister_submenu_operators()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
