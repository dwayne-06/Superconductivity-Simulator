from manim import *
import numpy as np

#Introduction
class CooperPairIntro(Scene): 
    def construct(self):

        circle = Circle()
        square = Square()

        text1 = Text("Cooper Pair Formation", font_size=72)
        text2 = Text("By Dwayne Nobleza", font_size=36)
        
        text1.to_edge(UP, buff=1.0) 
        text2.next_to(text1, DOWN, buff=0.5) 
        
        self.play(
            Write(text1), 
            Write(text2), 
            run_time=2
        )
        self.wait(0.5)
        self.play(
            Unwrite(text2)
        )

#Construction of the atomic lattice 

class CooperPair(Scene):
    def construct(self):

        time = ValueTracker(0)
        time.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(time)

        e1 = Dot(color=BLUE).shift(LEFT * 6)
        e1_label = MathTex("e^-", color=BLUE).next_to(e1, UP, buff=0.1)
        e1_group = VGroup(e1, e1_label)

        e2 = Dot(color=BLUE).shift(LEFT * 8 + DOWN * 0.3)
        e2_label = MathTex("e^-", color=BLUE).next_to(e2, UP, buff=0.1)
        e2_group = VGroup(e2, e2_label)

        electrons = [e1, e2]

        base_row = VGroup(
            Dot(LEFT),
            Dot(ORIGIN),
            Dot(RIGHT),
            Dot(2 * LEFT),
            Dot(3 * LEFT),
            Dot(4 * LEFT),
            Dot(2 * RIGHT)
        ).scale(2)

        g1 = base_row.copy().shift(RIGHT * 4 + UP * 3)
        g2 = base_row.copy().shift(RIGHT * 4 + UP * 1)
        g3 = base_row.copy().shift(RIGHT * 4 + DOWN * 1)
        g4 = base_row.copy().shift(RIGHT * 4 + DOWN * 3)

        lattice_groups = [g1, g2, g3, g4]

        self.add(g1, g2, g3, g4)

        for group in lattice_groups:
            for dot in group:
                dot.initial_pos = dot.get_center()

        def atom_updater(dot, dt):

            force = np.array([0.0, 0.0, 0.0])

            for e in electrons:
                r = e.get_center() - dot.initial_pos
                dist = np.linalg.norm(r)

                if dist < 4:
                    force += 1.3 * r / (dist + 0.2)

            t = time.get_value()
            k = 1
            omega = 3
            amplitude = 0.5

            wave = amplitude * np.sin(k * dot.initial_pos[0] - omega * t)
            phonon = np.array([0, wave, 0])

            restoring = -0.8 * (dot.get_center() - dot.initial_pos)

            dot.shift((force + restoring + phonon) * dt)

        # Apply updater
        for group in lattice_groups:
            for dot in group:
                dot.add_updater(atom_updater)

        self.wait(1)

        # Show electrons
        self.play(FadeIn(e1_group))
        self.wait(0.5)
        self.play(FadeIn(e2_group))

        self.wait(1)

        # First electron moves through lattice
        self.play(
            e1_group.animate.shift(RIGHT * 8),
            run_time=4,
            rate_func=linear
        )

        self.wait(1)

        # Second electron follows distortion (Cooper pairing)
        self.play(
            e2_group.animate.shift(RIGHT * 10 + UP * 0.3),
            run_time=4,
            rate_func=linear
        )

        self.wait(1)

        # Highlight the Cooper pair
        pair_circle = Circle(radius=0.6, color=YELLOW).move_to(
            (e1.get_center() + e2.get_center()) / 2
        )

        pair_label = MathTex("Cooper\\ Pair", color=YELLOW).next_to(pair_circle, RIGHT)

        self.play(Create(pair_circle), Write(pair_label))

        self.wait(3)

        


