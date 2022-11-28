import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def _create_colorbar(
    fig,
    im,
    ax,
    width="10%",
    height="100%",
    loc="center right",
    bbox_to_anchor=(0.1, 0, 1, 1),
    borderpad=0,
    orientation="vertical",
    ticks=None,
    label=None,
    binary=False,
    ticklabels=None,
    title=None,
):

    axins = inset_axes(
        ax,
        width=width,
        height=height,
        loc=loc,
        bbox_to_anchor=bbox_to_anchor,
        bbox_transform=ax.transAxes,
        borderpad=borderpad,
    )

    cbar = fig.colorbar(
        im,
        cax=axins,
        ticks=ticks,
        orientation=orientation,
        label=label,
    )

    if ticklabels is not None:
        cbar.set_ticklabels(ticklabels=ticklabels)

    if title is not None:
        cbar.ax.set_title(title)

    if binary:
        cbar.set_ticks(ticks=[1 / 4, 3 / 4])
        cbar.set_ticklabels(ticklabels=["excl", "incl"])

    return cbar


def _remove_ax_lines(
    ax,
    dirs=["left", "right", "top", "bottom"],
):
    for d in dirs:
        ax.spines[d].set_visible(False)


def _remove_ax_ticks(
    ax,
):
    ax.set(xticks=[], yticks=[])


def _set_ax_text(ax, xlabel=None, ylabel=None, title=None):

    ax.set_xlabel(xlabel) if xlabel is not None else None
    ax.set_ylabel(ylabel) if ylabel is not None else None
    ax.set_title(title) if title is not None else None


def _add_label_to_ax(
    ax,
    label,
    px=0.05,
    py=0.94,
    ha="left",
    va="top",
    fontsize=9,
    bbox=dict(boxstyle="round", ec="black", fc="white"),
):

    ax.text(
        px,
        py,
        s=label,
        ha=ha,
        va=va,
        fontsize=fontsize,
        transform=ax.transAxes,
        bbox=bbox,
    )


def _set_ax_line_color(ax, color, dirs=["left", "right", "top", "bottom"]):
    for d in dirs:
        ax.spines[d].set_color(color)


def _create_subplot(ax, mat, lims, cmap, xlabel, ylabel, title):

    im = ax.imshow(
        mat,
        vmin=lims[0],
        vmax=lims[1],
        cmap=cmap,
        interpolation=None,
    )
    ax.set(
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )
    return im


def _set_ax_shape(ax, shape, white=True):

    return ax.imshow(
        np.ones(shape), cmap=plt.cm.gray if white else plt.cm.binary, vmin=0, vmax=1
    )


def _plotdpi(dpi=124):
    return int(dpi)


def _create_bias_image(mean_image, ref, mask=None) -> np.array:
    """Helper function to create bias maps"""

    error_img = np.zeros(ref.shape)

    if mask is None:
        mask = ref != 0
    error_img[mask] = 100 * (mean_image[mask] - ref[mask]) / ref[mask]

    return error_img


def _create_percentage_diff_image(image, ref, mask):

    res = np.zeros(mask.shape)
    res[mask] = image[mask] * (100 / ref[mask])

    return res


def _draw_region_box(c, sx, sy):

    cx, cy = (c[0], c[1])

    trace_x = np.array(
        [
            cx - 0.5 * sx,
            cx - 0.5 * sx,
            cx + 0.5 * sx,
            cx + 0.5 * sx,
            cx - 0.5 * sx,
        ]
    )

    trace_y = np.array(
        [
            cy - 0.5 * sy,
            cy + 0.5 * sy,
            cy + 0.5 * sy,
            cy - 0.5 * sy,
            cy - 0.5 * sy,
        ]
    )

    return (
        trace_x.astype(np.int),
        trace_y.astype(np.int),
    )


def _select_matrix_from_box(image, trace_x, trace_y, stack=False):

    (xmin, xmax, ymin, ymax) = (
        trace_x.min(),
        trace_x.max(),
        trace_y.min(),
        trace_y.max(),
    )

    if stack:
        return image[:, ymin:ymax, xmin:xmax]
    return image[ymin:ymax, xmin:xmax]


def _plotsize(
    width=8.25,
    height=11.75,
    indent_width=0,
    indent_height=0,
):
    # defaults are a4 paper dimensions (inches)
    return (
        width - indent_width,
        height - indent_height,
    )


def _tex_str(string, bold=False):
    # note: replace \ with \\ in argument string
    if bold:
        return "\\textnormal{" + "\\textbf{" + string + "}}"
    return "\\textnormal{" + string + "}"


def _cmap_binary(
    c0="black",
    c1="white",
):
    "function to set binary color map (e.g. for image masks)"
    return matplotlib.colors.ListedColormap([c0, c1])


def _padding(
    array,
    xx,
    yy,
    constant_values=0,
):

    h, w = array.shape[0], array.shape[1]
    a = (xx - h) // 2
    aa = xx - a - h
    b = (yy - w) // 2
    bb = yy - b - w

    return np.pad(
        array,
        pad_width=((a, aa), (b, bb)),
        mode="constant",
        constant_values=constant_values,
    )
