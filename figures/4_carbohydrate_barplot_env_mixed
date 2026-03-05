import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# 1) Load data
# --------------------------
file_path = "Neutral_Carb_RA_PR_PR2_Pump_20260305.csv"
df = pd.read_csv(file_path)

# --------------------------
# 2) Filter: environmental + mixed
# --------------------------
df_env = df[
    (df["sample_type"].astype(str).str.strip() == "environmental") &
    (df["condition"].astype(str).str.strip() == "mixed")
].copy()

# Carbohydrate columns (9)
carb_cols = [
    "Fucose", "Rhamnose", "Galactosamine", "Arabinose", "Glucosamine",
    "Galactose", "Glucose", "MannoseXylose", "Ribose"
]

# Ensure numeric
df_env["depth_m"] = pd.to_numeric(df_env["depth_m"], errors="coerce")
for c in carb_cols:
    df_env[c] = pd.to_numeric(df_env[c], errors="coerce")

# --------------------------
# 3) Depth bins
# --------------------------
bins = [0, 60, 120, 160, 500]
labels = ["0–60", "61–120", "121–160", "161–500"]

df_env = df_env[df_env["depth_m"].between(0, 500, inclusive="both")].copy()

df_env["Depth_bin"] = pd.cut(
    df_env["depth_m"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# --------------------------
# 4) Aggregate + normalize
# --------------------------
df_grouped = (
    df_env
    .dropna(subset=["Depth_bin"])
    .groupby("Depth_bin", as_index=False)[carb_cols]
    .mean()
)

# Normalize each bin to sum to 1
row_sums = df_grouped[carb_cols].sum(axis=1)
df_grouped.loc[row_sums > 0, carb_cols] = df_grouped.loc[row_sums > 0, carb_cols].div(
    row_sums[row_sums > 0], axis=0
)

# Fix bin order
df_grouped["Depth_bin"] = pd.Categorical(
    df_grouped["Depth_bin"], categories=labels, ordered=True
)

# --------------------------
# 5) Plot settings (match PR/PR2 panel spacing)
# --------------------------
custom_palette = [
    "#335c67",
    "#99a88c",
    "#fff3b0",
    "#f0c977",
    "#e09f3e",
    "#bf6535",
    "#9e2a2b",
    "#791b1d",
    "#540b0e"
]

# Reverse depth order for plotting
labels_rev = labels[::-1]
y = np.arange(len(labels_rev))

# Match PR/PR2 spacing ratio (PR/PR2 had two bars of height 0.35 => 0.70)
bar_height = 0.70

# --------------------------
# 6) Plot
# --------------------------
fig, ax = plt.subplots(figsize=(7, 5))

left = np.zeros(len(labels_rev))
for j, carb in enumerate(carb_cols):

    vals = []
    for b in labels_rev:
        s = df_grouped.loc[df_grouped["Depth_bin"] == b, carb]
        vals.append(float(s.values[0]) if len(s) else 0.0)

    ax.barh(
        y,
        vals,
        left=left,
        height=bar_height,
        color=custom_palette[j],
        edgecolor="black",
        linewidth=0.7,
        label=carb
    )
    left += np.array(vals)

ax.set_yticks(y)
ax.set_yticklabels(labels_rev)
ax.set_xlim(0, 1)
ax.set_xlabel("Relative Abundance")
ax.set_ylabel("Depth bin (m)")

# Square barplot area (legend excluded)
ax.set_box_aspect(1)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend outside
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

plt.tight_layout()

# --------------------------
# 7) Export
# --------------------------
out_pdf = "Environmental_mixed_depthbinned_carbohydrates_PRpanel_spacing.pdf"
plt.savefig(out_pdf, format="pdf", bbox_inches="tight")
plt.close()

print(f"Saved: {out_pdf}")
