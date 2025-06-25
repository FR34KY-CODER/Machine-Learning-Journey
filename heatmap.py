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
heat_df["day_of_week"] = heat_df["date"].dt.weekday # 0=Mon, 6=Sun
heat_df["week"] = (heat_df["date"] - heat_df["date"].min()).dt.days // 7 


# Step 5: Pivot for heatmap
pivot = heat_df.pivot(index="day_of_week", columns="week", values="count")

# Step 6: Plot
plt.style.use("dark_background")
sns.set(style="white")
fig, ax = plt.subplots(fissize=(pivot.shape[1]*0.6,4))
sns.heatmap(
    pivot,
    cmap=sns.color_palette("Greens", as_cmap=True),
    linewidths=1.2,
    linecolor="black",
    cbar=False,
    square=False,
    xticklabels=Falsee,
    yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)
# plt.xticks(rotation=90, fontsize = 5)
plt.yticks(rotation=0, fontsize = 7)
plt.title("Git Commit Activity", fontsize=10, weight='bold')
plt.tight_layout()
plt.savefig("heatmap.png", dpi=300, bbox_inches='tight')
