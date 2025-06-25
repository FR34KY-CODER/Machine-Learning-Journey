import subprocess
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Step 1: Get Git commit dates
log_output = subprocess.check_output(
    ["git", "log", "--all", "--since=90.days", "--pretty=format:%ad", "--date=short"]
).decode("utf-8")
dates = log_output.splitlines()
df = pd.DataFrame(dates, columns=["date"])
df["date"] = pd.to_datetime(df["date"])
df["count"] = 1
df = df.groupby("date").count().reset_index()

# Step 2: Fill in all days of range
start_date = datetime.now() - timedelta(days=90)
end_date = datetime.now()
all_days = pd.date_range(start=start_date, end=end_date)
full_df = pd.DataFrame({"date": all_days})
full_df = full_df.merge(df, on="date", how="left").fillna(0)
full_df["count"] = full_df["count"].astype(int)

# Step 3: Calendar fields
full_df["dow"] = full_df["date"].dt.weekday  # Monday=0
full_df["week"] = (full_df["date"] - full_df["date"].min()).dt.days // 7

# Step 4: Plot with Plotly
fig = px.imshow(
    full_df.pivot(index="dow", columns="week", values="count"),
    color_continuous_scale=["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"],
    aspect="auto",
)

# Step 5: Clean layout like GitHub
fig.update_layout(
    title="🟩 Repo Git Commit Heatmap (Last 90 Days)",
    xaxis_title=None,
    yaxis_title=None,
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=40, b=20),
    template="plotly_dark"
)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(
    tickvals=list(range(7)),
    ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    autorange="reversed"
)

# Save as PNG
fig.write_image("heatmap.png", width=800, height=200)
