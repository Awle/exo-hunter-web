from manim import *
import pandas as pd
import json


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





class LoopOrbit(ThreeDScene):
    def construct(self):

        with open('response.json', 'r') as openfile:
            # Reading from json file
            response = json.load(openfile)
        response_raw = response
        response['solar_mass'] = response['solar_mass']
        response['solar_radius'] = np.log(float(response['solar_radius']) * 695508) /15
        response['orbital_period'] = np.log(response['orbital_period']) * 10
        response['planet_star_rad'] = np.log(response['planet_star_rad']) * 2
        plant_rad = np.log([float(x) * round(6371 / 100) for x in response['planet_radius']]) / 20
        response['planet_radius'] = plant_rad

        manim_input_values = response

        self.camera.background_color = BLACK
        self.set_camera_orientation(phi = 60 * DEGREES, theta= 0 * DEGREES) #phi-up down view, theta left-right tilt
        # kepid = Text(f"Kepler ID:{response_raw['id']}", font_size=50).set_shade_in_3d(True)
        # self.add_fixed_in_frame_mobjects(kepid) #<----- Add this
        # kepid.to_corner(UR)
        sun_radi = Text(f"Star radius: {round(response_raw['solar_radius'],3)} Sun(s)", font_size= 15, color= WHITE).set_shade_in_3d(True)
        self.add_fixed_in_frame_mobjects(sun_radi)
        sun_radi.to_corner(UL)
        sun_mass = Text(f"Star mass: {response_raw['solar_mass']} Sun(s)" , font_size= 15, color= WHITE).set_shade_in_3d(True).scale(1).next_to(sun_radi, DOWN)
        self.add_fixed_in_frame_mobjects(sun_mass)
        #sun_mass.to_corner(UL)
        planet_dist = Text(f"Planet(s) to sun distance: {[round(x,3) for x in response_raw['planet_star_rad']]} AU(s)", font_size= 15, color= WHITE).set_shade_in_3d(True)
        self.add_fixed_in_frame_mobjects(planet_dist)
        planet_dist.to_corner(UR)
        planet_mass = Text(
            f"Planet(s) radius: {[round(x,3) for x in response_raw['planet_radius']]} Earth(s)",
            font_size=15,
            color=WHITE).set_shade_in_3d(True).scale(1).next_to(
                planet_dist, DOWN)
        self.add_fixed_in_frame_mobjects(planet_mass)
        planet_orbit = Text(
            f"Planet(s) orbit(days): {[round(x,3) for x in response_raw['orbital_period']]} Day(s)",
            font_size=15,
            color=WHITE).set_shade_in_3d(True).scale(1).next_to(
                planet_dist, UP)
        self.add_fixed_in_frame_mobjects(planet_orbit)
        for i in range(len(manim_input_values['planet_radius'])):
            sun = Sphere(radius= manim_input_values['solar_radius']) #response_raw['solar_radius']
            sun.set_color(YELLOW_E)
            planet = Sphere(radius= manim_input_values['planet_radius'][i], color= BLUE ) #response_raw['planet_radius']
            orbit = Ellipse(width= manim_input_values['planet_star_rad'][i] + (i - 1), height= manim_input_values['planet_star_rad'][i] + (i - 2)) #response_raw['planet_star_rad'], response_raw['planet_star_rad']
            self.add(sun)
            self.add(orbit, planet)
            self.play(MoveAlongPath(planet, orbit), run_time= 2 + i, rate_function= linear) #response_raw['orbital_period']
