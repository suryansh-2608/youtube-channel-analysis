import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("📺 YouTube Channel Analysis Dashboard")
st.caption("Built by Suryansh")


channel_df = pd.read_csv("data/channel_stats.csv")
video_df = pd.read_csv("data/video_data.csv")


video_df['Published Date'] = pd.to_datetime(video_df['Published Date'])
video_df['Views'] = video_df['Views'].astype(int)
video_df['Likes'] = video_df['Likes'].astype(int)
video_df['Comments'] = video_df['Comments'].astype(int)


st.header("📈 Channel Overview")
st.metric("Channel Name", channel_df['Channel Name'][0])
st.metric("Subscribers", f"{int(channel_df['Subscribers'][0]):,}")
st.metric("Total Views", f"{int(channel_df['Total Views'][0]):,}")
st.metric("Total Videos", channel_df['Total Videos'][0])

st.divider()


st.subheader("🔥 Top 10 Most Viewed Videos")
top_videos = video_df.sort_values(by='Views', ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10,6))
sns.barplot(x='Views', y='Video Title', data=top_videos, palette="viridis", ax=ax1)
plt.title('Top 10 Most Viewed Videos')
st.pyplot(fig1)

st.divider()


st.subheader("📅 Upload Trend Over Time")
video_df['Month'] = video_df['Published Date'].dt.to_period('M')
uploads_per_month = video_df.groupby('Month').size()

fig2, ax2 = plt.subplots(figsize=(12,6))
uploads_per_month.plot(ax=ax2)
plt.title('Monthly Upload Trend')
plt.xlabel('Month')
plt.ylabel('Number of Videos')
plt.grid(True)
st.pyplot(fig2)

st.divider()


st.subheader("💬 Top 10 Videos by Engagement Ratio")
video_df['Engagement Ratio'] = (video_df['Likes'] + video_df['Comments']) / video_df['Views']
top_engagement = video_df.sort_values(by='Engagement Ratio', ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(10,6))
sns.barplot(x='Engagement Ratio', y='Video Title', data=top_engagement, palette="magma", ax=ax3)
plt.title('Top 10 Videos by Engagement')
st.pyplot(fig3)

st.success("✅ Dashboard Rendered Successfully!")
