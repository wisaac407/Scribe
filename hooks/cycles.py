"""
hooks/cycles.py: All the Cycles-specific hooks.

Copyright (C) 2015 Isaac Weaver
Author: Isaac Weaver <wisaac407@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import bpy

from scribe.renderer import Renderer, RenderHook


class CyclesHook(RenderHook):
    """Cycles-only render hook"""
    @classmethod
    def poll(self, context):
        return context.scene.render.engine == 'CYCLES'


### Seed Group
class SeedHook(CyclesHook):
    """Cycles sampling seed."""
    hook_label = 'Seed'
    hook_idname = 'seed'
    hook_group = 'seed'

    def post_render(self):
        return self.scene.cycles.seed


class SeedAnimatedHook(CyclesHook):
    """Weather or not the seed is animated from frame to frame."""
    hook_label = 'Seed is Animated'
    hook_idname = 'animated_seed'
    hook_group = 'seed'

    def post_render(self):
        return self.scene.cycles.use_animated_seed


## Volume Sampling group
class VolumeStepHook(CyclesHook):
    """Cycles volume step size."""
    hook_label = 'Step Size'
    hook_idname = 'step_size'
    hook_group = 'vol_sample'

    def post_render(self):
        return self.scene.cycles.volume_step_size


class VolumeStepMaxHook(CyclesHook):
    """Maximum number of cycles volume steps."""
    hook_label = 'Max Steps'
    hook_idname = 'step_max_size'
    hook_group = 'vol_sample'

    def post_render(self):
        return self.scene.cycles.volume_max_steps


## Performance group.
class TileSizeHook(CyclesHook):
    """Tile size."""
    hook_label = 'Tile Size'
    hook_idname = 'tile_size'
    hook_group = 'perf'

    def post_render(self):
        return '%sx%s' % (self.scene.render.tile_x, self.scene.render.tile_y)


class TileOrderHook(RenderHook):
    """Cycles tile order."""
    hook_label = 'Tile Order'
    hook_idname = 'tile_order'
    hook_group = 'perf'

    # Dictionary mapping order idname -> order label. i.e. {'CENTER': 'center'}
    orders = dict((idname, label) for idname, label, _ in
        bpy.types.CyclesRenderSettings.tile_order[1]['items'])

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.orders[self.scene.cycles.tile_order]


class ThreadsModeHook(RenderHook):
    """Which scheme is used to determine the number of threads."""
    hook_label = 'Threads Mode'
    hook_idname = 'threads_mode'
    hook_group = 'perf'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.scene.render.threads_mode.capitalize()


class ThreadsHook(RenderHook):
    """How many threads are being used to render."""
    hook_label = 'Threads'
    hook_idname = 'threads'
    hook_group = 'perf'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine in {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.scene.render.threads


## Bounces group.
class LBBoundsHook(CyclesHook):
    """Bounds of the number of reflection bounces."""
    hook_label = 'Total Bounds'
    hook_idname = 'lb_bounds'
    hook_group = 'light_bounces'

    def post_render(self):
        return "min: %s, max: %s" % (self.scene.cycles.min_bounces, self.scene.cycles.max_bounces)


class LBDiffuseHook(CyclesHook):
    """Maximum number of diffuse reflection bounces."""
    hook_label = 'Diffuse'
    hook_idname = 'lb_diffuse'
    hook_group = 'light_bounces'

    def post_render(self):
        return self.scene.cycles.diffuse_bounces


class LBGlossyHook(CyclesHook):
    """Maximum number of glossy reflection bounces."""
    hook_label = 'Glossy'
    hook_idname = 'lb_glossy'
    hook_group = 'light_bounces'

    def post_render(self):
        return self.scene.cycles.glossy_bounces


class LBTransHook(CyclesHook):
    """Maximum number of transmission reflection bounces."""
    hook_label = 'Transmission'
    hook_idname = 'lb_trans'
    hook_group = 'light_bounces'

    def post_render(self):
        return self.scene.cycles.transmission_bounces


class LBVolumeHook(CyclesHook):
    """Maximum number of volume reflection bounces."""
    hook_label = 'Volume'
    hook_idname = 'lb_volume'
    hook_group = 'light_bounces'

    def post_render(self):
        return self.scene.cycles.volume_bounces


class LPShadowsHook(CyclesHook):
    """Use transparency of surfaces for rendering shadows."""
    hook_label = 'Shadows'
    hook_idname = 'lp_shadows'
    hook_group = 'light_paths'

    def post_render(self):
        return self.scene.cycles.use_transparent_shadows


class LPCausticsReflectiveHook(CyclesHook):
    """Using reflective caustics."""
    hook_label = 'Reflective Caustics'
    hook_idname = 'lp_caustics_reflective'
    hook_group = 'light_paths'

    def post_render(self):
        return self.scene.cycles.caustics_reflective


class LPCausticsRefractiveHook(CyclesHook):
    """Using refractive caustics."""
    hook_label = 'Refractive Caustics'
    hook_idname = 'lp_caustics_refractive'
    hook_group = 'light_paths'

    def post_render(self):
        return self.scene.cycles.caustics_refractive


class LPFilterGlossyHook(CyclesHook):
    """Cycles filter glossy threshold."""
    hook_label = 'Filter Glossy'
    hook_idname = 'lp_filter_glossy'
    hook_group = 'light_paths'

    def post_render(self):
        return self.scene.cycles.blur_glossy


## Sampling group
class SMSamplesHook(CyclesHook):
    """Number of cycles samples used(accounting for square samples)."""
    hook_label = 'Samples'
    hook_idname = 'sm_samples'
    hook_group = 'sampling'

    def post_render(self):
        samples = self.scene.cycles.samples
        square_samples = self.scene.cycles.use_square_samples
        # If we are using square samples then square the output.
        return samples * samples if square_samples else samples


class SMClampDirectHook(CyclesHook):
    """How much we are clamping direct light."""
    hook_label = 'Clamp Direct'
    hook_idname = 'sm_clamp_direct'
    hook_group = 'sampling'

    def post_render(self):
        return self.scene.cycles.sample_clamp_direct


class SMClampIndirectHook(CyclesHook):
    """How much we are clamping indirect light."""
    hook_label = 'Clamp Indirect'
    hook_idname = 'sm_clamp_indirect'
    hook_group = 'sampling'

    def post_render(self):
        return self.scene.cycles.sample_clamp_indirect


def register():
    # Seed group.
    Renderer.register_group('seed', 'Seed')
    Renderer.register_hook(SeedHook)
    Renderer.register_hook(SeedAnimatedHook)

    # Volume sampling group.
    Renderer.register_group('vol_sample', 'Volume Sampling')
    Renderer.register_hook(VolumeStepHook)
    Renderer.register_hook(VolumeStepMaxHook)

    # Performance group.
    Renderer.register_group('perf', 'Performance')
    Renderer.register_hook(TileSizeHook)
    Renderer.register_hook(TileOrderHook)
    Renderer.register_hook(ThreadsModeHook)
    Renderer.register_hook(ThreadsHook)

    # Bounces group.
    Renderer.register_group('light_bounces', 'Bounces')
    Renderer.register_hook(LBBoundsHook)
    Renderer.register_hook(LBDiffuseHook)
    Renderer.register_hook(LBGlossyHook)
    Renderer.register_hook(LBTransHook)
    Renderer.register_hook(LBVolumeHook)

    # Light Paths group.
    Renderer.register_group('light_paths', 'Light Paths')
    Renderer.register_hook(LPShadowsHook)
    Renderer.register_hook(LPCausticsReflectiveHook)
    Renderer.register_hook(LPCausticsRefractiveHook)
    Renderer.register_hook(LPFilterGlossyHook)

    # Sampling group
    Renderer.register_group('sampling', 'Sampling')
    Renderer.register_hook(SMSamplesHook)
    Renderer.register_hook(SMClampDirectHook)
    Renderer.register_hook(SMClampIndirectHook)
