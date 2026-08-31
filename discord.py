import requests
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1543884411005833237/YHIVbH38NciyHXQpJfoqybxg94WOwGtxVf_b8nNQkij-JzRUddhyXKqkxTBy9lpty_io"


def send_discord_message(message, file_paths=None):
    data = {
        "content": message
    }

    opened_files = []
    files = []

    try:
        for i, path in enumerate(file_paths or []):
            f = open(path, "rb")
            opened_files.append(f)

            files.append(
                (
                    f"file{i}",
                    (os.path.basename(path), f)
                )
            )

        response = requests.post(
            WEBHOOK_URL,
            data=data,
            files=files
        )

        if response.status_code in (200, 204):
            print("Message sent successfully!")
            return True

        print("Error:", response.status_code, response.text)
        return False

    finally:
        for f in opened_files:
            f.close()


send_discord_message(
    "Candidate documents 📎",
    [
        r"selenium_error_1788080085.png",
    ]
)