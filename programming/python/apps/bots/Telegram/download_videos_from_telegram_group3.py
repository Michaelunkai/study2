import os
import asyncio
import re
import pickle
import sqlite3
import unicodedata
from telethon import TelegramClient
from telethon.errors import TimeoutError, ChannelPrivateError
from telethon.tl.types import PeerChannel
from tqdm import tqdm
from googletrans import Translator
import time
import shutil

# Replace these with your actual details
api_id = 20973185
api_hash = 'f5abc64651ccb223151d42a0e984f131'
phone_number = '+972547632418'

download_path = '/home/ubuntu/Downloads'
history_file = 'used_channel_ids.pkl'
session_file = 'session_name.session'
last_selection_file = 'last_selection.pkl'

def remove_locked_session(session_file):
    try:
        conn = sqlite3.connect(session_file)
        conn.close()
    except sqlite3.OperationalError:
        print("Session file is locked. Forcefully removing.")
        try:
            os.remove(session_file)
        except Exception as e:
            print(f"Error removing session file: {e}")

def clean_filename(filename):
    # Remove quality indicators and other common prefixes
    patterns = [
        r'4K\s*UHDTV\s*',
        r'1080[pP]\s*',
        r'720[pP]\s*',
        r'Zira[_ ]Media[_ ]',
        r'זירה[_ ]מדיה[_ ]',
    ]
    
    for pattern in patterns:
        filename = re.sub(pattern, '', filename)
    
    # Remove duplicate spaces
    filename = ' '.join(filename.split())
    return filename

def parse_episode_info(filename):
    # Handle various episode patterns
    episode_patterns = [
        (r'[Ee](\d+)[_ ][Pp](\d+)', lambda m: (1, int(m.group(2)))),  # E1_P2 or E1 P2
        (r'[Ee](\d+)פ(\d+)', lambda m: (1, int(m.group(2)))),         # E1פ2 (Hebrew)
        (r'ע(\d+)[_ ]פ(\d+)', lambda m: (1, int(m.group(2)))),        # ע1_פ2 (Hebrew)
        (r'[Pp](\d+)[_ ][Pp](\d+)', lambda m: (int(m.group(1)), int(m.group(2)))), # P1_P2
        (r'[Ss](\d+)[Ee](\d+)', lambda m: (int(m.group(1)), int(m.group(2)))),     # S1E2
    ]
    
    clean_name = clean_filename(filename)
    
    for pattern, handler in episode_patterns:
        match = re.search(pattern, clean_name)
        if match:
            return handler(match)
    
    return 1, 1  # Default to S01E01 if no pattern is found

async def translate_text(text):
    try:
        translator = Translator()
        time.sleep(1)  # Rate limiting
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def extract_show_name(filename):
    # Remove file extension
    name = os.path.splitext(filename)[0]
    
    # Remove episode information
    patterns = [
        r'[Ss]\d+[Ee]\d+',
        r'[Ee]\d+[_ ][Pp]\d+',
        r'[Pp]\d+[_ ][Pp]\d+',
        r'ע\d+[_ ]פ\d+',
        r'[Ee]\d+פ\d+',
    ]
    
    for pattern in patterns:
        name = re.sub(pattern, '', name)
    
    # Clean up the name
    name = clean_filename(name)
    return name.strip()

async def process_filename(original_filename):
    # Extract and translate show name if needed
    show_name = extract_show_name(original_filename)
    if not show_name.isascii():
        show_name = await translate_text(show_name)
    
    # Clean up show name
    show_name = clean_filename(show_name)
    
    # Get season and episode numbers
    season, episode = parse_episode_info(original_filename)
    
    # Get original extension
    ext = os.path.splitext(original_filename)[1]
    
    # Create Plex-compatible filename
    plex_filename = f"{show_name} - s{season:02d}e{episode:02d}{ext}"
    
    return show_name, season, episode, plex_filename

def create_directory_structure(base_path, show_name, season):
    # Create show directory
    show_path = os.path.join(base_path, show_name)
    if not os.path.exists(show_path):
        os.makedirs(show_path)
    
    # Create season directory
    season_path = os.path.join(show_path, f"Season {season:02d}")
    if not os.path.exists(season_path):
        os.makedirs(season_path)
    
    return season_path

async def download_with_retry(message, file_path, retries=3):
    for attempt in range(1, retries + 1):
        try:
            total_size = message.file.size or 0
            desc = os.path.basename(file_path)
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=desc) as pbar:
                def progress(current, total):
                    pbar.update(current - pbar.n)
                await message.download_media(file=file_path, progress_callback=progress)
            return True
        except TimeoutError:
            print(f"Timeout error while downloading {file_path}. Retrying... ({attempt}/{retries})")
        except Exception as e:
            print(f"Failed to download {file_path}: {e}. Retrying... ({attempt}/{retries})")
    return False

async def download_media(client, channel_id, selected_media_indices):
    media_list = await list_available_media(client, channel_id)
    if media_list is None:
        return

    selected_media = [media_list[int(index) - 1] for index in selected_media_indices if 0 < int(index) <= len(media_list)]

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for message in selected_media:
        try:
            # Get original filename
            original_filename = message.file.name or f"file_{message.id}{message.file.ext}"
            
            # Create temporary download path
            temp_path = os.path.join(download_path, f"temp_{original_filename}")
            
            # Download file to temporary location
            print(f"\nDownloading: {original_filename}")
            success = await download_with_retry(message, temp_path)
            if not success:
                print(f"Failed to download {original_filename} after 3 attempts.")
                continue
            
            # Process filename and get show information
            show_name, season, episode, plex_filename = await process_filename(original_filename)
            
            # Create proper directory structure
            final_dir = create_directory_structure(download_path, show_name, season)
            final_path = os.path.join(final_dir, plex_filename)
            
            # Handle existing files
            if os.path.exists(final_path):
                base, ext = os.path.splitext(plex_filename)
                counter = 1
                while os.path.exists(final_path):
                    plex_filename = f"{base} ({counter}){ext}"
                    final_path = os.path.join(final_dir, plex_filename)
                    counter += 1
            
            # Move file to final location
            shutil.move(temp_path, final_path)
            print(f"Successfully organized: {show_name}/Season {season:02d}/{plex_filename}")
            
            # Clean up any empty temporary files or directories
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error processing {original_filename}: {e}")
            continue

async def list_available_media(client, channel_id):
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            code = input('Please enter the code you received: ')
            await client.sign_in(phone_number, code)
        except Exception as e:
            print(f"Failed to log in: {e}")
            return None

    try:
        channel = await client.get_entity(PeerChannel(int(channel_id)))
    except ChannelPrivateError:
        print("Failed to retrieve channel: The channel is private, and you don't have access.")
        return None
    except ValueError:
        print("Failed to retrieve channel: Invalid channel ID format.")
        return None
    except Exception as e:
        print(f"Failed to retrieve channel: {e}")
        return None

    media_list = []
    async for message in client.iter_messages(channel):
        if message.video or message.file:
            media_list.append(message)
    return media_list

def parse_selection(selection):
    indices = []
    parts = selection.replace(' ', '').split(',')
    for part in parts:
        if '-' in part:
            start, end = part.split('-')
            start, end = int(start), int(end)
            indices.extend(range(start, end + 1))
        else:
            indices.append(int(part))
    return indices

async def main():
    if os.path.exists(session_file):
        remove_locked_session(session_file)

    if os.path.exists(history_file):
        with open(history_file, 'rb') as f:
            used_channel_ids = pickle.load(f)
    else:
        used_channel_ids = []

    if used_channel_ids:
        print("Previously used channel IDs: ", ", ".join(used_channel_ids))

    channel_id = input("Please enter the channel ID: ")

    if channel_id not in used_channel_ids:
        used_channel_ids.append(channel_id)
        with open(history_file, 'wb') as f:
            pickle.dump(used_channel_ids, f)

    client = TelegramClient(session_file, api_id, api_hash)

    try:
        await client.start(phone_number)
        media_list = await list_available_media(client, channel_id)

        if media_list:
            print("\nAvailable media:")
            for idx, message in enumerate(media_list, 1):
                filename = message.file.name or f"file_{message.id}{message.file.ext}"
                print(f"{idx}: {filename}")

            selected_indices_input = input("\nEnter the numbers of the media you want to download (e.g., '1-3,7-10'): ")
            selected_indices = parse_selection(selected_indices_input)

            await download_media(client, channel_id, selected_indices)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
