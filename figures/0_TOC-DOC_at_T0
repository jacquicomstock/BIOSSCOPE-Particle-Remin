import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = "C:/Users/jacqu/Desktop/Research/Projects/BIOSSCOPE/Particle_Experiments/Joined_PR_PR2_Files/DOC_TOC_PR_PR2_PR3.csv"
df = pd.read_csv(file_path)

# Filter to T0
df_t0 = df[df["Timepoint"] == "T0"].copy()

# Replicate-level DOC/TOC wide table (so TOC-DOC is computed within replicate)
replicate_tbl = (
    df_t0.pivot_table(
        index=["Experiment", "Water_Treatment", "Replicate"],
        columns="DOC/TOC",
        values="µMC",
        aggfunc="mean"
    )
    .reset_index()
)

# Compute replicate-level TOC - DOC
replicate_tbl["TOC_minus_DOC"] = replicate_tbl["TOC"] - replicate_tbl["DOC"]

# Summarize mean and SD across replicates for each Experiment × Water_Treatment
summ = (
    replicate_tbl
    .groupby(["Experiment", "Water_Treatment"], as_index=False)["TOC_minus_DOC"]
    .agg(mean="mean", sd="std", n="count")
)

# Parse prefix (UE vs M) and base treatment (CT/SP/DP)
def parse_prefix(wt: str) -> str:
    if isinstance(wt, str) and wt.startswith("UE_"):
        return "UE"
    if isinstance(wt, str) and wt.startswith("M_"):
        return "M"
    return "Other"

def parse_base(wt: str) -> str:
    if not isinstance(wt, str):
        return "Other"
    if wt.endswith("_CT"):
        return "Control"
    if wt.endswith("_SP"):
        return "Surface Particles"
    if wt.endswith("_DP"):
        return "Deep Particles"
    return "Other"

summ["Prefix"] = summ["Water_Treatment"].apply(parse_prefix)
summ["Base"] = summ["Water_Treatment"].apply(parse_base)

# Ordering: Control → Surface → Deep, and within each pair UE → M
base_order = ["Control", "Surface Particles", "Deep Particles"]
prefix_order = ["UE", "M"]  # UE first (left), M second (right)

# Colors: UE lighter shades than M
colors = {
    ("Control", "M"): "black",
    ("Control", "UE"): "#7a7a7a",              # light gray (lighter than black)
    ("Surface Particles", "M"): "#8B0000",     # dark red
    ("Surface Particles", "UE"): "#cc6a6a",    # lighter red
    ("Deep Particles", "M"): "#4B0082",        # dark purple
    ("Deep Particles", "UE"): "#9c7ac6",       # lighter purple
}
summ["color"] = summ.apply(lambda r: colors.get((r["Base"], r["Prefix"]), "gray"), axis=1)

# Build grouped x positions with touching bars
experiments = list(pd.unique(summ["Experiment"]))

bar_width = 0.40          # bar width
intra_offset = bar_width / 2  # puts UE at -0.20 and M at +0.20 (touching)
base_spacing = 1.0        # spacing between Control/Surface/Deep group centers
exp_gap = 0.9             # extra gap between experiments

x_positions = []
x_labels = []
plot_rows = []

x = 0.0
for exp in experiments:
    exp_df = summ[summ["Experiment"] == exp]
    for b in base_order:
        base_df = exp_df[exp_df["Base"] == b]
        if base_df.empty:
            continue

        group_center = x

        # UE then M
        for p in prefix_order:
            row = base_df[base_df["Prefix"] == p]
            if row.empty:
                continue
            row = row.iloc[0]
            xpos = group_center + (-intra_offset if p == "UE" else intra_offset)
            x_positions.append(xpos)
            plot_rows.append(row)

        # tick label at group center (not per bar)
        x_labels.append(f"{exp}\n{b}")
        x += base_spacing

    x += exp_gap

plot_df = pd.DataFrame(plot_rows).reset_index(drop=True)

# Tick positions (centers for each group label)
tick_positions = []
x = 0.0
for exp in experiments:
    exp_df = summ[summ["Experiment"] == exp]
    for b in base_order:
        if not exp_df[exp_df["Base"] == b].empty:
            tick_positions.append(x)
            x += base_spacing
    x += exp_gap

# Plot (Nature-style minimal)
plt.figure()
plt.bar(
    x_positions,
    plot_df["mean"].values,
    yerr=plot_df["sd"].values,
    width=bar_width,
    color=plot_df["color"].values,
    capsize=3,
    linewidth=0
)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1)
ax.spines["bottom"].set_linewidth(1)
ax.tick_params(axis="both", width=1)

plt.xticks(tick_positions, x_labels, rotation=90, ha="center")
plt.ylabel("TOC - DOC (µMC) at T0")
plt.title("TOC minus DOC at T0 (UE then M within treatments)", fontsize=12)

plt.tight_layout()
plt.show()
