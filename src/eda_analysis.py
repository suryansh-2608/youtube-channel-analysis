import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


video_df = pd.read_csv("../data/video_data.csv")


video_df['Published Date'] = pd.to_datetime(video_df['Published Date'])
video_df['Views'] = video_df['Views'].astype(int)
video_df['Likes'] = video_df['Likes'].astype(int)
video_df['Comments'] = video_df['Comments'].astype(int)

print("Data cleaned successfully!")


top_videos = video_df.sort_values(by='Views', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x='Views', y='Video Title', data=top_videos, palette="viridis")
plt.title('Top 10 Most Viewed Videos')
plt.xlabel('Views')
plt.ylabel('Video Title')
plt.tight_layout()
plt.savefig("../output/top_10_most_viewed.png")
plt.show()


video_df['Month'] = video_df['Published Date'].dt.to_period('M')

uploads_per_month = video_df.groupby('Month').size()

plt.figure(figsize=(12,6))
uploads_per_month.plot()
plt.title('Monthly Upload Trend')
plt.xlabel('Month')
plt.ylabel('Number of Videos')
plt.grid(True)
plt.tight_layout()
plt.savefig("../output/monthly_upload_trend.png")
plt.show()


video_df['Engagement Ratio'] = (video_df['Likes'] + video_df['Comments']) / video_df['Views']

top_engagement = video_df.sort_values(by='Engagement Ratio', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x='Engagement Ratio', y='Video Title', data=top_engagement, palette="magma")
plt.title('Top 10 Videos by Engagement Ratio')
plt.xlabel('Engagement Ratio')
plt.ylabel('Video Title')
plt.tight_layout()
plt.savefig("../output/top_10_engagement.png")
plt.show()

print("EDA visuals created and saved successfully!")
