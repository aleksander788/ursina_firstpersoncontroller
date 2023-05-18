from ursina import *

class SmoothFollow():
    def __init__(self, target=None, offset=(0, 0, 0), speed=8):
        self.target = target
        self.offset = offset
        self.speed = speed

    def update(self):
        self.entity.world_x = lerp(self.entity.world_x, self.target.world_x, time.dt * self.speed)
        self.entity.world_z = lerp(self.entity.world_z, self.target.world_z, time.dt * self.speed)

class FirstPersonController(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        self.cursor = Entity(parent=camera.ui, model="quad", color=color.dark_gray, scale=0.008, rotation_z=45)

        super().__init__(add_to_scene_entities, **kwargs)

        self.model = "cube"
        self.height = 2
        self.height_no_use = self.height
        self.visible_self = False
        self.fov = 90
        self.sprint_fov = 110
        self.mouse_sensitivity = Vec2(60, 60)
        self.speed = 0.8
        self.speed_no_use = self.speed
        self.sneak_speed = 0.4
        self.sprint_speed = 1.5
        self.gravity = 1
        self.collider = "box"
        self.camera_animating = False
        self.sprinting = False

        camera.position = (0, 0, 0)
        camera.fov = 90

        self.grounded = False
        self.jumping = False
        self.air_time = 0
        self.tempSpeed = 0
        self.weight = 5
        self.jump_height = 2
        self.jump_time = 0.5
        self.in_air_time = 0.025
        self.sneak = False

        self.direction = Vec3(0, 0, 0)

        self.controls = {"forward": "w", "backward": "s", "left": "a", "right": "d", "jump": "space", "sneak": "shift", "sprint": "control"}

        mouse.locked = True

        for key, val in kwargs.items():
            setattr(self, key, val)

        self.camera_pivot = Entity(parent=self, y=self.height_no_use)
        camera.add_script(SmoothFollow(target=self.camera_pivot, offset=(0, self.height_no_use, 0), speed=6))

    def end_jump(self):
        self.jumping = False

    def jump(self):
        if not self.jumping and self.grounded:
            if hasattr(self, "y_animator"):
                    self.y_animator.kill()

            self.stop_sneak()

            self.jumping = True
            self.grounded = False
            self.animate_y(self.y + self.jump_height, curve=curve.out_expo, delay=0, duration=self.jump_time)

            invoke(self.end_jump, delay=self.jump_time + self.in_air_time)

    def update(self):    
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        camera.rotation_y = self.rotation_y
        self.camera_pivot.y = self.y + self.height_no_use
        camera.y = self.y + self.height_no_use
        
        self.direction = (Vec3(
            self.forward * (held_keys[self.controls["forward"]] - held_keys[self.controls["backward"]])
            + self.right * (held_keys[self.controls["right"]] - held_keys[self.controls["left"]])
            ).normalized()) * self.speed_no_use
        
        if self.direction != Vec3(0, 0, 0):
            self.camera_animating = True
        else:
            self.camera_animating = False
        
        head_top_middle_ray = raycast(self.position + Vec3(0, self.height_no_use, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_top_right_ray = raycast(self.position + Vec3(0.5, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_top_left_ray = raycast(self.position + Vec3(-0.5, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_middle_ray = raycast(self.position + Vec3(0, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_left_ray = raycast(self.position + Vec3(-0.5, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_middle_left_ray = raycast(self.position + Vec3(-0.25, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_right_ray = raycast(self.position + Vec3(0.5, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        head_middle_right_ray = raycast(self.position + Vec3(0.25, self.height_no_use - 0.1, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)

        front_middle_half_ray = raycast(self.position + Vec3(0, self.height_no_use/2, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        front_left_half_ray = raycast(self.position + Vec3(-0.5, self.height_no_use/2, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        front_right_half_ray = raycast(self.position + Vec3(0.5, self.height_no_use/2, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)

        feet_middle_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        feet_left_ray = raycast(self.position + Vec3(-0.5, 0.5, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        feet_middle_left_ray = raycast(self.position + Vec3(-0.25, 0.5, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        feet_right_ray = raycast(self.position + Vec3(0.5, 0.5, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)
        feet_middle_right_ray = raycast(self.position + Vec3(0.25, 0.5, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)

        feet_bottom_middle_ray = raycast(self.position + Vec3(0, 0, 0), self.direction, ignore=(self, ), distance=0.5, debug=False)

        if not head_left_ray.hit and not head_right_ray.hit and not head_middle_ray.hit and not feet_left_ray.hit and not feet_right_ray.hit and not head_middle_left_ray.hit and not head_middle_right_ray.hit and not feet_middle_left_ray.hit and not feet_middle_right_ray.hit and not feet_middle_ray.hit and not feet_middle_ray.hit and not front_middle_half_ray.hit and not front_left_half_ray.hit and not front_right_half_ray.hit and not head_top_left_ray.hit and not head_top_middle_ray.hit and not head_top_right_ray.hit:
            self.position += self.direction * (self.speed / 5)

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        camera.rotation_x = self.camera_pivot.rotation_x

        if self.gravity and not self.jumping:
            bottom_middle_ray = raycast(self.position, Vec3(0, -1, 0), ignore=(self, ), distance=0.5, debug=False)
            bottom_1_ray = raycast(self.position, Vec3(-0.5, -1, 0.5), ignore=(self, ), distance=0.5, debug=False)
            bottom_2_ray = raycast(self.position, Vec3(0.5, -1, 0.5), ignore=(self, ), distance=0.5, debug=False)
            bottom_3_ray = raycast(self.position, Vec3(-0.5, -1, -0.5), ignore=(self, ), distance=0.5, debug=False)
            bottom_4_ray = raycast(self.position, Vec3(0.5, -1, -0.5), ignore=(self, ), distance=0.5, debug=False)

            ray = raycast(self.world_position + (0, self.height_no_use, 0), self.down, ignore=(self,))

            if ray.distance <= self.height_no_use + .1:
                if ray.world_normal.y > 0.7 and ray.world_point.y - self.world_y < 0.5:
                    self.y = ray.world_point[1]

            else:
                if not bottom_middle_ray.hit and not bottom_1_ray.hit and not bottom_2_ray.hit and not bottom_3_ray.hit and not bottom_4_ray.hit:
                    if self.tempSpeed < 0.25:
                        self.tempSpeed += self.weight/375
                    else:
                        self.tempSpeed += self.weight/1000

                    self.y -= self.tempSpeed

                    self.air_time += time.dt

                    self.grounded = False

                else:
                    if self.grounded == False:
                        if held_keys[self.controls["sneak"]]:
                            self.grounded = True
                            self.start_sneak()

                    self.grounded = True
                    self.air_time = 0
                    self.tempSpeed = 0

        if self.jumping:
            top_middle_ray = raycast(self.position + Vec3(0, self.height_no_use, 0), Vec3(0, 1, 0), ignore=(self, ), distance=0.55, debug=False)
            top_middle_1_ray = raycast(self.position + Vec3(0.5, self.height_no_use, 0.5), Vec3(0, 1, 0), ignore=(self, ), distance=0.55, debug=False)
            top_middle_2_ray = raycast(self.position + Vec3(-0.5, self.height_no_use, -0.5), Vec3(0, 1, 0), ignore=(self, ), distance=0.55, debug=False)
            top_middle_3_ray = raycast(self.position + Vec3(0.5, self.height_no_use, -0.5), Vec3(0, 1, 0), ignore=(self, ), distance=0.55, debug=False)
            top_middle_4_ray = raycast(self.position + Vec3(-0.5, self.height_no_use, 0.5), Vec3(0, 1, 0), ignore=(self, ), distance=0.55, debug=False)
            
            if top_middle_ray.hit or top_middle_1_ray.hit or top_middle_2_ray.hit or top_middle_3_ray.hit or top_middle_4_ray.hit:
                if hasattr(self, "y_animator"):
                    self.y_animator.kill()

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

    def start_sneak(self):
        if self.grounded:
            self.stop_sprint()
            self.sneak = True

            if hasattr(self, "height_no_use_animator"):
                self.height_no_use_animator.kill()
            
            self.animate("height_no_use", self.height - 0.5, curve=curve.out_expo, delay=0, duration=0.3)
            self.speed_no_use = self.sneak_speed

    def stop_sneak(self):
        if hasattr(self, "height_no_use_animator"):
            self.height_no_use_animator.kill()
        
        self.animate("height_no_use", self.height, curve=curve.out_expo, delay=0, duration=0.3)
        
        if not self.sprinting:
            self.speed_no_use = self.speed

        self.sneak = False

    def start_sprint(self):
        self.sprinting = True
        self.stop_sneak()
        self.speed_no_use = self.sprint_speed

        if hasattr(camera, "fov_animator"):
            camera.fov_animator.kill()

        camera.animate("fov", self.sprint_fov, delay=0, duration=0.5, curve=curve.out_expo)

    def stop_sprint(self):
        if not self.sneak:
            self.sprinting = False
            self.speed_no_use = self.speed

            if hasattr(camera, "fov_animator"):
                camera.fov_animator.kill()

            camera.animate("fov", self.fov, delay=0, duration=0.5, curve=curve.out_expo)

    def input(self, key):
        if key == self.controls["jump"]:
            self.jump()

        if key == self.controls["sneak"]:
            if self.sneak == False:
                self.start_sneak()
            else:
                sneak_ray = raycast(self.position + Vec3(0, self.height_no_use, 0), Vec3(0, 1, 0), distance=0.6, ignore=(self, ))
                sneak_1_ray = raycast(self.position + Vec3(0.5, self.height_no_use, 0.5), Vec3(0, 1, 0), distance=0.6, ignore=(self, ))
                sneak_2_ray = raycast(self.position + Vec3(-0.5, self.height_no_use, -0.5), Vec3(0, 1, 0), distance=0.6, ignore=(self, ))
                sneak_3_ray = raycast(self.position + Vec3(0.5, self.height_no_use, -0.5), Vec3(0, 1, 0), distance=0.6, ignore=(self, ))
                sneak_4_ray = raycast(self.position + Vec3(-0.5, self.height_no_use, 0.5), Vec3(0, 1, 0), distance=0.6, ignore=(self, ))
                if not sneak_ray.hit and not sneak_1_ray.hit and not sneak_2_ray.hit and not sneak_3_ray.hit and not sneak_4_ray.hit:
                    self.stop_sneak()

        if key == self.controls["sprint"]:
            self.start_sprint()

        if key == f"{self.controls['sprint']} up":
            if not held_keys["w"]:
                self.stop_sprint()

        if key == f"{self.controls['forward']} up":
            self.stop_sprint()

if __name__ == '__main__':
    app = Ursina()
    from first_person_controller import FirstPersonController
    from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader

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