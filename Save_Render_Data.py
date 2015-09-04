import bpy, os, time
from bpy.app.handlers import persistent


srd_renderer = None


def cleanup(scene):
    """Remove any intermediate props stored on the scene."""
    global srd_renderer
    srd_renderer = None


@persistent
def render_write(scene):
    # If we are writing a file then we should be writing the stats also.
    srd_renderer.can_render = True

@persistent
def render_cancel(scene):
    """Just cleanup the scene because rendering was canceled."""
    cleanup(scene)

@persistent
def render_init(scene):
    """Initialize the intermediate props set on the scene."""
    global srd_renderer
    srd_renderer = SRDRenderer(scene)

@persistent
def render_complete(scene):
    # If we haven't written any files then we shouldn't write our stats.
    srd_renderer.render()
    cleanup(scene)

@persistent
def render_pre(scene):
    srd_renderer.frame_begin()

@persistent
def render_post(scene):
    srd_renderer.frame_complete()


class SRDRenderSettings(bpy.types.PropertyGroup):
    enable = bpy.props.BoolProperty(
        description="Save the render data to file at render.",
        name="Save Render Data",
        default=True
    )
    filename = bpy.props.StringProperty(
        description="Name of output file",
        name="File Name",
        default="render_settings.txt",
        subtype="FILE_NAME"
    )


class SRDRenderer:
    """Hold the current state of the render, ie if currently rendering."""

    _registered_hooks = []
    _registered_groups = {'default': ('', 0)}
    _group_id = 1

    @classmethod
    def register_hook(cls, hook):
        """Add hook to the list of available hooks and add a bool property to the property group."""
        cls._registered_hooks.append(hook)
        setattr(SRDRenderSettings, hook.hook_idname, bpy.props.BoolProperty(name=hook.hook_label))

    @classmethod
    def register_group(cls, idname, label):
        cls._registered_groups[idname] = (label, cls._group_id)
        cls._group_id += 1

    @classmethod
    def get_hooks(cls):
        return cls._registered_hooks

    def __init__(self, scene):
        self.scene = scene
        self._active_hooks = []
        self.can_render = False  # Weather or not the settings should be rendered.

        # For every active hook, initialize it with the current scene, run the pre_render function
        # and add it to the active hooks list.
        for hook in SRDRenderer._registered_hooks:
            # Only add it if it's active.
            if getattr(scene.srd_settings, hook.hook_idname):
                hook = hook(scene)
                hook.pre_render()
                self._active_hooks.append(hook)

    def render(self):
        # Return if we can't render.
        if not self.can_render:
            return
        # Get the file paths.
        render_dir = bpy.path.abspath(self.scene.render.filepath)
        path = os.path.join(render_dir, self.scene.srd_settings.filename)

        ### Collect all the data.
        s = self.format_render_data()
        print(s)

        ### Write the data to the info file.
        f = open(path, 'w')
        f.write(s)
        f.close()

    def frame_begin(self):
        for hook in self._active_hooks:
            hook.pre_frame()

    def frame_complete(self):
        for hook in self._active_hooks:
            hook.post_frame()

    def format_render_data(self):
        maxlen = 0
        for hook in self._active_hooks:
            if len(hook.hook_label) > maxlen:
                maxlen = len(hook.hook_label)
        template = '{name:>%s}: {data}' % (maxlen + 1)

        def get_group(h):
            if h.hook_group not in self._registered_groups:
                raise Exception("Group '%s' has not yet been registered." % h.hook_group)
            return self._registered_groups[h.hook_group][1]

        s = ""
        lastgroup = 'default'
        for hook in sorted(self._active_hooks, key=get_group):
            if hook.hook_group != lastgroup:
                s += '\n%s:\n' % self._registered_groups[hook.hook_group][0]
                lastgroup = hook.hook_group
            s += template.format(name=hook.hook_label, data=hook.post_render())
            s += '\n'
        return s


class SettingsHook:
    """Base class for all settings hooks"""
    # Really no need for this to be changed in any instances.
    hook_label = 'Unset'  # Every sub-class should define their own name.
    hook_idname = ''  # This is how other hooks can reference this one.
    hook_group = 'default'  # Hooks can be assigned to layout groups.
    hook_render_engine = {'ALL'}  # ALL is for every render engine. Though it can be any combination of render engines.

    @classmethod
    def is_valid_renderer(cls, context):
        """Return true if this hook can be used with current render engine."""
        return context.scene.render.engine in cls.hook_render_engine or 'ALL' in cls.hook_render_engine

    def __init__(self, scene):
        self.scene = scene

    def pre_render(self):
        """Called before the rendering starts."""

    def post_render(self):
        """Called after all the rendering has finished."""
        # Every instance should implement this function.
        raise NotImplementedError

    def pre_frame(self):
        """Called before the rendering of each frame."""

    def post_frame(self):
        """Called after the rendering of each frame"""


class TimeHook(SettingsHook):
    hook_label = 'Time'
    hook_idname = 'time'

    t = 0
    ft = 0
    peakframe = 0
    peaktime = 0

    def pre_render(self):
        self.t = time.time()

    def post_render(self):
        return '%.2fs(Peak: %.2fs on frame %s)' % (time.time() - self.t, self.peaktime, self.peakframe)

    def pre_frame(self):
        self.ft = time.time()

    def post_frame(self):
        frametime = time.time() - self.ft
        if frametime > self.peaktime:
            self.peaktime = frametime
            self.peakframe = self.scene.frame_current

SRDRenderer.register_hook(TimeHook)

SRDRenderer.register_group('resolution', 'Output Resolution')


class ResolutionHook(SettingsHook):
    hook_label = 'Resolution'
    hook_idname = 'resolution'
    hook_group = 'resolution'

    def post_render(self):
        x = self.scene.render.resolution_x
        y = self.scene.render.resolution_y
        return "%sx%spx" % (x, y)

SRDRenderer.register_hook(ResolutionHook)


class TrueResolutionHook(SettingsHook):
    hook_label = 'True resolution'
    hook_idname = 'trueres'
    hook_group = 'resolution'

    def post_render(self):
        fac = self.scene.render.resolution_percentage / 100
        x = self.scene.render.resolution_x * fac
        y = self.scene.render.resolution_y * fac
        return "%sx%spx" % (x, y)

SRDRenderer.register_hook(TrueResolutionHook)


class FrameRangeHook(SettingsHook):
    hook_label = 'Frame Range'
    hook_idname = 'framerange'

    def post_render(self):
        start = self.scene.frame_start
        end = self.scene.frame_end
        return "%s - %s(Total Frames: %s)" % (start, end, end - (start-1))

SRDRenderer.register_hook(FrameRangeHook)

SRDRenderer.register_group('seed', 'Seed')


class SeedHook(SettingsHook):
    hook_label = 'Seed'
    hook_idname = 'seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.seed)

SRDRenderer.register_hook(SeedHook)


class SeedAnimatedHook(SettingsHook):
    hook_label = 'Seed is Animated'
    hook_idname = 'animated_seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.use_animated_seed)

SRDRenderer.register_hook(SeedAnimatedHook)


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
        layout.prop(context.scene.srd_settings, 'filename')
        for hook in SRDRenderer.get_hooks():
            if hook.is_valid_renderer(context):
                layout.prop(context.scene.srd_settings, hook.hook_idname)


def register():
    # Add handlers
    bpy.app.handlers.render_write.append(render_write)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_complete.append(render_complete)
    bpy.app.handlers.render_pre.append(render_pre)
    bpy.app.handlers.render_post.append(render_post)

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
    bpy.app.handlers.render_pre.pop()
    bpy.app.handlers.render_post.pop()
    # # END DEBUG CODE ##

    # Remove handlers
    # bpy.app.handlers.render_write.remove(render_write)
    # bpy.app.handlers.render_cancel.remove(render_cancel)
    # bpy.app.handlers.render_init.remove(render_init)
    # bpy.app.handlers.render_complete.remove(render_complete)
    # bpy.app.handlers.render_pre.remove(render_complete)
    # bpy.app.handlers.render_post.remove(render_complete)


if __name__ == "__main__":
    try:
        unregister()
    finally:
        register()