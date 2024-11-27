bl_info = {
    "name": "Ultimate Studio Scene",
    "blender": (4, 3, 0),
    "category": "Scene",
    "author": "NECRO MANIA",
    "description": "Generates an ultimate studio scene with advanced features."
}

import bpy
from math import radians, sin, pi
from random import uniform
from bpy.props import (
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    EnumProperty,
    IntProperty
)

class OBJECT_OT_UltimateStudioScenePlus(bpy.types.Operator):
    """Create the Ultimate Studio Scene with Animations and Advanced Features"""
    bl_idname = "object.create_ultimate_studio_scene_plus"
    bl_label = "Create Ultimate Studio Scene Plus"
    bl_options = {'REGISTER', 'UNDO'}

    # Wall and background properties
    wall_color: FloatVectorProperty(
        name="Wall Color",
        subtype='COLOR',
        default=(0.8, 0.8, 0.8),
        min=0.0, max=1.0,
        description="Color of the wall"
    )
    background_gradient: BoolProperty(
        name="Gradient Background",
        default=True,
        description="Add a gradient background for the scene"
    )

    # Lighting properties
    animated_lights: BoolProperty(
        name="Animated Lights",
        default=True,
        description="Animate the lights with movement or intensity changes"
    )
    light_count: IntProperty(
        name="Number of Lights",
        default=5,
        min=1,
        max=20,
        description="Number of lights in the scene"
    )
    light_color: FloatVectorProperty(
        name="Light Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        description="Base color of the lights"
    )
    light_animation_speed: FloatProperty(
        name="Light Animation Speed",
        default=1.0,
        min=0.1,
        max=10.0,
        description="Speed of light animations"
    )

    # Camera settings
    multiple_cameras: BoolProperty(
        name="Add Multiple Cameras",
        default=True,
        description="Add several cameras with different angles"
    )

    # Props and objects
    add_random_objects: BoolProperty(
        name="Add Random Objects",
        default=True,
        description="Add randomly placed objects in the scene"
    )
    object_count: IntProperty(
        name="Number of Random Objects",
        default=10,
        min=1,
        max=50,
        description="Number of random objects to add"
    )

    def create_wall_and_floor(self):
        """Create the studio wall and floor"""
        # Create wall
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
        wall = bpy.context.active_object
        wall.name = "Studio Wall"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 5)})
        bpy.ops.object.mode_set(mode='OBJECT')
        wall.location = (0, -5, 2.5)

        # Apply wall color
        mat_wall = bpy.data.materials.new(name="WallMaterial")
        mat_wall.use_nodes = True
        bsdf = mat_wall.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*self.wall_color, 1.0)
        wall.data.materials.append(mat_wall)

        # Create floor
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
        floor = bpy.context.active_object
        floor.name = "Studio Floor"

    def add_lights(self):
        """Add lights with optional animation"""
        for i in range(self.light_count):
            x = uniform(-5, 5)
            y = uniform(-5, 5)
            z = uniform(2, 6)
            bpy.ops.object.light_add(type='POINT', location=(x, y, z))
            light = bpy.context.active_object
            light.name = f"Studio Light {i+1}"
            light.data.color = self.light_color
            light.data.energy = 500
            
            if self.animated_lights:
                frame_start = 1
                frame_end = 250
                light.animation_data_create()
                light.animation_data.action = bpy.data.actions.new(name=f"LightAnim_{i}")
                fcurve = light.animation_data.action.fcurves.new(data_path="location", index=2)
                keyframe = fcurve.keyframe_points.insert(frame_start, light.location.z)
                keyframe.interpolation = 'SINE'
                keyframe = fcurve.keyframe_points.insert(frame_end, light.location.z + sin(pi * self.light_animation_speed))
                keyframe.interpolation = 'SINE'

    def add_random_objects(self):
        """Add random objects in the scene"""
        shapes = ['SPHERE', 'CUBE', 'CYLINDER', 'CONE', 'TORUS']
        for i in range(self.object_count):
            shape = shapes[i % len(shapes)]
            x, y, z = uniform(-4, 4), uniform(-4, 4), uniform(0, 2)
            if shape == 'SPHERE':
                bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
            elif shape == 'CUBE':
                bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            elif shape == 'CYLINDER':
                bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
            elif shape == 'CONE':
                bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
            elif shape == 'TORUS':
                bpy.ops.mesh.primitive_torus_add(location=(x, y, z))

    def add_cameras(self):
        """Add multiple cameras"""
        positions = [(0, -10, 3), (-5, -10, 5), (5, -10, 5)]
        for i, pos in enumerate(positions):
            bpy.ops.object.camera_add(location=pos)
            cam = bpy.context.active_object
            cam.name = f"Camera_{i+1}"
            cam.rotation_euler = (radians(90), 0, radians(90 * i))

    def execute(self, context):
        # Create base elements
        self.create_wall_and_floor()
        self.add_lights()
        
        if self.add_random_objects:
            self.add_random_objects()
        
        if self.multiple_cameras:
            self.add_cameras()

        self.report({'INFO'}, "Ultimate Studio Scene Plus created!")
        return {'FINISHED'}

class ULTIMATE_STUDIO_SCENE_PLUS_PT_panel(bpy.types.Panel):
    """Panel for Ultimate Studio Scene Generator Plus"""
    bl_label = "Ultimate Studio Scene Generator Plus"
    bl_idname = "ULTIMATE_STUDIO_SCENE_PLUS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Studio Scene'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator(OBJECT_OT_UltimateStudioScenePlus.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_UltimateStudioScenePlus)
    bpy.utils.register_class(ULTIMATE_STUDIO_SCENE_PLUS_PT_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_UltimateStudioScenePlus)
    bpy.utils.unregister_class(ULTIMATE_STUDIO_SCENE_PLUS_PT_panel)

if __name__ == "__main__":
    register()
