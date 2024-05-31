"""2D plots of pymatgen structures with matplotlib.

plot_structure_2d() and its helpers get_rot_matrix() and unit_cell_to_lines() were
inspired by ASE https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html#matplotlib.
"""

from __future__ import annotations

import math
import warnings
from itertools import product
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch, Wedge
from matplotlib.path import Path
from pymatgen.analysis.local_env import CrystalNN, NearNeighbors
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from pymatviz.utils import ExperimentalWarning, covalent_radii, jmol_colors


if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any, Literal

    from numpy.typing import ArrayLike
    from pymatgen.core import Structure


def _angles_to_rotation_matrix(
    angles: str, rotation: ArrayLike | None = None
) -> ArrayLike:
    """Convert Euler angles to a rotation matrix.

    Note the order of angles matters. 50x,40z != 40z,50x.

    Args:
        angles (str): Euler angles (in degrees) formatted as '-10y,50x,120z'
        rotation (np.array, optional): Initial rotation matrix. Use this if you already
            have a rotation and want to combine it with the rotation defined by angles.
            Defaults to identity matrix np.eye(3).

    Returns:
        np.array: 3d rotation matrix.
    """
    if rotation is None:
        rotation = np.eye(3)

    # Return initial rotation matrix if no angles
    if not angles:
        return rotation.copy()

    for angle in angles.split(","):
        radians = math.radians(float(angle[:-1]))
        xyz = angle[-1]
        dim = "xyz".index(xyz)
        sin = math.sin(radians)
        cos = math.cos(radians)
        if dim == 0:
            rotation = np.dot(rotation, [(1, 0, 0), (0, cos, sin), (0, -sin, cos)])
        elif dim == 1:
            rotation = np.dot(rotation, [(cos, 0, -sin), (0, 1, 0), (sin, 0, cos)])
        else:
            rotation = np.dot(rotation, [(cos, sin, 0), (-sin, cos, 0), (0, 0, 1)])
    return rotation


def unit_cell_to_lines(cell: ArrayLike) -> tuple[ArrayLike, ArrayLike, ArrayLike]:
    """Convert lattice vectors to plot lines.

    Args:
        cell (np.array): Lattice vectors.

    Returns:
        tuple[np.array, np.array, np.array]:
        - Lines
        - z-indices that sort plot elements into out-of-plane layers
        - lines used to plot the unit cell
    """
    n_lines = n1 = 0
    segments = []
    for idx in range(3):
        norm = math.sqrt(sum(cell[idx] ** 2))
        segment = max(2, int(norm / 0.3))
        segments.append(segment)
        n_lines += 4 * segment

    lines = np.empty((n_lines, 3))
    z_indices = np.empty(n_lines, dtype=int)
    unit_cell_lines = np.zeros((3, 3))

    for idx in range(3):
        segment = segments[idx]
        dd = cell[idx] / (4 * segment - 2)
        unit_cell_lines[idx] = dd
        P = np.arange(1, 4 * segment + 1, 4)[:, None] * dd
        z_indices[n1:] = idx
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            n2 = n1 + segment
            lines[n1:n2] = P + i * cell[idx - 2] + j * cell[idx - 1]
            n1 = n2

    return lines, z_indices, unit_cell_lines


def plot_structure_2d(
    struct: Structure,
    *,
    ax: plt.Axes | None = None,
    rotation: str = "10x,10y,0z",
    atomic_radii: float | dict[str, float] | None = None,
    colors: dict[str, str | list[float]] | None = None,
    scale: float = 1,
    show_unit_cell: bool = True,
    show_bonds: bool | NearNeighbors = False,
    site_labels: bool
    | Literal["symbol", "species"]
    | dict[str, str | float]
    | Sequence[str | float] = True,
    label_kwargs: dict[str, Any] | None = None,
    bond_kwargs: dict[str, Any] | None = None,
    standardize_struct: bool | None = None,
    axis: bool | str = "off",
) -> plt.Axes:
    """Plot pymatgen structures in 2D with matplotlib.

    Inspired by ASE's ase.visualize.plot.plot_atoms()
    https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html#matplotlib
    pymatviz aims to give similar output to ASE but supports disordered structures and
    avoids the conversion hassle of AseAtomsAdaptor.get_atoms(pmg_struct).

    For example, these two snippets should give very similar output:

    ```python
    from pymatgen.ext.matproj import MPRester

    mp_19017 = MPRester().get_structure_by_material_id("mp-19017")

    # ASE
    from ase.visualize.plot import plot_atoms
    from pymatgen.io.ase import AseAtomsAdaptor

    plot_atoms(AseAtomsAdaptor().get_atoms(mp_19017), rotation="10x,10y,0z", radii=0.5)

    # pymatviz
    from pymatviz import plot_structure_2d

    plot_structure_2d(mp_19017)
    ```

    Multiple structures in single figure example:

    ```py
    import matplotlib.pyplot as plt
    from pymatgen.ext.matproj import MPRester
    from pymatviz import plot_structure_2d

    structures = [
        MPRester().get_structure_by_material_id(f"mp-{idx}") for idx in range(1, 5)
    ]
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    for struct, ax in zip(structures, axs.flat):
        plot_structure_2d(struct, ax=ax)
    ```

    Args:
        struct (Structure): Must be pymatgen instance.
        ax (plt.Axes, optional): Matplotlib axes on which to plot. Defaults to None.
        rotation (str, optional): Euler angles in degrees in the form '10x,20y,30z'
            describing angle at which to view structure. Defaults to "".
        atomic_radii (float | dict[str, float], optional): Either a scaling factor for
            default radii or map from element symbol to atomic radii. Defaults to
            covalent radii.
        colors (dict[str, str | list[float]], optional): Map from element symbols to
            colors, either a named color (str) or rgb(a) values like (0.2, 0.3, 0.6).
            Defaults to JMol colors (https://jmol.sourceforge.net/jscolors).
        scale (float, optional): Scaling of the plotted atoms and lines. Defaults to 1.
        show_unit_cell (bool, optional): Whether to plot unit cell. Defaults to True.
        show_bonds (bool | NearNeighbors, optional): Whether to plot bonds. If True, use
            pymatgen.analysis.local_env.CrystalNN to infer the structure's connectivity.
            If False, don't plot bonds. If a subclass of
            pymatgen.analysis.local_env.NearNeighbors, use that to determine
            connectivity. Options include VoronoiNN, MinimumDistanceNN, OpenBabelNN,
            CovalentBondNN, dtc. Defaults to True.
        site_labels (bool | "symbol" | "species" | dict[str, str | float] | Sequence):
            How to annotate lattice sites.
            If True, labels are element species (symbol + oxidation
            state). If a dict, should map species strings (or element symbols but looks
            for species string first) to labels. If a list, must be same length as the
            number of sites in the crystal. If a string, must be "symbol" or
            "species". "symbol" hides the oxidation state, "species" shows it
            (equivalent to True). Defaults to True.
        label_kwargs (dict, optional): Keyword arguments for matplotlib.text.Text like
            {"fontsize": 14}. Defaults to None.
        bond_kwargs (dict, optional): Keyword arguments for the matplotlib.path.Path
            class used to plot chemical bonds. Allowed are edgecolor, facecolor, color,
            linewidth, linestyle, antialiased, hatch, fill, capstyle, joinstyle.
            Defaults to None.
        standardize_struct (bool, optional): Whether to standardize the structure using
            SpacegroupAnalyzer(struct).get_conventional_standard_structure() before
            plotting. Defaults to False unless any fractional coordinates are negative,
            i.e. any crystal sites are outside the unit cell. Set this to False to
            disable this behavior which speeds up plotting for many structures.
        axis (bool | str, optional): Whether/how to show plot axes. Defaults to "off".
            See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axis for
            details.

    Raises:
        ValueError: On invalid site_labels.

    Returns:
        plt.Axes: matplotlib Axes instance with plotted structure.
    """
    ax = ax or plt.gca()

    if isinstance(site_labels, (list, tuple)) and len(site_labels) != len(struct):
        raise ValueError(
            f"If a list, site_labels ({len(site_labels)=}) must have same length as"
            f" the number of sites in the crystal ({len(struct)=})"
        )

    # Default behavior in case of no user input: standardize if any fractional
    # coordinates are negative
    has_sites_outside_unit_cell = any(any(site.frac_coords < 0) for site in struct)
    if standardize_struct is False and has_sites_outside_unit_cell:
        warnings.warn(
            "your structure has negative fractional coordinates but you passed "
            f"{standardize_struct=}, you may want to set standardize_struct=True",
            UserWarning,
        )
    elif standardize_struct is None:
        standardize_struct = has_sites_outside_unit_cell
    if standardize_struct:
        struct = SpacegroupAnalyzer(struct).get_conventional_standard_structure()

    # Get default colors
    if colors is None:
        colors = jmol_colors

    # Get any element at each site, only used for occlusion calculation which won't be
    # perfect for disordered sites. Plotting wedges of different radii for disordered
    # sites is handled later.
    elements_at_sites = [str(site.species.elements[0].symbol) for site in struct]

    if atomic_radii is None or isinstance(atomic_radii, float):
        # atomic_radii is a scaling factor for the default set of radii
        atomic_radii = 0.7 * covalent_radii * (atomic_radii or 1)
    elif missing := set(elements_at_sites) - set(atomic_radii):
        # atomic_radii is assumed to be a map from element symbols to atomic radii
        # make sure all present elements are assigned a radius
        raise ValueError(f"atomic_radii is missing keys: {missing}")

    radii_at_sites = np.array(
        [atomic_radii[el] for el in elements_at_sites]  # type: ignore[index]
    )

    # Generate lines for unit cell
    rotation_matrix = _angles_to_rotation_matrix(rotation)
    unit_cell = struct.lattice.matrix

    if show_unit_cell:
        lines, z_indices, unit_cell_lines = unit_cell_to_lines(unit_cell)
        corners = np.array(list(product((0, 1), (0, 1), (0, 1))))
        cell_vertices = np.dot(corners, unit_cell)
        cell_vertices = np.dot(cell_vertices, rotation_matrix)
    else:
        lines = np.empty((0, 3))
        z_indices = None
        unit_cell_lines = None
        cell_vertices = None

    # Zip atoms and unit cell lines together
    n_atoms = len(struct)
    n_lines = len(lines)

    positions = np.empty((n_atoms + n_lines, 3))
    site_coords = np.array([site.coords for site in struct])
    positions[:n_atoms] = site_coords
    positions[n_atoms:] = lines

    # Determine which unit cell line should be hidden behind other objects
    for idx in range(n_lines):
        this_layer = unit_cell_lines[z_indices[idx]]

        occluded_top = ((site_coords - lines[idx] + this_layer) ** 2).sum(
            1
        ) < radii_at_sites**2

        occluded_bottom = ((site_coords - lines[idx] - this_layer) ** 2).sum(
            1
        ) < radii_at_sites**2

        if any(occluded_top & occluded_bottom):
            z_indices[idx] = -1

    # Apply rotation matrix
    positions = np.dot(positions, rotation_matrix)
    rotated_site_coords = positions[:n_atoms]

    # Normalize wedge positions
    min_coords = (rotated_site_coords - radii_at_sites[:, None]).min(0)
    max_coords = (rotated_site_coords + radii_at_sites[:, None]).max(0)

    if show_unit_cell:
        min_coords = np.minimum(min_coords, cell_vertices.min(0))
        max_coords = np.maximum(max_coords, cell_vertices.max(0))

    means = (min_coords + max_coords) / 2
    coord_ranges = 1.05 * (max_coords - min_coords)

    offset = scale * (means - coord_ranges / 2)
    positions *= scale
    positions -= offset

    # Rotate and scale unit cell lines
    if n_lines > 0:
        unit_cell_lines = np.dot(unit_cell_lines, rotation_matrix)[:, :2] * scale

    special_site_labels = ("symbol", "species")
    # Sort positions by 3rd dim to plot from back to front along z-axis (out-of-plane)
    for idx in positions[:, 2].argsort():
        xy = positions[idx, :2]
        start = 0
        zorder = positions[idx][2]

        if idx < n_atoms:
            # Loop over all species on a site (usually just 1 for ordered sites)
            for species, occupancy in struct[idx].species.items():
                # Strip oxidation state from element symbol (e.g. Ta5+ to Ta)
                elem_symbol = species.symbol

                radius = atomic_radii[elem_symbol] * scale  # type: ignore[index]
                face_color = colors[elem_symbol]
                wedge = Wedge(
                    xy,
                    radius,
                    360 * start,
                    360 * (start + occupancy),
                    facecolor=face_color,
                    edgecolor="black",
                    zorder=zorder,
                )
                ax.add_patch(wedge)

                # Generate labels
                if site_labels == "symbol":
                    txt = elem_symbol
                elif site_labels in ("species", True):
                    txt = species
                elif site_labels is False:
                    txt = ""
                elif isinstance(site_labels, dict):
                    # Try element incl. oxidation state as dict key first (e.g. Na+),
                    # then just element as fallback
                    txt = site_labels.get(
                        repr(species), site_labels.get(elem_symbol, "")
                    )
                    if txt in special_site_labels:
                        txt = species if txt == "species" else elem_symbol
                elif isinstance(site_labels, (list, tuple)):
                    txt = site_labels[idx]  # idx runs from 0 to n_atoms
                else:
                    raise ValueError(
                        f"Invalid {site_labels=}. Must be one of (bool, "
                        f"{', '.join(special_site_labels)}, dict, list)"
                    )

                # Add labels
                if site_labels:
                    # Place element symbol half way along outer wedge edge for
                    # disordered sites
                    half_way = 2 * np.pi * (start + occupancy / 2)
                    direction = np.array([math.cos(half_way), math.sin(half_way)])
                    text_offset = (
                        (0.5 * radius) * direction if occupancy < 1 else (0, 0)
                    )

                    txt_kwds = dict(
                        ha="center",
                        va="center",
                        zorder=zorder,
                        **(label_kwargs or {}),
                    )
                    ax.text(*(xy + text_offset), txt, **txt_kwds)

                start += occupancy

        # Plot unit cell
        else:
            cell_idx = idx - n_atoms
            # Only plot lines not obstructed by an atom
            if z_indices[cell_idx] != -1:
                hxy = unit_cell_lines[z_indices[cell_idx]]
                path = PathPatch(Path((xy + hxy, xy - hxy)), zorder=zorder)
                ax.add_patch(path)

    if show_bonds:
        warnings.warn(
            "Warning: the show_bonds feature of plot_structure_2d() is experimental. "
            "Issues and PRs with improvements welcome.",
            category=ExperimentalWarning,
            stacklevel=2,
        )
        if show_bonds is True:
            neighbor_strategy_cls = CrystalNN
        elif issubclass(show_bonds, NearNeighbors):
            neighbor_strategy_cls = show_bonds
        else:
            raise ValueError(
                f"Expected boolean or a NearNeighbors subclass for {show_bonds = }"
            )

        # If structure doesn't have any oxidation states yet, guess them from chemical
        # composition. Use CrystalNN and other strategies to better estimate bond
        # connectivity. Use getattr on site.specie since it's often a pymatgen Element
        # which has no oxi_state
        if not any(
            hasattr(getattr(site, "specie", None), "oxi_state") for site in struct
        ):
            try:
                struct.add_oxidation_state_by_guess()
            except ValueError:  # fails for disordered structures
                # Charge balance analysis requires integer values in Composition
                pass

        structure_graph = neighbor_strategy_cls().get_bonded_structure(struct)

        bonds = structure_graph.graph.edges(data=True)
        for bond in bonds:
            from_idx, to_idx, data = bond
            if data["to_jimage"] != (0, 0, 0):
                continue  # skip bonds across periodic boundaries
            from_xy = positions[from_idx, :2]
            to_xy = positions[to_idx, :2]

            bond_patch = PathPatch(Path((from_xy, to_xy)), **(bond_kwargs or {}))
            ax.add_patch(bond_patch)

    width, height, _ = scale * coord_ranges
    ax.set(xlim=[0, width], ylim=[0, height], aspect="equal")
    ax.axis(axis)

    return ax
