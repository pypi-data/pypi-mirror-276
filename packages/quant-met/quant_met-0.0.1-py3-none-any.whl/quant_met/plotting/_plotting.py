import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.collections import LineCollection


def plot_into_bz(
    bz_corners, k_points, fig: plt.Figure | None = None, ax: plt.Axes | None = None
):
    if fig is None:
        fig, ax = plt.subplots()

    ax.scatter(*zip(*k_points))
    ax.scatter(*zip(*bz_corners), alpha=0.8)

    ax.set_aspect("equal", adjustable="box")

    return fig


def scatter_into_bz(
    bz_corners,
    k_points,
    data,
    fig: plt.Figure | None = None,
    ax: plt.Axes | None = None,
):
    if fig is None:
        fig, ax = plt.subplots()

    scatter = ax.scatter(*zip(*k_points), c=data, cmap="viridis")
    ax.scatter(*zip(*bz_corners), alpha=0.8)
    fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)

    ax.set_aspect("equal", adjustable="box")

    return fig


def plot_bcs_bandstructure(
    non_interacting_bands,
    deltas,
    k_point_list,
    ticks,
    labels,
    fig: plt.Figure | None = None,
    ax: plt.Axes | None = None,
):
    if fig is None:
        fig, ax = plt.subplots()

    ax.axhline(y=0, alpha=0.7, linestyle="--", color="black")

    for index, (band, delta) in enumerate(zip(non_interacting_bands, deltas)):
        ax.plot(
            k_point_list,
            np.sqrt(band**2 + np.abs(delta) ** 2),
            label=f"band {index}, +",
        )
        ax.plot(
            k_point_list,
            -np.sqrt(band**2 + np.abs(delta) ** 2),
            label=f"band {index}, -",
        )
    ax.set_box_aspect(1)

    ax.set_xticks(ticks, labels)
    ax.set_yticks(range(-5, 6))
    ax.set_facecolor("lightgray")
    ax.grid(visible=True)
    # ax.set_ylim([-5, 5])
    ax.tick_params(
        axis="both", direction="in", bottom=True, top=True, left=True, right=True
    )

    ax.legend()

    return fig, ax


def plot_nonint_bandstructure(
    bands,
    k_point_list,
    ticks,
    labels,
    overlaps: npt.NDArray | None = None,
    fig: plt.Figure | None = None,
    ax: plt.Axes | None = None,
):
    if fig is None:
        fig, ax = plt.subplots()

    ax.axhline(y=0, alpha=0.7, linestyle="--", color="black")

    if overlaps is None:
        for band in bands:
            ax.plot(k_point_list, band)
    else:
        line = None

        for band, wx in zip(bands, overlaps):
            points = np.array([k_point_list, band]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            norm = plt.Normalize(-1, 1)
            lc = LineCollection(segments, cmap="seismic", norm=norm)
            lc.set_array(wx)
            lc.set_linewidth(2)
            line = ax.add_collection(lc)

        colorbar = fig.colorbar(line, fraction=0.046, pad=0.04, ax=ax)
        color_ticks = [-1, 1]
        colorbar.set_ticks(ticks=color_ticks, labels=[r"$w_{\mathrm{Gr}_1}$", r"$w_X$"])

    ax.set_box_aspect(1)
    ax.set_xticks(ticks, labels)
    ax.set_yticks(range(-5, 6))
    ax.set_facecolor("lightgray")
    ax.grid(visible=True)
    # ax.set_ylim([-5, 5])
    ax.tick_params(
        axis="both", direction="in", bottom=True, top=True, left=True, right=True
    )

    return fig


def _generate_part_of_path(p_0, p_1, n, length_whole_path):
    distance = np.linalg.norm(p_1 - p_0)
    number_of_points = int(n * distance / length_whole_path) + 1

    k_space_path = np.vstack(
        [
            np.linspace(p_0[0], p_1[0], number_of_points),
            np.linspace(p_0[1], p_1[1], number_of_points),
        ]
    ).T[:-1]

    return k_space_path


def generate_bz_path(points=None, number_of_points=1000):
    n = number_of_points

    cycle = [
        np.linalg.norm(points[i][0] - points[i + 1][0]) for i in range(len(points) - 1)
    ]
    cycle.append(np.linalg.norm(points[-1][0] - points[0][0]))

    length_whole_path = np.sum(np.array([cycle]))

    ticks = [0]
    for i in range(0, len(cycle) - 1):
        ticks.append(np.sum(cycle[0 : i + 1]) / length_whole_path)
    ticks.append(1)
    labels = [rf"${points[i][1]}$" for i in range(len(points))]
    labels.append(rf"${points[0][1]}$")

    whole_path_plot = np.concatenate(
        [
            np.linspace(
                ticks[i],
                ticks[i + 1],
                num=int(n * cycle[i] / length_whole_path),
                endpoint=False,
            )
            for i in range(0, len(ticks) - 1)
        ]
    )

    points_path = [
        _generate_part_of_path(points[i][0], points[i + 1][0], n, length_whole_path)
        for i in range(0, len(points) - 1)
    ]
    points_path.append(
        _generate_part_of_path(points[-1][0], points[0][0], n, length_whole_path)
    )
    whole_path = np.concatenate(points_path)

    return whole_path, whole_path_plot, ticks, labels
