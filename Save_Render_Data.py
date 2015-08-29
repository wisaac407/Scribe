import bpy, os, time, random
from bpy.app.handlers import persistent

SCRIPT_ID = "render%s" % random.random()

FORMAT = """
Frames: %(nframes)s(%(fstart)s-%(fend)s)
Total Time: %(time).2fs
Average Time: %(average_time).2fs per frame

Resolution: %(res_x)sx%(res_y)spx(%(res_percent)s%%)
True Resolution: %(true_res_x)sx%(true_res_y)spx

Seed: %(seed)s
Is seed animated: %(animated_seed)s

Samples: %(samples)s
Square Samples: %(square_samples)s

Tile Size: %(tile_x)sx%(tile_y)s
""".strip()


def cleanup(scene):
    """Remove any intermediate props stored on the scene."""

    # Loop through all the scene custom props deleting the ones that we set.
    for key in scene.keys():
        if key.startswith(SCRIPT_ID): del scene[key]


@persistent
def render_write(scene):
    # If we are writing a file then we should be writing the stats also.
    scene[SCRIPT_ID + 'written'] = True


@persistent
def render_cancel(scene):
    """Just cleanup the scene because rendering was canceled."""
    cleanup(scene)


@persistent
def render_init(scene):
    """Initialize the intermediate props set on the scene."""
    scene[SCRIPT_ID + 'time'] = time.time()  # For logging the total rendering time.
    scene[SCRIPT_ID + 'written'] = False  # Weather or the any files have been written to disk.


@persistent
def render_complete(scene):
    # If we haven't written any files then we shouldn't write our stats.
    if not scene[SCRIPT_ID + 'written']:
        cleanup(scene)
        return
    # Get the file paths.
    render_dir = bpy.path.abspath(scene.render.filepath)
    path = os.path.join(render_dir, 'render_settings.txt')

    # ## Collect all the data.

    # Total render time
    t = time.time() - scene[SCRIPT_ID + 'time']

    # Frames
    frame_start = scene.frame_start
    frame_end = scene.frame_end
    nframes = frame_end - (frame_start - 1)
    average_time = t / nframes

    # Resolution
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    res_percent = scene.render.resolution_percentage

    true_res_x = res_x * (res_percent / 100)
    true_res_y = res_y * (res_percent / 100)

    # Seed
    seed = scene.cycles.seed
    animated_seed = scene.cycles.use_animated_seed

    # Samples
    samples = scene.cycles.samples
    square_samples = scene.cycles.use_square_samples

    # Tile size
    tile_x = scene.render.tile_x
    tile_y = scene.render.tile_y

    ### Format the data
    s = FORMAT % {
        'time': t,
        'fstart': frame_start,
        'fend': frame_end,
        'nframes': nframes,
        'average_time': average_time,
        'res_x': res_x,
        'res_y': res_y,
        'res_percent': res_percent,
        'true_res_x': true_res_x,
        'true_res_y': true_res_y,
        'seed': seed,
        'animated_seed': animated_seed,
        'samples': samples,
        'square_samples': square_samples,
        'tile_x': tile_x,
        'tile_y': tile_y
    }
    print(s)

    # Cleanup the custom props on the scene.
    cleanup(scene)

    ### Write the data to the info file.
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

    def pre_hook(self, context):
        pass

    def post_hook(self, context):
        # Every instance should implement this function.
        raise NotImplementedError


class TimeHook(SettingsHook):
    hook_label = 'Time'
    hook_idname = 'time'

    t = 0

    def pre_hook(self, context):
        self.t = time.time()

    def post_hook(self, context):
        return '%.2fs' % (time.time() - self.t)

register_hook(TimeHook)


class ResolutionHook(SettingsHook):
    hook_label = 'Resolution'
    hook_idname = 'resolution'

    def post_hook(self, context):
        x = context.scene.render.resolution_x
        y = context.scene.render.resolution_y
        return "%sx%s" % (x, y)

register_hook(ResolutionHook)


class SeedHook(SettingsHook):
    hook_label = 'Seed'
    hook_idname = 'seed'

    def post_hook(self, context):
        return str(context.scene.cycles.seed)

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
        layout.label('Hello World!')


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
    ## END DEBUG CODE ##

    # Remove handlers
    #bpy.app.handlers.render_write.remove(render_write)
    #bpy.app.handlers.render_cancel.remove(render_cancel)
    #bpy.app.handlers.render_init.remove(render_init)
    #bpy.app.handlers.render_complete.remove(render_complete)


if __name__ == "__main__":
    try:
        unregister()
    finally:
        register()