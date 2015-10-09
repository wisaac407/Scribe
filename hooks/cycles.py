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

from ..ScribeRenderHook import ScribeRenderHook
from ..ScribeRenderer import ScribeRenderer


### Seed Group
class SeedHook(ScribeRenderHook):
    """Cycles sampling seed."""
    hook_label = 'Seed'
    hook_idname = 'seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.seed


class SeedAnimatedHook(ScribeRenderHook):
    """Weather or not the seed is animated from frame to frame."""
    hook_label = 'Seed is Animated'
    hook_idname = 'animated_seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.use_animated_seed


## Volume Sampling group
class VolumeStepHook(ScribeRenderHook):
    """Cycles volume step size."""
    hook_label = 'Step Size'
    hook_idname = 'step_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.volume_step_size


class VolumeStepMaxHook(ScribeRenderHook):
    """Maximum number of cycles volume steps."""
    hook_label = 'Max Steps'
    hook_idname = 'step_max_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.volume_max_steps


## Performance group.
class TileSizeHook(ScribeRenderHook):
    """Tile size."""
    hook_label = 'Tile Size'
    hook_idname = 'tile_size'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return '%sx%s' % (self.scene.render.tile_x, self.scene.render.tile_y)


class TileOrderHook(ScribeRenderHook):
    """Cycles tile order."""
    hook_label = 'Tile Order'
    hook_idname = 'tile_order'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    # Dictionary mapping order idname -> order label. i.e. {'CENTER': 'center'}
    orders = dict((idname, label) for idname, label, _ in
        bpy.types.CyclesRenderSettings.tile_order[1]['items'])

    def post_render(self):
        return self.orders[self.scene.cycles.tile_order]


class ThreadsModeHook(ScribeRenderHook):
    """Which scheme is used to determine the number of threads."""
    hook_label = 'Threads Mode'
    hook_idname = 'threads_mode'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.scene.render.threads_mode.capitalize()


class ThreadsHook(ScribeRenderHook):
    """How many threads are being used to render."""
    hook_label = 'Threads'
    hook_idname = 'threads'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.scene.render.threads


## Bounces group.
class LBBoundsHook(ScribeRenderHook):
    """Bounds of the number of reflection bounces."""
    hook_label = 'Total Bounds'
    hook_idname = 'lb_bounds'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return "min: %s, max: %s" % (self.scene.cycles.min_bounces, self.scene.cycles.max_bounces)


class LBDiffuseHook(ScribeRenderHook):
    """Maximum number of diffuse reflection bounces."""
    hook_label = 'Diffuse'
    hook_idname = 'lb_diffuse'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.diffuse_bounces


class LBGlossyHook(ScribeRenderHook):
    """Maximum number of glossy reflection bounces."""
    hook_label = 'Glossy'
    hook_idname = 'lb_glossy'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.glossy_bounces


class LBTransHook(ScribeRenderHook):
    """Maximum number of transmission reflection bounces."""
    hook_label = 'Transmission'
    hook_idname = 'lb_trans'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.transmission_bounces


class LBVolumeHook(ScribeRenderHook):
    """Maximum number of volume reflection bounces."""
    hook_label = 'Volume'
    hook_idname = 'lb_volume'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.volume_bounces


class LPShadowsHook(ScribeRenderHook):
    """Use transparency of surfaces for rendering shadows."""
    hook_label = 'Shadows'
    hook_idname = 'lp_shadows'
    hook_group = 'light_paths'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.use_transparent_shadows


class LPCausticsReflectiveHook(ScribeRenderHook):
    """Using reflective caustics."""
    hook_label = 'Reflective Caustics'
    hook_idname = 'lp_caustics_reflective'
    hook_group = 'light_paths'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.caustics_reflective


class LPCausticsRefractiveHook(ScribeRenderHook):
    """Using refractive caustics."""
    hook_label = 'Refractive Caustics'
    hook_idname = 'lp_caustics_refractive'
    hook_group = 'light_paths'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.caustics_refractive


class LPFilterGlossyHook(ScribeRenderHook):
    """Cycles filter glossy threshold."""
    hook_label = 'Filter Glossy'
    hook_idname = 'lp_filter_glossy'
    hook_group = 'light_paths'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.blur_glossy


## Sampling group
class SMSamplesHook(ScribeRenderHook):
    """Number of cycles samples used(accounting for square samples)."""
    hook_label = 'Samples'
    hook_idname = 'sm_samples'
    hook_group = 'sampling'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        samples = self.scene.cycles.samples
        square_samples = self.scene.cycles.use_square_samples
        # If we are using square samples then square the output.
        return samples * samples if square_samples else samples


class SMClampDirectHook(ScribeRenderHook):
    """How much we are clamping direct light."""
    hook_label = 'Clamp Direct'
    hook_idname = 'sm_clamp_direct'
    hook_group = 'sampling'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.sample_clamp_direct


class SMClampIndirectHook(ScribeRenderHook):
    """How much we are clamping indirect light."""
    hook_label = 'Clamp Indirect'
    hook_idname = 'sm_clamp_indirect'
    hook_group = 'sampling'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return self.scene.cycles.sample_clamp_indirect


def register():
    # Seed group.
    ScribeRenderer.register_group('seed', 'Seed')
    ScribeRenderer.register_hook(SeedHook)
    ScribeRenderer.register_hook(SeedAnimatedHook)

    # Volume sampling group.
    ScribeRenderer.register_group('vol_sample', 'Volume Sampling')
    ScribeRenderer.register_hook(VolumeStepHook)
    ScribeRenderer.register_hook(VolumeStepMaxHook)

    # Performance group.
    ScribeRenderer.register_group('perf', 'Performance')
    ScribeRenderer.register_hook(TileSizeHook)
    ScribeRenderer.register_hook(TileOrderHook)
    ScribeRenderer.register_hook(ThreadsModeHook)
    ScribeRenderer.register_hook(ThreadsHook)

    # Bounces group.
    ScribeRenderer.register_group('light_bounces', 'Bounces')
    ScribeRenderer.register_hook(LBBoundsHook)
    ScribeRenderer.register_hook(LBDiffuseHook)
    ScribeRenderer.register_hook(LBGlossyHook)
    ScribeRenderer.register_hook(LBTransHook)
    ScribeRenderer.register_hook(LBVolumeHook)

    # Light Paths group.
    ScribeRenderer.register_group('light_paths', 'Light Paths')
    ScribeRenderer.register_hook(LPShadowsHook)
    ScribeRenderer.register_hook(LPCausticsReflectiveHook)
    ScribeRenderer.register_hook(LPCausticsRefractiveHook)
    ScribeRenderer.register_hook(LPFilterGlossyHook)

    # Sampling group
    ScribeRenderer.register_group('sampling', 'Sampling')
    ScribeRenderer.register_hook(SMSamplesHook)
    ScribeRenderer.register_hook(SMClampDirectHook)
    ScribeRenderer.register_hook(SMClampIndirectHook)
