import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Step 1: Get Git log
log_output = subprocess.check_output(
    ["git", "log", "--all", "--since=60.days", "--pretty=format:%ad", "--date=short"]
).decode("utf-8")

# Step 2: Parse commit dates
dates = log_output.splitlines()
df = pd.DataFrame(dates, columns=["commit_date"])  # ✅ Rename directly
df["count"] = 1
df = df.groupby("commit_date").count().reset_index()

# Step 3: Create full calendar DataFrame
all_days = pd.date_range(end=datetime.now(), periods=60)
heat_df = pd.DataFrame({"date": all_days})
heat_df["date_str"] = heat_df["date"].dt.strftime("%Y-%m-%d")

# ✅ Correct merge on renamed 'commit_date'
heat_df = heat_df.merge(df, left_on="date_str", right_on="commit_date", how="left").fillna(0)
heat_df["count"] = heat_df["count"].astype(int)

# Step 4: Add calendar fields
heat_df["dow"] = heat_df["date"].dt.weekday  # 0=Mon, 6=Sun
heat_df["week"] = heat_df["date"].dt.isocalendar().week
heat_df["year"] = heat_df["date"].dt.year
heat_df["week_year"] = heat_df["year"].astype(str) + "-W" + heat_df["week"].astype(str)

# Step 5: Pivot for heatmap
pivot = heat_df.pivot(index="dow", columns="week_year", values="count")

# Step 6: Plot
weeks = len(pivot.columns)
fig_width = weeks * 0.8
plt.figure(figsize=(fig_width, 4))
sns.set(style="white")
ax = sns.heatmap(
    pivot,
    cmap="YlGn",
    linewidths=0.3,
    linecolor="lightgray",
    cbar=False,
    square=False,
    xticklabels=True,
    yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)
plt.xticks(rotation=45, fontsize = 8)
plt.yticks(rotation=0, fontsize = 8)
plt.title("Git Commit Activity (Last 60 Days)", fontsize=10, weight='bold')
plt.tight_layout()
plt.savefig("heatmap.png", dpi=300, bbox_inches='tight')
