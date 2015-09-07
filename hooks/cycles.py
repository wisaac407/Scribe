from SRDRenderHook import SRDRenderHook
from SRDRenderer import SRDRenderer

### Seed Group
SRDRenderer.register_group('seed', 'Seed')


class SeedHook(SRDRenderHook):
    """Cycles sampling seed."""
    hook_label = 'Seed'
    hook_idname = 'seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.seed)

SRDRenderer.register_hook(SeedHook)


class SeedAnimatedHook(SRDRenderHook):
    """Weather or not the seed is animated from frame to frame."""
    hook_label = 'Seed is Animated'
    hook_idname = 'animated_seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.use_animated_seed)

SRDRenderer.register_hook(SeedAnimatedHook)


## Volume Sampling group
SRDRenderer.register_group('vol_sample', 'Volume Sampling')


class VolumeStepHook(SRDRenderHook):
    """Cycles volume step size."""
    hook_label = 'Step Size'
    hook_idname = 'step_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_step_size)

SRDRenderer.register_hook(VolumeStepHook)


class VolumeStepMaxHook(SRDRenderHook):
    """Maximum number of cycles volume steps."""
    hook_label = 'Max Steps'
    hook_idname = 'step_max_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_max_steps)

SRDRenderer.register_hook(VolumeStepMaxHook)