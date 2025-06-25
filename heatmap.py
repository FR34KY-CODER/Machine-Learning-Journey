import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Step 1: Get Git log
log_output = subprocess.check_output(
    ["git", "log", "--since=60.days", "--pretty=format:%ad", "--date=short"]
).decode("utf-8")

# Step 2: Process commit dates
dates = log_output.splitlines()
df = pd.DataFrame(dates, columns=["date"])
df["count"] = 1
df = df.groupby("date").count().reset_index()

# Step 3: Fill in missing days with 0s
all_days = pd.date_range(end=datetime.now(), periods=60).strftime("%Y-%m-%d")
heat_df = pd.DataFrame({"date": all_days})
heat_df = heat_df.merge(df, on="date", how="left").fillna(0)
heat_df["count"] = heat_df["count"].astype(int)
heat_df["date"] = pd.to_datetime(heat_df["date"])
heat_df["day"] = heat_df["date"].dt.dayofweek
heat_df["week"] = heat_df["date"].dt.strftime('%U')

# Step 4: Create pivot table
pivot = heat_df.pivot(index="day", columns="week", values="count")

# Step 5: Plot heatmap
plt.figure(figsize=(12, 3))
sns.set(style="whitegrid")
ax = sns.heatmap(
    pivot,
    cmap="Greens",         # 🔄 match GitHub’s green style
    linewidths=0.5,
    linecolor='lightgray',
    square=True,
    cbar=False,
    xticklabels=True,
    yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)

# Step 6: Aesthetics
plt.xticks(rotation=0)
plt.title("Commit Activity Heatmap", fontsize=14, weight='bold', pad=10)
plt.tight_layout()
plt.savefig("heatmap.png", dpi=300, bbox_inches='tight')
