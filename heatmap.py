import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import calmap
from datetime import datetime, timedelta

# Step 1: Get commit dates from Git (last 90 days)
log_output = subprocess.check_output(
    ["git", "log", "--since=90.days", "--pretty=format:%ad", "--date=short"]
).decode("utf-8")
dates = log_output.splitlines()

# Step 2: Prepare DataFrame with commit counts
df = pd.DataFrame(dates, columns=["date"])
df["date"] = pd.to_datetime(df["date"])
df["count"] = 1
daily = df.groupby("date")["count"].sum()

# Step 3: Plot with calmap (remove suptitle from here!)
fig, ax = calmap.calendarplot(
    daily,
    cmap='Greens',
    fillcolor='white',
    linewidth=1,
    fig_kws=dict(figsize=(12, 4))
)

# Force black background manually
fig.patch.set_facecolor("black")
for ax in np.ravel(axes):
    ax.set_facecolor("black") 
# Step 4: Add suptitle the correct way
plt.suptitle("Repo Commit Activity (Last 90 Days)", fontsize=12, fontweight='bold', color = 'white')

# Step 5: Save
plt.tight_layout()
plt.savefig("heatmap.png", dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
