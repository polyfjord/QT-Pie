bl_info = {
     "name": "Quick Trigger Pie Menu",
     "author": "Polyfjord",
     "version": (1, 1, 0),
     "blender": (4, 5, 0),
     "location": "Everywhere",
     "description": "Easier access to impractical hotkeys.",
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


def get_addon_preferences(context=None):
    ctx = context or bpy.context
    for name in _module_name_candidates():
        addon = ctx.preferences.addons.get(name)
        if addon:
            prefs = addon.preferences
            ensure = getattr(prefs, "ensure_defaults", None)
            if ensure:
                ensure()
            return prefs
    return None


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


class QTPiePreferences_UL_entries(bpy.types.UIList):
    bl_idname = "QTPiePreferences_UL_entries"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            split = layout.split(factor=0.2)
            arrow = ARROW_LABELS.get(item.slot, item.slot or "?")
            split.label(text=arrow)
            split.label(text=item.label or DEFAULT_MENU_ENTRIES.get(item.slot, {}).get("label", ""))
        elif self.layout_type == "GRID":
            layout.alignment = 'CENTER'
            arrow = ARROW_LABELS.get(item.slot, item.slot or "?")
            layout.label(text=arrow)


class QTPiePreferences_OT_reset_entries(bpy.types.Operator):
    bl_idname = "qtpie.reset_entries"
    bl_label = "Reset Pie Entries"
    bl_description = "Restore the original entries."
    bl_options = {"INTERNAL"}

    def execute(self, context):
        prefs = get_addon_preferences(context)
        if not prefs:
            self.report({'WARNING'}, "QT-Pie preferences not available")
            return {'CANCELLED'}
        prefs.reset_to_defaults()
        self.report({'INFO'}, "QT-Pie pie menu entries reset")
        return {'FINISHED'}


class QTPieAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    show_advanced: BoolProperty(
        name="Settings (Advanced)",
        description="Show or hide advanced pie menu customization options",
        default=False,
    )
    entries: CollectionProperty(type=QTPieMenuEntry)
    entries_index: IntProperty(default=0)

    def reset_to_defaults(self):
        self.entries.clear()
        for slot in SLOT_ORDER:
            defaults = DEFAULT_MENU_ENTRIES[slot]
            entry = self.entries.add()
            entry.slot = slot
            entry.label = defaults["label"]
            entry.operator = defaults["operator"]
            entry.icon = defaults["icon"]
        self.entries_index = 0

    def ensure_defaults(self):
        if len(self.entries) != len(SLOT_ORDER) or any(entry.slot not in SLOT_ORDER for entry in self.entries):
            preserved = {entry.slot: (entry.label, entry.operator, entry.icon) for entry in self.entries if entry.slot in SLOT_ORDER}
            self.entries.clear()
            for slot in SLOT_ORDER:
                defaults = DEFAULT_MENU_ENTRIES[slot]
                label, operator, icon = preserved.get(slot, (defaults["label"], defaults["operator"], defaults["icon"]))
                entry = self.entries.add()
                entry.slot = slot
                entry.label = label
                entry.operator = operator
                entry.icon = icon
        else:
            # ensure ordering matches SLOT_ORDER while preserving current data
            needs_reorder = any(self.entries[index].slot != slot for index, slot in enumerate(SLOT_ORDER) if index < len(self.entries))
            if needs_reorder:
                preserved = {entry.slot: (entry.label, entry.operator, entry.icon) for entry in self.entries}
                self.entries.clear()
                for slot in SLOT_ORDER:
                    defaults = DEFAULT_MENU_ENTRIES[slot]
                    label, operator, icon = preserved.get(slot, (defaults["label"], defaults["operator"], defaults["icon"]))
                    entry = self.entries.add()
                    entry.slot = slot
                    entry.label = label
                    entry.operator = operator
                    entry.icon = icon

        if self.entries:
            self.entries_index = max(0, min(self.entries_index, len(self.entries) - 1))
        else:
            self.entries_index = 0

    def draw(self, context):
        self.ensure_defaults()

        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        header = layout.row()
        icon = "TRIA_DOWN" if self.show_advanced else "TRIA_RIGHT"
        header.prop(self, "show_advanced", text="", icon=icon, emboss=False)
        header.label(text="Settings (Advanced)")

        if not self.show_advanced:
            return

        advanced = layout.box()

        info_box = advanced.box()
        info_box.label(text="Select a slice to edit its label, operator, and optional icon.")
        info_box.label(text="Operators use category.operator syntax; clear the operator to hide the slice.")

        row = advanced.row()
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

        if not self.entries:
            return

        entry = self.entries[self.entries_index]
        entry_box = advanced.box()
        slot_row = entry_box.row()
        slot_row.enabled = False
        slot_row.prop(entry, "slot", text="Slice")
        entry_box.prop(entry, "label")
        entry_box.prop(entry, "operator")
        entry_box.prop(entry, "icon")


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


# --- The pie menu (Object layout preserved; other modes use separators) -------
class VIEW3D_MT_custom_q_pie(bpy.types.Menu):
    bl_label = "Quick Trigger Pie Menu"
    bl_idname = "VIEW3D_MT_custom_q_pie"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        pie = layout.menu_pie()  # Order: W, E, S, N, NW, NE, SW, SE

        prefs = get_addon_preferences(context)
        entries_by_slot = {}
        if prefs:
            for entry in prefs.entries:
                if entry.slot and entry.slot not in entries_by_slot:
                    entries_by_slot[entry.slot] = entry

        def entry_data(slot):
            entry = entries_by_slot.get(slot)
            defaults = DEFAULT_MENU_ENTRIES[slot]
            if entry:
                label = (entry.label or "").strip() or defaults["label"]
                operator_id = (entry.operator or "").strip()
                icon = (entry.icon or "").strip()
            else:
                label = defaults["label"]
                operator_id = defaults["operator"]
                icon = defaults["icon"]
            return entry, label, operator_id, icon

        mode = context.mode
        is_object = (mode == "OBJECT")
        is_edit = mode.startswith("EDIT")  # EDIT_MESH/EDIT_CURVE/.../EDIT_GPENCIL

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

        # Slot W (Left)
        entry_w, label_w, operator_w, icon_w = entry_data("W")
        show_w = operator_w and (is_object or operator_w != "view3d.qtpie_parent_set_object")
        if show_w:
            context_override = "EXEC_DEFAULT" if operator_w == "view3d.qtpie_parent_set_object" else None
            _invoke_pie_operator(pie, operator_w, label_w, icon_w, context_override=context_override)
        else:
            pie.separator()  # keep slot

        # Slot E (Right)
        entry_e, label_e, operator_e, icon_e = entry_data("E")
        if operator_e == "view3d.qtpie_set_pivot":
            if ident_e:
                display_label = label_e if (entry_e and (entry_e.label or "").strip()) else _label_for_identifier(area_type, ident_e)
                display_icon = icon_e or _icon_for_identifier(ident_e)
                _invoke_pie_operator(
                    pie,
                    operator_e,
                    display_label,
                    display_icon,
                    properties={"value": ident_e},
                    depress=(current_value == ident_e),
                )
            else:
                pie.separator()
        elif operator_e:
            _invoke_pie_operator(pie, operator_e, label_e, icon_e)
        else:
            pie.separator()

        # Slot S (Down)
        entry_s, label_s, operator_s, icon_s = entry_data("S")
        if operator_s == "view3d.qtpie_set_pivot":
            if ident_s:
                display_label = label_s if (entry_s and (entry_s.label or "").strip()) else _label_for_identifier(area_type, ident_s)
                display_icon = icon_s or _icon_for_identifier(ident_s)
                _invoke_pie_operator(
                    pie,
                    operator_s,
                    display_label,
                    display_icon,
                    properties={"value": ident_s},
                    depress=(current_value == ident_s),
                )
            else:
                pie.separator()
        elif operator_s:
            _invoke_pie_operator(pie, operator_s, label_s, icon_s)
        else:
            pie.separator()

        # Slot N (Up)
        entry_n, label_n, operator_n, icon_n = entry_data("N")
        if operator_n == "view3d.qtpie_set_pivot":
            if ident_n:
                display_label = label_n if (entry_n and (entry_n.label or "").strip()) else _label_for_identifier(area_type, ident_n)
                display_icon = icon_n or _icon_for_identifier(ident_n)
                _invoke_pie_operator(
                    pie,
                    operator_n,
                    display_label,
                    display_icon,
                    properties={"value": ident_n},
                    depress=(current_value == ident_n),
                )
            else:
                pie.separator()
        elif operator_n:
            _invoke_pie_operator(pie, operator_n, label_n, icon_n)
        else:
            pie.separator()

        # Slot NW (Up-Left)
        entry_nw, label_nw, operator_nw, icon_nw = entry_data("NW")
        if operator_nw:
            _invoke_pie_operator(pie, operator_nw, label_nw, icon_nw)
        else:
            pie.separator()

        # Slot NE (Up-Right)
        entry_ne, label_ne, operator_ne, icon_ne = entry_data("NE")
        show_ne = (is_object or is_edit) or (operator_ne and operator_ne != "view3d.toggle_proportional_edit_smart")
        if operator_ne and show_ne:
            use_depress = (operator_ne == "view3d.toggle_proportional_edit_smart") and prop_on
            _invoke_pie_operator(pie, operator_ne, label_ne, icon_ne, depress=use_depress)
        else:
            pie.separator()  # keep slot

        # Slot SW (Down-Left)
        entry_sw, label_sw, operator_sw, icon_sw = entry_data("SW")
        if operator_sw:
            _invoke_pie_operator(pie, operator_sw, label_sw, icon_sw)
        else:
            pie.separator()

        # Slot SE (Down-Right)
        entry_se, label_se, operator_se, icon_se = entry_data("SE")
        show_se = operator_se and (is_object or operator_se != "view3d.qtpie_insert_keys")
        if show_se:
            context_override = "EXEC_DEFAULT" if operator_se == "view3d.qtpie_insert_keys" else None
            _invoke_pie_operator(pie, operator_se, label_se, icon_se, context_override=context_override)
        else:
            pie.separator()  # keep slot



# --- Keymap handling: Q across Blender (unchanged) ----------------------------
addon_keymaps = []
SPACE_KEYMAPS = [
    ("Window", 'EMPTY'),
]

classes = (
    QTPieMenuEntry,
    QTPiePreferences_UL_entries,
    QTPiePreferences_OT_reset_entries,
    QTPieAddonPreferences,
    VIEW3D_OT_toggle_proportional_edit_smart,
    VIEW3D_OT_qtpie_render_image,
    VIEW3D_OT_qtpie_view_render,
    VIEW3D_OT_qtpie_parent_set_object,
    VIEW3D_OT_qtpie_insert_keys,
    VIEW3D_OT_qtpie_set_pivot,
    VIEW3D_MT_custom_q_pie,
)


def _add_keymap(kc, name, space_type):
    try:
        if addon_keymaps:
            return
        km = kc.keymaps.new(name=name, space_type=space_type)
        kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_custom_q_pie"
        kmi.repeat = True
        addon_keymaps.append((km, kmi))
    except Exception:
        pass


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prefs = get_addon_preferences()
    if prefs:
        prefs.ensure_defaults()

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

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
