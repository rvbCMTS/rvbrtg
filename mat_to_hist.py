import os
import time
from pathlib import Path
from manim import *
from manim import tempconfig
import pydicom
from maxutils.manim.helpers import build_pixels_vgroup

def get_histogram_traces_from_mat(mat, mask, nbins):
    vals = mat[mask]

    hist, bins = np.histogram(vals, bins=nbins)

    # step-curve
    xhist = np.repeat(hist, 2)
    yhist = np.repeat(bins, 2)[1:-1]

    # skala (visuell)
    xhist = xhist / xhist.max()
    xhist *= 0.75 * mat.size

    return xhist, yhist, hist, bins


RESALG = RESAMPLING_ALGORITHMS["none"]
dcm_file = pydicom.dcmread('test_img.dcm')

# 🔧 Inställningar
RESOLUTION = "480p"
FPS = 15
BACKGROUND_COLOR = BLACK
PREVIEW = True
config["disable_caching"] = True

# 🎥 Resolution map
RESOLUTIONS = {
    "480p": (854, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


class BuildScene(ThreeDScene):
    def construct(self):


        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(NumberPlane())
        img = dcm_file.pixel_array
        mat = img[::32, ::32]
        n_bins = 50

        vals = mat.flatten()
        idx = np.arange(vals.shape[0])

        
        pixels = build_pixels_vgroup(
            mat=mat,
            mask=np.ones(mat.shape, dtype=bool),
            image_width=6,
            plot_min=mat.min(),
            plot_max=mat.max(),
            colormap='gray_r',
            offset_from_origin=(-3.5, 1, 0),
        )


        pixels_edge = SurroundingRectangle(pixels, buff=0)
        #self.add(NumberPlane())
        ax = Axes(
            axis_config={"numbers_to_include": []},
            x_length=pixels_edge.width,
            y_length=pixels_edge.height,
            x_range=(0, len(vals), 10000),
            y_range=(min(vals), max(vals), 10000),
            )

        ax.next_to(pixels, direction=RIGHT)
        ax_bars = ax.copy().next_to(ax, direction=RIGHT)
        self.add(ax_bars)



        cb = (
            Rectangle(width=0.5, height=4, fill_opacity=1, color=YELLOW)
            .set_stoke(0)
            .set_fill([BLACK, WHITE])
            .shift(0 * RIGHT)
        )


        self.add(pixels, pixels_edge, ax)
        self.wait()


        idx_sorted = sorted(
            idx,
            key=lambda i: (-pixels[i].col, pixels[i].row)
        )


        self.play(
            LaggedStart(
                *[
                    pixels[i]
                    .animate.scale(0.05)
                    .move_to(ax.c2p(k, pixels[i].val))
                    .fade_to(YELLOW, alpha=1)
                    .set_opacity(0.3)
                    for k, i in enumerate(idx_sorted)
                ],
                lag_ratio=0.05,
                run_time=6,
            )
        )

        self.wait()

        self.play(
            pixels_edge.animate.shift(6.25*LEFT),
            ax.animate.shift(6.25*LEFT),
            ax_bars.animate.shift(6.25*LEFT),
            pixels.animate.shift(6.25*LEFT),
            )

        bins = 30


        # bin-kanter
        edges = np.linspace(mat.min(), mat.max(), bins + 1)

        # en grupp per bin
        pixel_bins = [VGroup() for _ in range(bins)]

        for px in pixels:

            val = px.val

            # hitta bin-index
            bin_idx = np.digitize(val, edges) - 1

            # fix för maxvärdet
            bin_idx = np.clip(bin_idx, 0, bins - 1)

            pixel_bins[bin_idx].add(px)



        ys = np.linspace(mat.min(), mat.max(), bins)

        gridlines = VGroup(*[
            Line(
                ax.c2p(0, y),
                ax.c2p(len(idx), y),
            ).set_stroke(GRAY, width=1, opacity=0.5)
            for y in ys
        ])

        self.play(
            LaggedStart(
                *[Create(line) for line in gridlines],
                lag_ratio=0.05,
                run_time=2
            )
        )

        self.wait()

        # histogram
        hist, edges = np.histogram(vals, bins=bins)

        # maxvärde behövs för skalning
        max_count = max(hist)

        bars = VGroup()

        for count, y0, y1 in zip(hist, edges[:-1], edges[1:]):

            # mitten av binen i y-led
            y_center = (y0 + y1) / 2

            # bredd i x-led
            x_width = count

            bar = Rectangle(
                width=ax.x_axis.n2p(x_width)[0] - ax.x_axis.n2p(0)[0],
                height=ax.y_axis.n2p(y1)[1] - ax.y_axis.n2p(y0)[1],
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=1,
            )

            # placera så att stapeln börjar vid y-axeln
            bar.move_to(
                ax_bars.c2p(x_width / 2, y_center)
            )

            bars.add(bar)





        #self.play(
        #    LaggedStart(
        #        *[DrawBorderThenFill(bar) for bar in bars],
        #        lag_ratio=0.1,
        #        run_time=3,
        #    )
        #)
        #for i in range(len(pixel_bins)):
        #    self.play(Transform(pixel_bins[i], bars[i]))
        #self.wait()
        #return
        self.play(LaggedStart(*[Transform(pixel_bins[i], bars[i]) for i in range(len(pixel_bins))]))

        self.play(FadeOut(ax), FadeOut(gridlines), pixels_edge.animate.move_to(ax))
        
        

        #self.add(p2)
        #self.add(ax, pixels, cbar, border)
        #self.wait()


        
        #self.move_camera(phi=40 * DEGREES, theta=-60 * DEGREES),
        
        self.wait()
        matrix = [[0, 1], [1, 0]]
        pixel_bins = VGroup(*pixel_bins)

        self.play(pixel_bins.animate.next_to(pixels_edge.get_bottom(), DOWN).shift(1.75*UP).rotate(PI/2), FadeOut(ax_bars))
        self.wait()

        cbar = (
            Rectangle(width=4, height=0.25, fill_opacity=1, color=YELLOW)
            .set_fill([BLACK, WHITE])
        )
        self.add(cbar.move_to(pixel_bins[0].get_left()))

        self.wait()


        return
        return
        self.play(cbar.animate.shift(6.5*LEFT))



        self.wait()
        
        # --- definiera bins ---

        bins = np.linspace(0, max(vals), n_bins)
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        # map pixelvärden → bin centers
        vals_sorted = np.array([pixels[i].val for i in idx_sorted])

        bin_idx = np.searchsorted(bins, vals_sorted, side='right') - 1
        bin_idx = np.clip(bin_idx, 0, len(bin_centers) - 1)

        vals_binned = bin_centers[bin_idx]

        
        self.play(
            *[
                pixels[i]
                .animate.scale((1,5,1)).move_to(ax.c2p(k, vals_binned[k]))
                for k, i in enumerate(idx_sorted)
            ],
            run_time=2,
        )
        self.wait()


        # --- STACKING ---
        stack_pos = np.zeros(len(vals_sorted))
        counts = np.zeros(len(bin_centers), dtype=int)

        for k, b in enumerate(bin_idx):
            stack_pos[k] = counts[b]
            counts[b] += 1

        self.play(
            *[
                pixels[i]
                .animate.move_to(ax.c2p(stack_pos[k], vals_binned[k]))
                for k, i in enumerate(idx_sorted)
            ],
            run_time=2,
        )

        self.wait()

        matrix = [[0, 1], [1, 0]]

        self.play(
            *[
                pixels[i].animate.apply_matrix(matrix, about_point=ax.get_center())
                for i in range(len(pixels))
            ],
            ax.animate.apply_matrix(matrix, about_point=ax.get_center()),
            cbar.animate.apply_matrix(matrix, about_point=ax.get_center()),
            run_time=2,
        )

        self.wait(2)
        g1 = Group(pixels, cbar)
        
        self.play(
            image_group.animate.move_to(ORIGIN).shift(1*UP),
            g1.animate.move_to(ORIGIN).shift(2.25*DOWN),
            FadeOut(ax),
            run_time=2,
            )
        self.wait()

        
        return

        #self.add(*[dot for dot in dots])



        
        
        self.wait()

        self.play(*[
            Transform(d1, d2)
            for d1, d2 in zip(pixels, dots_sorted)
        ])

        self.wait()

        return
        self.play(*[
            Transform(d1, d2)
            for d1, d2 in zip(pixels, dots)
        ])

        self.wait()

        return
        self.play(*[
            Transform(d1, d2)
            for d1, d2 in zip(dots, dots_sorted_stacked)
        ])
        self.wait()


        #h0 = ax.plot_line_graph(x_values=idxx_sorted, y_values=vals_sorted)
        #self.add(h0)
        #pixels = _position_matrix_voxelvise(

        #    mat=mat,
        #    mask=np.ones(mat.shape, dtype=bool),
        #    image_width=6,
        #    plot_max=mat.max(),
        #    offset_from_origin=(3.5, 0, 0),
        #    colormap='gray_r'
        #)
        #self.add(pixels)
        
        #xhist, yhist = get_histogram_traces_from_mat(
        #    mat=mat,
        #    mask=np.ones(mat.shape, dtype=bool),
        #    nbins=100,
        #    plot_max=mat.max(),

        #)

        #h0 = ax.plot_line_graph(
        #    y_values=yhist, x_values=xhist, add_vertex_dots=False
        #)
        #self.add(h0)

        

        return

if __name__ == "__main__":
    pixel_width, pixel_height = RESOLUTIONS[RESOLUTION]

    SCENE_NAME = Path(__file__).stem

    # Mapp för just denna rendering
    media_path = os.path.join("manim", "outputs", SCENE_NAME)
    os.makedirs(media_path, exist_ok=True)

    with tempconfig(
        {
            "pixel_width": pixel_width,
            "pixel_height": pixel_height,
            "frame_rate": FPS,
            "preview": PREVIEW,
            "background_color": BACKGROUND_COLOR,
            "output_file": SCENE_NAME,
            "media_dir": media_path,
        }
    ):
        start = time.time()
        scene = BuildScene()
        scene.render()

        print(f"elapsed time: {np.round((time.time() - start) / 60, 1)} min)")