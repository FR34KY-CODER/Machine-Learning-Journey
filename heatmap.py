import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Get last 60 days of commits
log_output = subprocess.check_output(
    ["git", "log", "--since=60.days", "--pretty=format:%ad", "--date=short"]
).decode("utf-8")

dates = log_output.splitlines()
df = pd.DataFrame(dates, columns=["date"])
df["count"] = 1
df = df.groupby("date").count().reset_index()

# Fill missing dates
all_days = pd.date_range(end=datetime.now(), periods=60).strftime("%Y-%m-%d")
heat_df = pd.DataFrame({"date": all_days})
heat_df = heat_df.merge(df, on="date", how="left").fillna(0)
heat_df["count"] = heat_df["count"].astype(int)
heat_df["date"] = pd.to_datetime(heat_df["date"])
heat_df["day"] = heat_df["date"].dt.dayofweek
heat_df["week"] = heat_df["date"].dt.isocalendar().week
pivot = heat_df.pivot("day", "week", "count")

# Plot and save
plt.figure(figsize=(12, 3))
sns.heatmap(pivot, cmap="YlGnBu", linewidths=1, linecolor="gray", cbar=False)
plt.title("Daily Git Commit Activity (Last 60 Days)")
plt.yticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], rotation=0)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("heatmap.png")  # ← IMPORTANT