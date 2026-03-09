import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# 1) Load data
# --------------------------
file_path = "Neutral_Carb_RA_PR_PR2_Pump_20260305.csv"
df = pd.read_csv(file_path)

# --------------------------
# 2) Filter PR2 + remove Control
# --------------------------
df_pr2 = df[
    (df["cruise"] == "PR2") &
    (df["Treatment"] != "Control")
].copy()

# Carbohydrate columns (9)
carb_cols = [
    "Fucose", "Rhamnose", "Galactosamine", "Arabinose", "Glucosamine",
    "Galactose", "Glucose", "MannoseXylose", "Ribose"
]

# Ensure numeric
for c in carb_cols:
    df_pr2[c] = pd.to_numeric(df_pr2[c], errors="coerce")

# --------------------------
# 3) Aggregate + normalize
# --------------------------
df_grouped = (
    df_pr2
    .groupby(["Water_Treatment", "Timepoint"], as_index=False)[carb_cols]
    .mean()
)

# Normalize each bar to sum to 1
row_sums = df_grouped[carb_cols].sum(axis=1)
df_grouped.loc[row_sums > 0, carb_cols] = df_grouped.loc[row_sums > 0, carb_cols].div(
    row_sums[row_sums > 0], axis=0
)

# Enforce y-axis order (TOP -> BOTTOM after invert_yaxis)
treatment_order = ["UE SP", "M SP", "UE DP", "M DP"]
df_grouped = df_grouped[df_grouped["Water_Treatment"].isin(treatment_order)].copy()

df_grouped["Water_Treatment"] = pd.Categorical(
    df_grouped["Water_Treatment"],
    categories=treatment_order,
    ordered=True
)

df_grouped = df_grouped.sort_values(["Water_Treatment", "Timepoint"])

# --------------------------
# 4) Plot settings
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

y = np.arange(len(treatment_order))
bar_h = 0.35

# --------------------------
# 5) Plot (horizontal stacked bars)
#    T0 ABOVE TF within each treatment
# --------------------------
fig, ax = plt.subplots(figsize=(7, 5))

for tp in ["T0", "TF"]:
    subset = df_grouped[df_grouped["Timepoint"] == tp]
    left = np.zeros(len(treatment_order))

    # T0 above TF (before invert_yaxis)
    ypos = y - bar_h/2 if tp == "T0" else y + bar_h/2

    for j, carb in enumerate(carb_cols):
        vals = []
        for tr in treatment_order:
            s = subset.loc[subset["Water_Treatment"] == tr, carb]
            vals.append(float(s.values[0]) if len(s) else 0.0)

        ax.barh(
            ypos,
            vals,
            height=bar_h,
            left=left,
            color=custom_palette[j],
            edgecolor="black",
            linewidth=0.7,
            label=carb if tp == "T0" else None  # legend once
        )
        left += np.array(vals)

# Axis labels/limits
ax.set_yticks(y)
ax.set_yticklabels(treatment_order)
ax.set_xlim(0, 1)
ax.set_xlabel("Relative Abundance")

# Put UE SP at top and M DP at bottom
ax.invert_yaxis()

# Square plotting area (legend excluded)
ax.set_box_aspect(1)

# Minimalist styling
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend outside
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

plt.tight_layout()

# --------------------------
# 6) Export
# --------------------------
out_pdf = "PR2_carbohydrate_stacked_barplot_T0_above_TF_final.pdf"
plt.savefig(out_pdf, format="pdf", bbox_inches="tight")
plt.close()

print(f"Saved: {out_pdf}")
