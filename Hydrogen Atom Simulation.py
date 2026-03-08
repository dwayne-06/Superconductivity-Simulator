from manim import *
import numpy as np

class Hydrogen(Scene):
    def construct(self):

        title = Text("H atom", font_size=48).to_edge(UP)

        self.play(Write(title))

        circle = Circle(radius=1, color=WHITE)
        electron = Dot(color=BLUE).shift(UP * 1)

        electron_label = MathTex("e^-", color=BLUE)
        electron_label.next_to(electron, UP, buff=0.1)

        # updater makes the label follow the electron
        electron_label.add_updater(
            lambda m: m.next_to(electron, UP, buff=0.1)
        )

        atom = Dot(color=RED)

        self.add(circle, electron, electron_label, atom)

        self.play(
            Rotate(
                electron,
                angle=2 * PI,
                about_point=ORIGIN,
                rate_func=linear
            ),
            run_time=4
        )
        