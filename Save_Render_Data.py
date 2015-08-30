import bpy, os, time
from bpy.app.handlers import persistent


written = False
hooks = []


def format_render_data(hooks):
    s = ""
    for hook in hooks:
        s += hook.hook_template.format(name=hook.hook_label, data=hook.post_hook())
        s += '\n'
    return s


def cleanup(scene):
    """Remove any intermediate props stored on the scene."""

    global written, hooks
    written = False
    hooks = []


@persistent
def render_write(scene):
    # If we are writing a file then we should be writing the stats also.
    global written
    written = True

@persistent
def render_cancel(scene):
    """Just cleanup the scene because rendering was canceled."""
    cleanup(scene)


@persistent
def render_init(scene):
    """Initialize the intermediate props set on the scene."""
    global written, hooks
    written = False
    hooks = []
    # For every active hook, initialize it with the current scene, run the pre_hook function
    # and add it to the list of active hooks list.
    for hook in settings_hooks:
        # Only add it if it's active.
        if getattr(scene.srd_settings, hook.hook_idname):
            hook = hook(scene)
            hook.pre_hook()
            hooks.append(hook)


@persistent
def render_complete(scene):
    # If we haven't written any files then we shouldn't write our stats.
    if not written:
        cleanup(scene)
        return
    # Get the file paths.
    render_dir = bpy.path.abspath(scene.render.filepath)
    path = os.path.join(render_dir, 'render_settings.txt')

    # ## Collect all the data.
    s = format_render_data(hooks)
    print(s)

    # Cleanup the custom props on the scene.
    cleanup(scene)

    # ## Write the data to the info file.
    f = open(path, 'w')
    f.write(s)
    f.close()


class SRDRenderSettings(bpy.types.PropertyGroup):
    enable = bpy.props.BoolProperty(
        description="Save the render data to file at render.",
        name="Save Render Data",
        default=True
    )


settings_hooks = []


def register_hook(hook):
    """Add hook to the list of available hooks and add a bool property to the property group."""
    settings_hooks.append(hook)
    setattr(SRDRenderSettings, hook.hook_idname, bpy.props.BoolProperty(name=hook.hook_label))


class SettingsHook:
    """Base class for all settings hooks"""
    # Really no need for this to be changed in any instances.
    hook_template = '{name}: {data}'
    hook_label = 'Unset'  # Every sub-class should define their own name.
    hook_idname = ''  # This is how other hooks can reference this one.

    def __init__(self, scene):
        self.scene = scene

    def pre_hook(self):
        pass

    def post_hook(self):
        # Every instance should implement this function.
        raise NotImplementedError


class TimeHook(SettingsHook):
    hook_label = 'Time'
    hook_idname = 'time'

    t = 0

    def pre_hook(self):
        self.t = time.time()

    def post_hook(self):
        return '%.2fs' % (time.time() - self.t)


register_hook(TimeHook)


class ResolutionHook(SettingsHook):
    hook_label = 'Resolution'
    hook_idname = 'resolution'

    def post_hook(self):
        x = self.scene.render.resolution_x
        y = self.scene.render.resolution_y
        return "%sx%s" % (x, y)


register_hook(ResolutionHook)


class SeedHook(SettingsHook):
    hook_label = 'Seed'
    hook_idname = 'seed'

    def post_hook(self):
        return str(self.scene.cycles.seed)


register_hook(SeedHook)


class SRDRenderPanel(bpy.types.Panel):
    """Puts the panel in the render data section."""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_idname = 'RENDER_PT_SRD'
    bl_label = "Save Render Data"

    def draw_header(self, context):
        self.layout.prop(context.scene.srd_settings, "enable", text="")

    def draw(self, context):
        layout = self.layout
        layout.active = context.scene.srd_settings.enable
        for hook in settings_hooks:
            layout.prop(context.scene.srd_settings, hook.hook_idname)


def register():
    # Add handlers
    bpy.app.handlers.render_write.append(render_write)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_complete.append(render_complete)

    bpy.utils.register_class(SRDRenderPanel)
    bpy.utils.register_class(SRDRenderSettings)

    bpy.types.Scene.srd_settings = \
        bpy.props.PointerProperty(type=SRDRenderSettings)


def unregister():
    # # BEGIN DEBUG CODE ##
    bpy.app.handlers.render_write.pop()
    bpy.app.handlers.render_cancel.pop()
    bpy.app.handlers.render_init.pop()
    bpy.app.handlers.render_complete.pop()
    # # END DEBUG CODE ##

    # Remove handlers
    # bpy.app.handlers.render_write.remove(render_write)
    # bpy.app.handlers.render_cancel.remove(render_cancel)
    # bpy.app.handlers.render_init.remove(render_init)
    # bpy.app.handlers.render_complete.remove(render_complete)


if __name__ == "__main__":
    try:
        unregister()
    finally:
        register()