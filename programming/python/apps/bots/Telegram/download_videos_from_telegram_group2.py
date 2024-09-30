import os
import asyncio
import re
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, SessionPasswordNeededError
from telethon.tl.types import PeerChannel
from tqdm import tqdm

# --------------------- Configuration ---------------------

# Replace these with your actual details from Telegram Developer Portal
api_id = 20973185  # Your API ID
api_hash = 'f5abc64651ccb223151d42a0e984f131'  # Your API Hash
phone_number = '+972547632418'  # Your phone number

# Path to save videos and files (Windows path)
download_path = r'C:\Users\micha\Downloads'  # Ensure this path exists or will be created

# ---------------------------------------------------------

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

def sanitize_filename(filename):
    """
    Remove invalid characters from filenames for Windows.
    """
    return re.sub(r'[\\/:*?"<>|]', '', filename)

def has_extension(filename, ext):
    """
    Check if the filename already has the specified extension.
    """
    return filename.lower().endswith(f".{ext.lower()}")

async def download_with_retry(message, file_path, retries=3):
    """
    Attempt to download media with a specified number of retries.
    """
    for attempt in range(1, retries + 1):
        try:
            # Initialize the progress bar
            with tqdm(
                total=message.file.size if message.file else None,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=os.path.basename(file_path),
                leave=False
            ) as pbar:
                def progress(current, total):
                    pbar.update(current - pbar.n)

                # Download the media with a progress callback
                await message.download_media(file=file_path, progress_callback=progress)
            print(f"✅ Successfully downloaded: {os.path.basename(file_path)}")
            return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt} - Failed to download {os.path.basename(file_path)}: {e}")
            if attempt < retries:
                            print(f"🔄 Retrying {attempt + 1}/{retries}...")
        else:
            print(f"❌ Failed to download {os.path.basename(file_path)} after {retries} attempts.")

    return False

async def list_media(channel):
    """
    Fetch and list all media files from the specified channel.
    Returns a list of tuples: (message, file_name)
    """
    media_files = []
    print("\n📥 Fetching media files from the channel...")
    async for message in client.iter_messages(channel):
        if message.media:
            # Handle cases where message.file may be None
            file_name = None
            ext = 'dat'  # Default extension if none is found

            if message.file:
                # Try to get the file name and extension
                base_name = message.file.name or f"{message.id}"
                ext = message.file.ext or ext
            else:
                # Fallback for messages without a file attribute
                base_name = f"{message.id}"

            if not has_extension(base_name, ext):
                file_name = sanitize_filename(f"{base_name}.{ext}")
            else:
                file_name = sanitize_filename(base_name)

            media_files.append((message, file_name))
    return media_files

async def select_files_to_download(media_files):
    """
    Display a numbered list of media files and allow the user to select which ones to download.
    Returns a list of selected media tuples.
    """
    if not media_files:
        print("❌ No media files found in the channel.")
        return []

    print("\n📄 List of Media Files:")
    for idx, (_, file_name) in enumerate(media_files, start=1):
        print(f"{idx}. {file_name}")

    print("\n📋 Enter the numbers of the files you want to download, separated by commas (e.g., 1,3,5):")
    selection = input("Your selection: ").strip()

    if not selection:
        print("❌ No selection made. Exiting.")
        return []

    try:
        selected_indices = [int(num.strip()) for num in selection.split(',')]
    except ValueError:
        print("❌ Invalid input. Please enter numbers separated by commas.")
        return []

    # Validate indices
    selected_media = []
    for idx in selected_indices:
        if 1 <= idx <= len(media_files):
            selected_media.append(media_files[idx - 1])
        else:
            print(f"⚠️ Invalid number: {idx}. Skipping.")

    return selected_media

async def download_selected_files(selected_media):
    """
    Download the selected media files.
    """
    if not selected_media:
        print("❌ No valid files selected for download.")
        return

    print("\n📥 Starting download of selected files...")
    for message, file_name in selected_media:
        file_path = os.path.join(download_path, file_name)

        # Skip if already downloaded
        if os.path.exists(file_path):
            print(f"⏭️ Skipping '{file_name}' - already exists.")
            continue

        # Download the file with retries
        print(f"🔽 Downloading '{file_name}'...")
        await download_with_retry(message, file_path)

    print("\n🎉 Download process completed.")

async def main():
    """
    Main function to orchestrate the downloading process.
    """
    await client.connect()

    # Authenticate if not already authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            code = input('🔑 Please enter the code you received: ').strip()
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input('🔒 Two-step verification enabled. Please enter your password: ').strip()
            await client.sign_in(password=password)
        except Exception as e:
            print(f"❌ Failed to log in: {e}")
            await client.disconnect()
            return

    # Prompt for the channel ID or username
    channel_id_input = input("\n📢 Please enter the channel ID or username (e.g., -1001638433296 or @channelusername): ").strip()

    # Retrieve the channel entity
    try:
        if channel_id_input.startswith('@'):
            channel = await client.get_entity(channel_id_input)
        else:
            # Attempt to parse as integer ID
            channel = await client.get_entity(PeerChannel(int(channel_id_input)))
    except ChannelPrivateError:
        print(f"❌ Failed to retrieve channel: The channel is private, and you don't have access.")
        await client.disconnect()
        return
    except ValueError:
        print(f"❌ Failed to retrieve channel: Invalid channel ID format.")
        await client.disconnect()
        return
    except Exception as e:
        print(f"❌ Failed to retrieve channel: {e}")
        await client.disconnect()
        return

    # Ensure the download directory exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Fetch and list media files
    media_files = await list_media(channel)

    if not media_files:
        print("❌ No media files found in the channel.")
        await client.disconnect()
        return

    # Allow user to select files to download
    selected_media = await select_files_to_download(media_files)

    # Download the selected files
    await download_selected_files(selected_media)

    # Disconnect the client
    await client.disconnect()

# Entry point of the script
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Script interrupted by user. Exiting...")

