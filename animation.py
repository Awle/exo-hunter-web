from manim import *
import pandas as pd
from website import response


class NoExo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        sphere1 = Sphere(center=(0, 0, 0), radius=2, resolution=(50, 50))

        sphere1.set_color(YELLOW)

        text3d = Text("This star in unlikely to have any exoplanet",
                      font_size=36).set_shade_in_3d(False)
        text3d.set_color(RED)
        text3d.set_opacity(opacity=3)

        axes = ThreeDAxes()

        dot1 = Dot3D(point=(0.5, -2, 0.8),
                     radius=0.3,
                     color=BLACK,
                     resolution=(20, 20))
        dot2 = Dot3D(point=(2, -0.5, 0.8),
                     radius=0.3,
                     color=BLACK,
                     resolution=(20, 20))
        dot3 = Dot3D(point=(1.5, -1.5, -0.5),
                     radius=0.6,
                     color=BLACK,
                     resolution=(20, 20))

        self.add_fixed_in_frame_mobjects(text3d)
        self.add_foreground_mobjects(text3d)
        self.add(sphere1, text3d)
        self.play(Write(text3d))
        self.add_foreground_mobjects(text3d)
        self.wait(1)
        self.play(FadeIn(dot1, dot2, dot3), run_time=1)
        self.play(Unwrite(text3d, reverse=False))
        self.wait(0.5)
