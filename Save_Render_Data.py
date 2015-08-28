import bpy, os, time, random
from bpy.app.handlers import persistent

SCRIPT_ID = "render%s" % random.random()

FORMAT = """
Frames: %(nframes)s(%(fstart)s-%(fend)s)
Total Time: %(time).2fs
Average Time: %(average_time).2fs per frame

Resolution: %(res_x)sx%(res_y)spx(%(res_percent)s%%)
Ture Resolution: %(true_res_x)sx%(true_res_y)spx

Seed: %(seed)s
Is seed animated: %(animated_seed)s

Samples: %(samples)s
Square Samples: %(square_samples)s

Tile Size: %(tile_x)sx%(tile_y)s
""".strip()

def cleanup(scene):
    "Remove any intermediate props stored on the scene."
    
    # Loop through all the scene custom props deleting the ones that we set.
    for key in scene.keys():
        if key.startswith(SCRIPT_ID): del scene[key]

@persistent
def render_write(scene):
    # If we are writing a file then we should be writing the stats also.
    scene[SCRIPT_ID+'written'] = True

@persistent
def render_cancel(scene):
    "Just cleanup the scene because rendering was canceled."
    cleanup(scene)


@persistent
def render_init(scene):
    "Initilize the intermediate props set on the scene."
    scene[SCRIPT_ID+'time'] = time.time() # For logging the total rendering time.
    scene[SCRIPT_ID+'written'] = False # Weather or the any files have been written to disk.


@persistent
def render_complete(scene):
    # If we haven't written any files then we shouldn't write our stats.
    if not scene[SCRIPT_ID+'written']:
        cleanup(scene)
        return
    # Get the file paths.
    render_dir = bpy.path.abspath(scene.render.filepath)
    path = os.path.join(render_dir, 'render_settings.txt')
    
    ### Collect all the data.
    
    # Total render time
    t = time.time() - scene[SCRIPT_ID+'time']
    
    # Frames
    frame_start = scene.frame_start
    frame_end = scene.frame_end
    nframes = frame_end - (frame_start-1)
    average_time = t/nframes
    
    # Resolution
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    res_percent = scene.render.resolution_percentage
    
    true_res_x = res_x * (res_percent/100)
    true_res_y = res_y * (res_percent/100)
    
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


class RenderSettings(bpy.types.PropertyGroup):
    # XXX TODO: Fill in currect properties.
    enable = bpy.props.BoolProperty(
        description="Save the render data to file at render.",
        name="Save Render Data",
        default = True
    )


class RENDER_PT_SRD(bpy.types.Panel):
    """Puts the panel in the render data section."""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_label = "Save Render Data"

    def draw_header(self, context):
        self.layout.prop(context.scene.srd_settings, "enable", text="")

    def draw(self, context):
        layout = self.layout
        
        layout.active = context.scene.srd_settings.enable
        

def register():
    # Add handlers
    bpy.app.handlers.render_write.append(render_write)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_complete.append(render_complete)
    
    # Register custom properties
    bpy.utils.register_class(RenderSettings)

    bpy.types.Scene.srd_settings = \
        bpy.props.PointerProperty(type=RenderSettings)

    # Register panels
    bpy.utils.register_class(RENDER_PT_SRD)


def unregister():
    ## BEGIN DEBUG CODE ##
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