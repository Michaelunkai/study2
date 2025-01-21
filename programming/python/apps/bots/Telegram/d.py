import os
import asyncio
import pickle
import sqlite3
from telethon import TelegramClient
from telethon.errors import TimeoutError
from telethon.tl.types import PeerChannel
from tqdm import tqdm

# Telegram API credentials
api_id = 20973185
api_hash = 'f5abc64651ccb223151d42a0e984f131'
phone_number = '+972547632418'

# Basic paths
DOWNLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Downloads')
SESSION_FILE = 'session_name.session'
HISTORY_FILE = 'used_channel_ids.pkl'
SELECTIONS_FILE = 'used_download_selections.pkl'

def remove_locked_session():
    """Remove locked session if exists"""
    if os.path.exists(SESSION_FILE):
        try:
            conn = sqlite3.connect(SESSION_FILE)
            conn.close()
        except sqlite3.OperationalError:
            print("Removing locked session file...")
            try:
                os.remove(SESSION_FILE)
            except Exception as e:
                print(f"Error removing session: {e}")

async def list_channel_media(client, channel_id):
    """List all media in channel"""
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input('Enter the Telegram verification code: ')
        await client.sign_in(phone_number, code)

    try:
        channel = await client.get_entity(PeerChannel(int(channel_id)))
        media_messages = []
        async for message in client.iter_messages(channel):
            if message.file:
                media_messages.append(message)
        return media_messages
    except Exception as e:
        print(f"Error accessing channel: {e}")
        return None

async def download_file(message, file_path, retries=3):
    """Download file with progress bar"""
    for attempt in range(retries):
        try:
            file_size = message.file.size or 0
            desc = os.path.basename(file_path)

            with tqdm(total=file_size, unit='B', unit_scale=True, desc=desc) as progress_bar:
                def callback(current, total):
                    progress_bar.update(current - progress_bar.n)

                await message.download_media(file=file_path, progress_callback=callback)
            return True

        except TimeoutError:
            print(f"Timeout on attempt {attempt + 1}/{retries}")
        except Exception as e:
            print(f"Download error on attempt {attempt + 1}/{retries}: {e}")

        if attempt < retries - 1:
            await asyncio.sleep(5)
    return False

def parse_selection(input_str):
    """Parse user selection like '1-3,5,7-9'"""
    indices = []
    for part in input_str.replace(' ', '').split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            indices.extend(range(start, end + 1))
        else:
            indices.append(int(part))
    return indices

async def download_selected_files(client, channel_id, selected_indices):
    """Download selected files directly to download folder"""
    # Get media list
    media_list = await list_channel_media(client, channel_id)
    if not media_list:
        print("No media found in channel.")
        return

    # Create download directory if it doesn't exist
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    # Download selected files
    for idx in selected_indices:
        if not (1 <= idx <= len(media_list)):
            print(f"Invalid selection: {idx}")
            continue

        message = media_list[idx - 1]
        filename = message.file.name or f"file_{message.id}{message.file.ext}"

        # Handle duplicate filenames
        file_path = os.path.join(DOWNLOAD_PATH, filename)
        if os.path.exists(file_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(file_path):
                new_name = f"{base} ({counter}){ext}"
                file_path = os.path.join(DOWNLOAD_PATH, new_name)
                counter += 1

        print(f"\nDownloading: {filename}")
        if await download_file(message, file_path):
            print(f"Successfully downloaded: {file_path}")
        else:
            print(f"Failed to download: {filename}")

async def main():
    # Initialize
    remove_locked_session()

    # Load history
    try:
        with open(HISTORY_FILE, 'rb') as f:
            used_channels = pickle.load(f)
    except:
        used_channels = []

    # Load selections history
    try:
        with open(SELECTIONS_FILE, 'rb') as f:
            used_selections = pickle.load(f)
    except:
        used_selections = {}

    # Show previous channels
    if used_channels:
        print("Previously used channels:", ", ".join(used_channels))

    # Get channel ID
    channel_id = input("Enter channel ID: ")
    if channel_id not in used_channels:
        used_channels.append(channel_id)
        with open(HISTORY_FILE, 'wb') as f:
            pickle.dump(used_channels, f)

    # Initialize client
    async with TelegramClient(SESSION_FILE, api_id, api_hash) as client:
        # List available media
        media_list = await list_channel_media(client, channel_id)
        if not media_list:
            return

        # Show available files
        print("\nAvailable files:")
        for i, msg in enumerate(media_list, 1):
            filename = msg.file.name or f"file_{msg.id}{msg.file.ext}"
            print(f"{i}: {filename}")

        # Handle selection
        if channel_id in used_selections:
            prev_sel = used_selections[channel_id]
            use_prev = input(f"\nUse previous selection ({prev_sel})? (Y/n): ").lower()
            if use_prev in ('y', 'yes', ''):
                selected_indices = prev_sel
            else:
                selection = input("Enter file numbers (e.g., '1-3,5,7-9'): ")
                selected_indices = parse_selection(selection)
        else:
            selection = input("Enter file numbers (e.g., '1-3,5,7-9'): ")
            selected_indices = parse_selection(selection)

        # Save selection
        used_selections[channel_id] = selected_indices
        with open(SELECTIONS_FILE, 'wb') as f:
            pickle.dump(used_selections, f)

        # Download files
        await download_selected_files(client, channel_id, selected_indices)

if __name__ == '__main__':
    asyncio.run(main())
