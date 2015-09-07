class SRDRenderHook:
    """Base class for all settings hooks.

    Doc string will become the tooltip."""
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