import json
import os
import uuid
from dataclasses import asdict

import requests
from dotenv import load_dotenv

from notion_ai.types import HelpMeWrite

load_dotenv()


TOKEN_V2 = os.getenv("TOKEN_V2")
SPACE_ID = os.getenv("SPACE_ID")


class NotionAi:
    BASE_URI = "https://www.notion.so/api/v3"

    def __init__(self, token_v2: str, space_id: str):
        self.token_v2 = token_v2
        self.space_id = space_id
        self.client = requests.Session()
        self.client.headers.update(
            {
                "Content-Type": "application/json",
                "Cookie": f"token_v2={self.token_v2}",
            }
        )

    def _send_request(self, context: HelpMeWrite) -> str:
        response = self.client.post(
            f"{self.BASE_URI}/getCompletion",
            json={
                "id": str(uuid.uuid4()),
                "model": "openai-3",
                "spaceId": self.space_id,
                "isSpacePermission": False,
                "context": asdict(context),
            },
            stream=True,
            timeout=None,
        )
        return self._stream_handler(response)
    
    def _stream_handler(self, response: requests.Response) -> str:
        result = ""
        for chunk in response.iter_lines(decode_unicode=True):
            chunk_dict = json.loads(chunk)
            if chunk and chunk_dict["type"] == "success":
                result += chunk_dict["completion"]
        return result

    def help_me_write(self, prompt: str) -> str:
        return self._send_request(HelpMeWrite(prompt=prompt))


notion_ai_client = NotionAi(TOKEN_V2, SPACE_ID)
