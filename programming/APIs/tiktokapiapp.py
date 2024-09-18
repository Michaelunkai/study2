from TikTokApi import TikTokApi

api = TikTokApi()

# The below code might need a try-except block to handle any potential errors
try:
    for video in api.trending():
        print(video['author']['username'])
except Exception as e:
    print("An error occurred:", e)
