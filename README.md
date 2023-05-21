# Ursina FirstPersonController v1.1

FirstPersonController is an open source Ursina Engine library that anyone can use.

FirstPersonController has smooth movement, smooth jumping, smooth running and smooth sneaking. It also has 33 different raycasts to make the collision system as precise as possible.

FirstPersonController is fully configurable.

Attributes that can be changed without editing the library:
```
- height
- visible_self
- fov
- sprint_fov
- speed
- sneak_speed
- sprint_speed
- gravity
- weight
- jump_height
- jump_time
- in_air_time
- ignore_entities
```

Sample code using FirstPersonController:
```
from ursina import *
from first_person_controller import FirstPersonController
from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader

app = Ursina()

shader = lit_with_shadows_shader

player = FirstPersonController()

Sky(texture="sky.png")

sun = DirectionalLight(shadow_map_resolution=(4096, 4096))
sun.look_at(Vec3(-1, 0.5, 0))
scene.fog_density = (100, 1000)

window.borderless = False
window.editor_ui.disable()

ground = Entity(scale=(15, 1, 40), y=-1, texture="white_cube", collider="box", model="cube", shader=shader)
ground.texture_scale = (ground.scale_x, ground.scale_z)
ground2 = Entity(scale=(10, 1, 15), y=-1, texture="white_cube", collider="box", model="cube", rotation_x=-30, z=2.9, shader=shader)
ground2.texture_scale = (ground2.scale_x, ground2.scale_z)

wall1 = Entity(scale=(1, 3.5, 5), y=1.25, texture="white_cube", collider="box", model="cube", x=-2, shader=shader)
wall1.texture_scale = (wall1.scale_x,  wall1.scale_z)

ground3 = Entity(scale=(5, 1, 5), y=3.5, texture="white_cube", collider="box", model="cube", shader=shader)
ground3.texture_scale = (ground3.scale_x, ground3.scale_z)

ground4 = Entity(scale=(3, 1, 3), y=4, texture="white_cube", collider="box", model="cube", z=-4, shader=shader)
ground4.texture_scale = (ground4.scale_x, ground4.scale_z)

app.run()
```

Images:
![image](https://github.com/aleksander788/ursina_firstpersoncontroller/assets/133954902/0d854e32-621f-4cc4-afb7-0fd6364a4ede)
![image](https://github.com/aleksander788/ursina_firstpersoncontroller/assets/133954902/511f9475-d6fe-4a95-a929-3e2fd96216c7)
![image](https://github.com/aleksander788/ursina_firstpersoncontroller/assets/133954902/5b0c13aa-799e-4fc9-8dcb-b082a4d79472)
