import asyncio
import os
from telethon import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

# Replace these with your actual API credentials from https://my.telegram.org
API_ID = 30962930 
API_HASH = 'd8ec5c8c5758bcb1f59d7c657a185a6f'
SESSION_NAME = 'user_session'

async def send_file_to_number(client: TelegramClient, phone_number: str, file_path: str | None, caption: str = ""):
    # Step 1: Format phone number (must include country code, e.g., '+1234567890')
    formatted_number = phone_number.strip().replace(" ", "")
    if not formatted_number.startswith("+"):
        formatted_number = f"+{formatted_number}"

    # Step 2: Import phone number as a contact to resolve the Telegram entity
    contact = InputPhoneContact(
        client_id=0,
        phone=formatted_number,
        first_name="Contact",
        last_name=""
    )

    result = await client(ImportContactsRequest([contact]))

    if not result.users:
        print(f"Failed to find a Telegram user associated with {phone_number}.")
        return

    target_user = result.users[0]

    # Step 3: Send the attachment or plain text message
    if file_path:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return

        await client.send_file(
            entity=target_user,
            file=file_path,
            caption=caption
        )
        print(f"Attachment successfully sent to {formatted_number}")
        return

    await client.send_message(entity=target_user, message=caption)
    print(f"Message successfully sent to {formatted_number}")

async def _send_message(phone_number: str, message: str, file_path: str | None = None):
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        await send_file_to_number(client, phone_number, file_path, message)


def send_message(phone_number: str, message: str, file_path: str | None = None):
    asyncio.run(_send_message(phone_number, message, file_path))
# from telethon import TelegramClient

# API_ID = 1234567 
# API_HASH = 'your_api_hash_here'
# SESSION_NAME = 'user_session'

# async def main():
#     async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
#         # Check if currently authorized
#         if await client.is_user_authorized():
#             print("Logging out...")
            
#             # Invalidates session on Telegram servers and deletes local session file
#             await client.log_out() 
            
#             print("Successfully logged out.")
#         else:
#             print("Client is not logged in.")

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())