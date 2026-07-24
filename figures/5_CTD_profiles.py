from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedLocator, FormatStrFormatter


# ============================================================
# USER SETTINGS
# ============================================================

# Folder containing the three input CSV files
input_folder = Path(
    r"C:\Users\jacqu\Desktop\CTD_profiles"
)

# Folder where the SVG figures will be saved
output_folder = input_folder / "CTD_figures_shared_axes"
output_folder.mkdir(parents=True, exist_ok=True)

# Input files and desired output names
casts = {
    "20230715_92315_002": input_folder / "20230715_92315_002_ctd.csv",
    "20250517_92511_014": input_folder / "20250517_92511_014_ctd.csv",
    "20240323_92408_016": input_folder / "20240323_92408_016_ctd.csv",
}

# Expected column names
depth_column = "Depth"
temperature_column = "Temp"
fluorescence_column = "Fluor_filt"
sigma_theta_column = "sig_theta"
mld_column = "MLD_dens125"

# Maximum plotted depth
maximum_depth = 500


# ============================================================
# SHARED AXIS LIMITS AND TICKS
# ============================================================

# All three figures use these same limits
temperature_limits = (15, 28)
fluorescence_limits = (-0.02, 0.25)
sigma_theta_limits = (23.5, 27.0)

# All three figures use these same tick positions
temperature_ticks = [15, 18, 21, 24, 27]

fluorescence_ticks = [
    0.00,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
]

sigma_theta_ticks = [
    23.5,
    24.0,
    24.5,
    25.0,
    25.5,
    26.0,
    26.5,
    27.0,
]

depth_ticks = [0, 100, 200, 300, 400, 500]


# ============================================================
# FONT AND VECTOR SETTINGS
# ============================================================

plt.rcParams.update(
    {
        # Arial should be available on Windows.
        "font.family": "Arial",
        "font.sans-serif": ["Arial"],

        # Keep text as editable text in SVG.
        "svg.fonttype": "none",

        # General styling
        "axes.linewidth": 2,
        "font.size": 16,
    }
)


# ============================================================
# PLOTTING FUNCTION
# ============================================================

def make_ctd_figure(
    data: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Create one CTD profile figure with three shared top x-axes:
    temperature, fluorescence, and sigma-theta.
    """

    required_columns = [
        depth_column,
        temperature_column,
        fluorescence_column,
        sigma_theta_column,
        mld_column,
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Convert required columns to numeric.
    plot_data = data[required_columns].copy()

    for column in required_columns:
        plot_data[column] = pd.to_numeric(
            plot_data[column],
            errors="coerce",
        )

    # Restrict to 0–500 m and remove rows missing profile data.
    plot_data = (
        plot_data.loc[
            plot_data[depth_column].between(
                0,
                maximum_depth,
            )
        ]
        .dropna(
            subset=[
                depth_column,
                temperature_column,
                fluorescence_column,
                sigma_theta_column,
            ]
        )
        .sort_values(depth_column)
    )

    if plot_data.empty:
        raise ValueError(
            "No valid profile data were found between "
            f"0 and {maximum_depth} m."
        )

    # Retrieve the first non-missing MLD value.
    mld_values = plot_data[mld_column].dropna()

    if len(mld_values) > 0:
        mixed_layer_depth = float(mld_values.iloc[0])
    else:
        mixed_layer_depth = None

    # --------------------------------------------------------
    # Create axes
    # --------------------------------------------------------

    fig, temperature_axis = plt.subplots(
        figsize=(5.4, 11.0)
    )

    fluorescence_axis = temperature_axis.twiny()
    sigma_theta_axis = temperature_axis.twiny()

    # Move the additional axes upward.
    fluorescence_axis.spines["top"].set_position(
        ("outward", 60)
    )

    sigma_theta_axis.spines["top"].set_position(
        ("outward", 120)
    )

    # --------------------------------------------------------
    # Plot profiles
    # --------------------------------------------------------

    temperature_axis.plot(
        plot_data[temperature_column],
        plot_data[depth_column],
        color="black",
        linewidth=4,
        solid_capstyle="round",
    )

    fluorescence_axis.plot(
        plot_data[fluorescence_column],
        plot_data[depth_column],
        color="forestgreen",
        linewidth=4,
        solid_capstyle="round",
    )

    sigma_theta_axis.plot(
        plot_data[sigma_theta_column],
        plot_data[depth_column],
        color="#6A0DAD",
        linewidth=4,
        solid_capstyle="round",
    )

    # --------------------------------------------------------
    # Mixed-layer-depth line
    # --------------------------------------------------------

    if (
        mixed_layer_depth is not None
        and 0 <= mixed_layer_depth <= maximum_depth
    ):
        temperature_axis.axhline(
            y=mixed_layer_depth,
            color="grey",
            linestyle="--",
            linewidth=2.5,
            zorder=0,
        )

    # --------------------------------------------------------
    # Shared limits
    # --------------------------------------------------------

    temperature_axis.set_xlim(
        temperature_limits
    )

    fluorescence_axis.set_xlim(
        fluorescence_limits
    )

    sigma_theta_axis.set_xlim(
        sigma_theta_limits
    )

    # Reverse depth axis so zero is at the top.
    temperature_axis.set_ylim(
        maximum_depth,
        0,
    )

    # --------------------------------------------------------
    # Axis labels
    # --------------------------------------------------------

    temperature_axis.set_xlabel(
        "Temperature (°C)",
        fontsize=20,
        fontweight="bold",
        color="black",
        labelpad=12,
        fontfamily="Arial",
    )

    fluorescence_axis.set_xlabel(
        "Fluorescence (RFU)",
        fontsize=20,
        fontweight="bold",
        color="forestgreen",
        labelpad=12,
        fontfamily="Arial",
    )

    sigma_theta_axis.set_xlabel(
        r"$\sigma_\theta$ (kg m$^{-3}$)",
        fontsize=20,
        fontweight="bold",
        color="#6A0DAD",
        labelpad=12,
        fontfamily="Arial",
    )

    temperature_axis.set_ylabel(
        "Depth (m)",
        fontsize=20,
        fontweight="bold",
        fontfamily="Arial",
    )

    # Place all x-axes at the top.
    for axis in [
        temperature_axis,
        fluorescence_axis,
        sigma_theta_axis,
    ]:
        axis.xaxis.tick_top()
        axis.xaxis.set_label_position("top")

    # --------------------------------------------------------
    # Fixed major ticks
    # --------------------------------------------------------

    temperature_axis.xaxis.set_major_locator(
        FixedLocator(temperature_ticks)
    )

    fluorescence_axis.xaxis.set_major_locator(
        FixedLocator(fluorescence_ticks)
    )

    sigma_theta_axis.xaxis.set_major_locator(
        FixedLocator(sigma_theta_ticks)
    )

    temperature_axis.yaxis.set_major_locator(
        FixedLocator(depth_ticks)
    )

    # Format fluorescence and sigma-theta labels consistently.
    fluorescence_axis.xaxis.set_major_formatter(
        FormatStrFormatter("%.2f")
    )

    sigma_theta_axis.xaxis.set_major_formatter(
        FormatStrFormatter("%.1f")
    )

    # --------------------------------------------------------
    # Minor ticks
    # --------------------------------------------------------

    temperature_axis.xaxis.set_minor_locator(
        AutoMinorLocator(3)
    )

    fluorescence_axis.xaxis.set_minor_locator(
        AutoMinorLocator(2)
    )

    sigma_theta_axis.xaxis.set_minor_locator(
        AutoMinorLocator(2)
    )

    temperature_axis.yaxis.set_minor_locator(
        AutoMinorLocator(2)
    )

    # --------------------------------------------------------
    # Tick styling
    # --------------------------------------------------------

    axis_styles = [
        (temperature_axis, "black"),
        (fluorescence_axis, "forestgreen"),
        (sigma_theta_axis, "#6A0DAD"),
    ]

    for axis, axis_color in axis_styles:

        axis.tick_params(
            axis="x",
            which="major",
            direction="in",
            colors=axis_color,
            labelsize=16,
            width=2,
            length=8,
            pad=6,
        )

        axis.tick_params(
            axis="x",
            which="minor",
            direction="in",
            colors=axis_color,
            width=1.5,
            length=4,
        )

        axis.spines["top"].set_color(axis_color)
        axis.spines["top"].set_linewidth(2)

        axis.spines["right"].set_visible(False)
        axis.spines["bottom"].set_visible(False)

    temperature_axis.tick_params(
        axis="y",
        which="major",
        direction="in",
        labelsize=16,
        width=2,
        length=8,
    )

    temperature_axis.tick_params(
        axis="y",
        which="minor",
        direction="in",
        width=1.5,
        length=4,
    )

    # Remove duplicate left spines from the extra axes.
    fluorescence_axis.spines["left"].set_visible(False)
    sigma_theta_axis.spines["left"].set_visible(False)

    # Explicitly set tick-label font to Arial.
    all_axes = [
        temperature_axis,
        fluorescence_axis,
        sigma_theta_axis,
    ]

    for axis in all_axes:
        for label in axis.get_xticklabels():
            label.set_fontfamily("Arial")
            label.set_fontsize(16)

        for label in axis.get_yticklabels():
            label.set_fontfamily("Arial")
            label.set_fontsize(16)

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    fig.subplots_adjust(
        left=0.22,
        right=0.95,
        bottom=0.06,
        top=0.60,
    )

    # --------------------------------------------------------
    # Save editable SVG
    # --------------------------------------------------------

    fig.savefig(
        output_path,
        format="svg",
        bbox_inches="tight",
        transparent=False,
    )

    plt.close(fig)


# ============================================================
# GENERATE ALL THREE FIGURES
# ============================================================

for cast_name, input_path in casts.items():

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    cast_data = pd.read_csv(input_path)

    output_path = output_folder / (
        f"{cast_name}_shared_axes_Arial.svg"
    )

    make_ctd_figure(
        data=cast_data,
        output_path=output_path,
    )

    print(f"Saved: {output_path}")


print("\nAll three figures were created successfully.")
