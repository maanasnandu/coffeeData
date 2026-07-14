import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import seaborn as sns
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Connect to RDS
load_dotenv()
DB_ENDPOINT = os.getenv("DB_ENDPOINT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
db_url = f"postgresql://postgres:{DB_PASSWORD}@{DB_ENDPOINT}:5432/postgres"
engine = create_engine(db_url)
df = pd.read_sql("SELECT * FROM global_top_100_shops", engine)

# 2. Set the Artisanal Editorial Aesthetic
bg_color = '#F5F2EB'
text_color = '#222222'
subtext_color = "#6B675F"
indigo = '#2E4057'
copper = '#B87333'
canvas_grey = '#D9D5CF'
grid_color = "#E3DFD6"

plt.rcParams.update({
    'figure.facecolor': bg_color,
    'axes.facecolor': bg_color,
    'text.color': text_color,
    'axes.labelcolor': text_color,
    'xtick.color': text_color,
    'ytick.color': text_color,
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

def style_axes(ax, left_spine=False):
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_visible(left_spine)
    if not left_spine:
        ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# CHART 1: "Dumbell plot"
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# Filter for countries with 3+ shops
country_counts = df['country'].value_counts()
countries_3plus = country_counts[country_counts >= 3].index
df_3plus = df[df['country'].isin(countries_3plus)]

# Find the best (min) and worst (max) rank for each country
range_df = df_3plus.groupby('country')['rank'].agg(['min', 'max']).reset_index()
range_df = range_df.sort_values('min', ascending=False).reset_index(drop=True)

# Draw the connecting lines
ax.hlines(y=range_df.index, xmin=range_df['min'], xmax=range_df['max'], color=canvas_grey, linewidth=3, zorder=1)

# Draw the endpoints
ax.scatter(range_df['max'], range_df.index, color=canvas_grey, s=150, zorder=2)
ax.scatter(range_df['min'], range_df.index, color=copper, s=150, zorder=3)

# Add clear, exact labels
for i, row in range_df.iterrows():
    # Country label on the far left
    ax.text(row['min'] - 4, i, row['country'], va='center', ha='right', color=text_color, fontweight='bold',
            fontsize=11)

    # Best rank number inside the copper dot
    ax.text(row['min'], i, str(row['min']), va='center', ha='center', color='white', fontweight='bold', fontsize=8,
            zorder=4)

    # Worst rank number above the grey dot
    ax.text(row['max'], i + 0.25, f"#{row['max']}", va='bottom', ha='center', color=text_color, fontsize=10)

    # Find and label the best shop name for that country below the line
    best_shop = df[(df['country'] == row['country']) & (df['rank'] == row['min'])]['shop_name'].values[0]
    ax.text(row['min'], i - 0.35, best_shop, va='top', ha='left', color=indigo, fontsize=9, fontweight='bold')

# Clean up the axes completely
ax.set_title('The Ranking Range: Highest vs. Lowest Ranked Shops by Country', loc='left', fontsize=16,
             fontweight='bold', pad=20)
ax.text(0, 1.02, 'Showing countries with 3 or more shops in the Top 100.', transform=ax.transAxes, fontsize=11,
        color='#555555')
ax.set_xlim(-15, 105)
ax.axis('off')  # Turn off the confusing grid and borders completely

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, '1_rank_range_dumbbell.png'), dpi=300, bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# CHART 2: "Regional Concentration" (Faceted Ranks)
# ---------------------------------------------------------
# Take the top 6 countries by volume for the grid
top_6_countries = country_counts.nlargest(6).index
df_top6 = df[df['country'].isin(top_6_countries)].copy()

# Create a grid of subplots (2 rows, 3 columns)
fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
axes = axes.flatten()

for i, country in enumerate(top_6_countries):
    ax = axes[i]
    country_data = df_top6[df_top6['country'] == country].sort_values('rank')

    # Create an internal rank (1st, 2nd, 3rd within the country)
    country_data['internal_rank'] = range(1, len(country_data) + 1)

    bars = ax.barh(country_data['internal_rank'], country_data['rank'], color=indigo, height=0.5)

    ax.set_title(country, fontweight='bold', color=text_color, loc='left')
    ax.invert_yaxis()  # Put 1st place at the top
    ax.set_yticks(country_data['internal_rank'])
    ax.set_yticklabels([f"#{int(r)} Global" for r in country_data['rank']], fontsize=10, color=copper,
                       fontweight='bold')

    ax.tick_params(axis='both', length=0)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])

    # Add shop names precisely next to the bars
    for bar, name in zip(bars, country_data['shop_name']):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height() / 2, name,
                va='center', ha='left', fontsize=10, color=text_color)

fig.suptitle('Regional Concentration: Internal Rankings of Top Markets', fontsize=18, fontweight='bold', x=0.03,
             ha='left')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(BASE_DIR, '2_regional_concentration.png'), dpi=300, bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# CHART 3: "Coffee Superpowers" (Minimalist Bar)
# ---------------------------------------------------------
# fig, ax = plt.subplots(figsize=(10, 6))
#
# top_10_superpowers = country_counts.nlargest(10).sort_values(ascending=True)
#
# bars = ax.barh(top_10_superpowers.index, top_10_superpowers.values, color=indigo, height=0.6)
# for bar in bars:
#     width = bar.get_width()
#     ax.text(width + 0.2, bar.get_y() + bar.get_height() / 2, f'{int(width)}',
#             ha='left', va='center', color=text_color, fontweight='bold', fontsize=12)
#
# ax.set_title('Coffee Superpowers: Top 10 Countries by Shop Count', loc='left', fontsize=18, fontweight='bold', pad=20)
# ax.tick_params(axis='y', length=0, labelsize=12)
# ax.get_xaxis().set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
#
# plt.tight_layout()
# plt.savefig(os.path.join(BASE_DIR, '3_coffee_superpowers.png'), dpi=300, bbox_inches='tight')
# plt.close()




# ------------------------------
TOP_N = 15
top_countries = country_counts.head(TOP_N)
other_total = country_counts.iloc[TOP_N:].sum()
plot_data = top_countries.copy()
if other_total > 0:
    plot_data[f"Other ({country_counts.shape[0]-TOP_N} countries)"] = other_total

plot_data = plot_data.sort_values(ascending=True)  # smallest at bottom for barh

fig, ax = plt.subplots(figsize=(10, 8.5))

colors = [copper if name.startswith("Other") else indigo for name in plot_data.index]
bars = ax.barh(plot_data.index, plot_data.values, color=colors, height=0.65, zorder=3)

for bar, value in zip(bars, plot_data.values):
    ax.text(bar.get_width() + 0.6, bar.get_y() + bar.get_height() / 2, str(value),
            va="center", ha="left", fontsize=11, fontweight="bold", color=text_color)

ax.set_xlim(0, plot_data.max() * 1.15)
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.grid(axis="x", color=grid_color, linewidth=1, zorder=0)
style_axes(ax)
ax.set_xlabel("Number of shops in the Top 100", fontsize=11, color=subtext_color, labelpad=10)

fig.suptitle("Coffee Superpowers", x=0.06, y=0.97, ha="left",
             fontsize=22, fontweight="bold", color=text_color)
ax.set_title(f"Shops per country among the Global Top 100 ({TOP_N} largest shown individually)",
             loc="left", fontsize=12, color=subtext_color, pad=14)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig(os.path.join(BASE_DIR, "1_coffee_superpowers.png"), dpi=300, bbox_inches="tight")
plt.close()

print("Clean, editorial-grade charts successfully generated! ☕📊")