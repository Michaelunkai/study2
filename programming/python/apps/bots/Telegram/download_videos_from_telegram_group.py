import os
import asyncio
import re
from telethon import TelegramClient
from telethon.errors import TimeoutError, ChannelPrivateError
from telethon.tl.types import PeerChannel

# Your API ID and Hash from Telegram Developer Portal
api_id = <YOUR_API_ID>  # Replace with your API ID
api_hash = '<YOUR_API_HASH>'  # Replace with your API Hash
phone_number = '<YOUR_PHONE_NUMBER>'  # Replace with your phone number

# Path to save videos and files (Windows path)
download_path = r'<YOUR_DOWNLOAD_PATH>'  # Replace with your desired download path (e.g., C:\Users\yourname\Downloads)

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

# Function to sanitize the filename for Windows
def sanitize_filename(filename):
    # Remove invalid characters: \ / : * ? " < > |
    return re.sub(r'[\\/*?:"<>|]', "", filename)

async def download_media(channel_id):
    await client.connect()

    # If the client is not authorized, sign in with the phone number
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            # Automatically use a previously received code
            code = input('Please enter the code you received: ')
            await client.sign_in(phone_number, code)
        except Exception as e:
            print(f"Failed to log in: {e}")
            return

    # Get the channel by ID
    try:
        # Use PeerChannel to directly access the channel by ID
        channel = await client.get_entity(PeerChannel(int(channel_id)))
    except ChannelPrivateError:
        print(f"Failed to retrieve channel: The channel is private, and you don't have access.")
        return
    except ValueError:
        print(f"Failed to retrieve channel: Invalid channel ID format.")
        return
    except Exception as e:
        print(f"Failed to retrieve channel: {e}")
        return

    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Iterate over messages and download all 1080p videos and relevant files
    async for message in client.iter_messages(channel):
        # Check for video messages
        if message.video:
            # Check if the video has 1080p resolution
            for attr in message.video.attributes:
                if hasattr(attr, 'w') and hasattr(attr, 'h'):
                    if attr.w == 1920 and attr.h == 1080:
                        video_name = sanitize_filename(f"{message.file.name or message.id}.mp4")
                        video_path = os.path.join(download_path, video_name)

                        # Skip if file already exists
                        if os.path.exists(video_path):
                            print(f"Skipping {video_name} - already downloaded.")
                            continue

                        # Download video
                        print(f"Downloading 1080p video: {video_name}")
                        try:
                            await message.download_media(file=video_path)
                        except TimeoutError:
                            print(f"Timeout error while downloading {video_name}, retrying...")
                            try:
                                await message.download_media(file=video_path)
                            except TimeoutError:
                                print(f"Failed to download {video_name} after retrying.")

        # Check for other types of files
        elif message.file:
            file_name = sanitize_filename(f"{message.file.name or message.id}.{message.file.ext or 'dat'}")
            file_path = os.path.join(download_path, file_name)

            # Skip if file already exists
            if os.path.exists(file_path):
                print(f"Skipping {file_name} - already downloaded.")
                continue

            # Download the file
            print(f"Downloading file: {file_name}")
            try:
                await message.download_media(file=file_path)
            except TimeoutError:
                print(f"Timeout error while downloading {file_name}, retrying...")
                try:
                    await message.download_media(file=file_path)
                except TimeoutError:
                    print(f"Failed to download {file_name} after retrying.")

# Run the script
if __name__ == '__main__':
    channel_id = input("Please enter the channel ID: ")  # Ask the user for channel ID
    with client:
        client.loop.run_until_complete(download_media(channel_id))
