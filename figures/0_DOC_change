import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.units import inch

# ----------------------------
# Load dataset
# ----------------------------
file_path = "C:/Users/jacqu/Desktop/Research/Projects/BIOSSCOPE/Particle_Experiments/Joined_PR_PR2_Files/DOC_TOC_PR_PR2_PR3.csv"
df = pd.read_csv(file_path)

# ----------------------------
# Compute replicate-level DOC change (TF - T0)
# ----------------------------
doc_df = df[df["DOC/TOC"] == "DOC"].copy()

rep_tbl = (
    doc_df.pivot_table(
        index=["Experiment", "Water_Treatment", "Replicate"],
        columns="Timepoint",
        values="µMC",
        aggfunc="mean"
    )
    .reset_index()
)

rep_tbl["DOC_change"] = rep_tbl["TF"] - rep_tbl["T0"]

# Mean + SD per Experiment × Water_Treatment
summ = (
    rep_tbl
    .groupby(["Experiment", "Water_Treatment"], as_index=False)["DOC_change"]
    .agg(mean="mean", sd="std")
)

# ----------------------------
# Parse treatment labels + colors (same as your prior figure)
# ----------------------------
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

base_order = ["Control", "Surface Particles", "Deep Particles"]
prefix_order = ["UE", "M"]  # UE left, M right

colors_map = {
    ("Control", "M"): "black",
    ("Control", "UE"): "#7a7a7a",              # light gray
    ("Surface Particles", "M"): "#8B0000",     # dark red
    ("Surface Particles", "UE"): "#cc6a6a",    # lighter red
    ("Deep Particles", "M"): "#4B0082",        # dark purple
    ("Deep Particles", "UE"): "#9c7ac6",       # lighter purple
}
summ["color"] = summ.apply(lambda r: colors_map.get((r["Base"], r["Prefix"]), "gray"), axis=1)

# ----------------------------
# Build x positions to match prior layout:
# within each experiment: Control -> Surface -> Deep
# within each base: UE then M (touching bars)
# ----------------------------
experiments = list(pd.unique(summ["Experiment"]))

bar_width = 0.40
intra_offset = bar_width / 2   # touching bars
base_spacing = 1.0
exp_gap = 0.9

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

        # one tick label per base group (centered)
        x_labels.append(f"{exp}\n{b}")
        x += base_spacing

    x += exp_gap

plot_df = pd.DataFrame(plot_rows).reset_index(drop=True)

# Tick positions at group centers
tick_positions = []
x = 0.0
for exp in experiments:
    exp_df = summ[summ["Experiment"] == exp]
    for b in base_order:
        if not exp_df[exp_df["Base"] == b].empty:
            tick_positions.append(x)
            x += base_spacing
    x += exp_gap

# ----------------------------
# Plot + save high-res PNG
# ----------------------------
plt.figure(figsize=(10, 6), dpi=300)

plt.bar(
    x_positions,
    plot_df["mean"].values,
    yerr=plot_df["sd"].values,
    width=bar_width,
    color=plot_df["color"].values,
    capsize=4
)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1)
ax.spines["bottom"].set_linewidth(1)

plt.xticks(tick_positions, x_labels, rotation=90)
plt.ylabel("Change in DOC (TF - T0, µMC)")
plt.tight_layout()

png_path = "/mnt/data/DOC_change_highres.png"
plt.savefig(png_path, dpi=600, bbox_inches="tight")
plt.close()

# ----------------------------
# Put PNG into a PDF (high-quality)
# ----------------------------
pdf_path = "/mnt/data/DOC_change_high_quality.pdf"
doc = SimpleDocTemplate(pdf_path)
elements = [
    Image(png_path, width=6.5 * inch, height=4 * inch),
    Spacer(1, 0.2 * inch)
]
doc.build(elements)

print("Wrote:", pdf_path)
