import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.units import inch

# ----------------------------
# Load dataset
# ----------------------------
file_path = "C:/Users/jacqu/Desktop/Research/Projects/BIOSSCOPE/Particle_Experiments/Joined_PR_PR2_Files/POM_PR_PR2_PR3.csv"
df = pd.read_csv(file_path)

# ----------------------------
# Filter to T0 and summarize C/N (molar)
# ----------------------------
df_t0 = df[df["Timepoint"] == "T0"].copy()

summ = (
    df_t0.groupby(["Experiment", "Water_Amendment_Abr"], as_index=False)["C/N(molar)"]
    .agg(mean="mean", sd="std")
)

# ----------------------------
# Parse treatment labels
# ----------------------------
def parse_prefix(wt):
    if isinstance(wt, str) and wt.startswith("UE_"):
        return "UE"
    if isinstance(wt, str) and wt.startswith("M_"):
        return "M"
    return "Other"

def parse_base(wt):
    if not isinstance(wt, str):
        return "Other"
    if wt.endswith("_CT"):
        return "Control"
    if wt.endswith("_SP"):
        return "Surface Particles"
    if wt.endswith("_DP"):
        return "Deep Particles"
    return "Other"

summ["Prefix"] = summ["Water_Amendment_Abr"].apply(parse_prefix)
summ["Base"] = summ["Water_Amendment_Abr"].apply(parse_base)

# ----------------------------
# Ordering + color scheme (same as previous figures)
# ----------------------------
base_order = ["Control", "Surface Particles", "Deep Particles"]
prefix_order = ["UE", "M"]  # UE left, M right

colors_map = {
    ("Control", "M"): "black",
    ("Control", "UE"): "#7a7a7a",
    ("Surface Particles", "M"): "#8B0000",
    ("Surface Particles", "UE"): "#cc6a6a",
    ("Deep Particles", "M"): "#4B0082",
    ("Deep Particles", "UE"): "#9c7ac6",
}

summ["color"] = summ.apply(
    lambda r: colors_map.get((r["Base"], r["Prefix"]), "gray"), axis=1
)

# ----------------------------
# Build grouped x positions
# ----------------------------
experiments = list(pd.unique(summ["Experiment"]))

bar_width = 0.40
intra_offset = bar_width / 2
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

        for p in prefix_order:
            row = base_df[base_df["Prefix"] == p]
            if row.empty:
                continue
            row = row.iloc[0]
            xpos = group_center + (-intra_offset if p == "UE" else intra_offset)
            x_positions.append(xpos)
            plot_rows.append(row)

        x_labels.append(f"{exp}\n{b}")
        x += base_spacing

    x += exp_gap

plot_df = pd.DataFrame(plot_rows).reset_index(drop=True)

# Tick positions
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
# Create high-resolution PNG
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

# Minimal/Nature-style axes
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1)
ax.spines["bottom"].set_linewidth(1)

plt.xticks(tick_positions, x_labels, rotation=90)
plt.ylabel("C/N (molar) at T0")
plt.tight_layout()

png_path = "/mnt/data/POM_CN_molar_T0_highres.png"
plt.savefig(png_path, dpi=600, bbox_inches="tight")
plt.close()

# ----------------------------
# Embed PNG into PDF
# ----------------------------
pdf_path = "/mnt/data/POM_CN_molar_T0_high_quality.pdf"
doc = SimpleDocTemplate(pdf_path)
elements = [
    Image(png_path, width=6.5 * inch, height=4 * inch),
    Spacer(1, 0.2 * inch)
]
doc.build(elements)

print("Wrote:", pdf_path)
