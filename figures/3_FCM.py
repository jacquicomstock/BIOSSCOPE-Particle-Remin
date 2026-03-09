import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.units import inch
import matplotlib.patches as mpatches

# ----------------------------
# Load dataset
# ----------------------------
file_path = ""C:/Users/jacqu/Desktop/Research/Projects/BIOSSCOPE/Particle_Experiments/AE2408/Biogeochem/PR2_FCM_noMF.csv""
df = pd.read_csv(file_path)

# Clean column names (some had leading/trailing spaces)
df.columns = df.columns.str.strip()

value_col = "Concentration (cells/mL)"

# ----------------------------
# Summarize mean + SD for each Water_Treatment × Timepoint
# ----------------------------
summ = (
    df.groupby(["Water_Treatment", "Timepoint"], as_index=False)[value_col]
      .agg(mean="mean", sd="std")
)

# ----------------------------
# Map treatments to your same color scheme
# NOTE: in this dataset EP = Surface, MP = Deep
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
    if wt.endswith("_EP"):   # EP = Surface Particles
        return "Surface Particles"
    if wt.endswith("_MP"):   # MP = Deep Particles
        return "Deep Particles"
    return "Other"

summ["Prefix"] = summ["Water_Treatment"].apply(parse_prefix)
summ["Base"]   = summ["Water_Treatment"].apply(parse_base)

# Strict ordering: Control → Surface → Deep; UE → M
base_order = ["Control", "Surface Particles", "Deep Particles"]
prefix_order = ["UE", "M"]

summ["Base"] = pd.Categorical(summ["Base"], categories=base_order, ordered=True)
summ["Prefix"] = pd.Categorical(summ["Prefix"], categories=prefix_order, ordered=True)
summ = summ.sort_values(["Base", "Prefix", "Water_Treatment", "Timepoint"])

colors_map = {
    ("Control", "M"): "black",
    ("Control", "UE"): "#7a7a7a",
    ("Surface Particles", "M"): "#8B0000",
    ("Surface Particles", "UE"): "#cc6a6a",
    ("Deep Particles", "M"): "#4B0082",
    ("Deep Particles", "UE"): "#9c7ac6",
}
summ["color"] = summ.apply(lambda r: colors_map.get((r["Base"], r["Prefix"]), "gray"), axis=1)

# Ordered treatment list for x-axis
ordered_treatments = (
    summ[["Water_Treatment", "Base", "Prefix"]]
      .drop_duplicates()
      .sort_values(["Base", "Prefix"])
)["Water_Treatment"].tolist()

# ----------------------------
# Build bar positions: T0 and TF next to each other
# TF gets hatch pattern
# ----------------------------
bar_width = 0.35
x_positions, means, errors, colors, hatches = [], [], [], [], []

x = 0
for wt in ordered_treatments:
    sub = summ[summ["Water_Treatment"] == wt]

    for tp, offset in zip(["T0", "TF"], [-bar_width/2, bar_width/2]):
        row = sub[sub["Timepoint"] == tp]
        if row.empty:
            continue

        x_positions.append(x + offset)
        means.append(row["mean"].values[0])
        errors.append(row["sd"].values[0])
        colors.append(row["color"].values[0])
        hatches.append("" if tp == "T0" else "///")

    x += 1

# ----------------------------
# Plot and save high-res PNG
# ----------------------------
plt.figure(figsize=(10, 6), dpi=300)

for xp, m, e, c, h in zip(x_positions, means, errors, colors, hatches):
    plt.bar(
        xp,
        m,
        yerr=e,
        width=bar_width,
        color=c,
        hatch=h,
        capsize=4
    )

plt.xticks(range(len(ordered_treatments)), ordered_treatments, rotation=90)
plt.ylabel(value_col)

# Legend (pattern indicates TF)
legend_elements = [
    mpatches.Patch(facecolor="white", edgecolor="black", label="T0"),
    mpatches.Patch(facecolor="white", edgecolor="black", hatch="///", label="TF"),
]
plt.legend(handles=legend_elements, title="Timepoint")

plt.tight_layout()

png_path = "/mnt/data/PR2_FCM_noMF_highres.png"
plt.savefig(png_path, dpi=600, bbox_inches="tight")
plt.close()

# ----------------------------
# Embed PNG into a PDF
# ----------------------------
pdf_path = "/mnt/data/PR2_FCM_noMF_high_quality.pdf"
doc = SimpleDocTemplate(pdf_path)
elements = [
    Image(png_path, width=6.5 * inch, height=4 * inch),
    Spacer(1, 0.2 * inch),
]
doc.build(elements)

print("Wrote:", pdf_path)
