import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Step 1: Get Git log
log_output = subprocess.check_output(
    ["git", "log", "--all", "--since=60.days", "--pretty=format:%ad", "--date=short"]
).decode("utf-8")

# Step 2: Parse dates
dates = log_output.splitlines()
df = pd.DataFrame(dates, columns=["date"])
df["count"] = 1
df = df.groupby("date").count().reset_index()

# Step 3: Full calendar
all_days = pd.date_range(end=datetime.now(), periods=60)
heat_df = pd.DataFrame({"date": all_days})
heat_df["date_str"] = heat_df["date"].dt.strftime("%Y-%m-%d")
df.rename(columns={"date": "commit_date"}, inplace = True)
heat_df = heat_df.merge(df, left_on="date_str", right_on="date", how="left").fillna(0)
heat_df["count"] = heat_df["count"].astype(int)
heat_df["dow"] = heat_df["date"].dt.weekday  # 0=Mon, 6=Sun
heat_df["week"] = heat_df["date"].dt.isocalendar().week

# Fix week/year edge cases
heat_df["year"] = heat_df["date"].dt.year
heat_df["week_year"] = heat_df["year"].astype(str) + "-W" + heat_df["week"].astype(str)

# Pivot table
pivot = heat_df.pivot(index="dow", columns="week_year", values="count")

# Step 4: Plot
plt.figure(figsize=(len(pivot.columns), 4))
sns.set(style="white")
ax = sns.heatmap(
    pivot,
    cmap="YlGn",
    linewidths=0.5,
    linecolor="lightgray",
    cbar=False,
    square=True,
    xticklabels=True,
    yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)
plt.xticks(rotation=45)
plt.title("Git Commit Activity (Last 60 Days)", fontsize=13, weight='bold')
plt.tight_layout()
plt.savefig("heatmap.png", dpi=300, bbox_inches='tight')
