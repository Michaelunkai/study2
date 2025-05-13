import asyncio
from telethon import TelegramClient, functions, types

# Your API credentials
api_id = 20973185
api_hash = 'f5abc64651ccb223151d42a0e984f131'

async def archive_all_chats():
    # Create and start the client
    client = TelegramClient('archiver_session', api_id, api_hash)
    await client.start()
    
    print("Connected to Telegram...")
    
    # Get all dialogs (chats)
    dialogs = await client.get_dialogs()
    print(f"Fetched {len(dialogs)} dialogs")
    
    # Archive each chat
    count = 0
    for dialog in dialogs:
        # Skip already archived chats
        if hasattr(dialog, 'archived') and dialog.archived:
            continue
            
        try:
            # Archive the chat using the archiving method
            await client(functions.messages.ToggleDialogPinRequest(
                peer=dialog.input_entity,
                pinned=False
            ))
            
            await client(functions.folders.EditPeerFoldersRequest(
                folder_peers=[types.InputFolderPeer(
                    peer=dialog.input_entity,
                    folder_id=1  # 1 is the archive folder
                )]
            ))
            
            print(f"Archived: {dialog.name}")
            count += 1
        except Exception as e:
            print(f"Error archiving {dialog.name}: {e}")
    
    print(f"Successfully archived {count} chats")
    await client.disconnect()
    print("Disconnected from Telegram")

# Run the script
if __name__ == "__main__":
    try:
        asyncio.run(archive_all_chats())
    except Exception as e:
        print(f"Fatal error: {e}")
