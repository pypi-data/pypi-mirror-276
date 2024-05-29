import pyperclip
import argparse
import time
import orjson
import pynput
from typing import Annotated, List, Optional, Callable
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Request, Body, Depends
from fastapi.responses import ORJSONResponse
import uvicorn
from icecream import ic


class Output:
    instance = None
    text_output_method: Callable[[str], None]

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

            keyboard = pynput.keyboard.Controller()

            def text_output_method(text: str):
                pyperclip.copy(text)
                keyboard.press(pynput.keyboard.Key.shift)
                time.sleep(0.01)
                keyboard.press(pynput.keyboard.Key.insert)
                time.sleep(0.05)
                keyboard.release(pynput.keyboard.Key.insert)
                time.sleep(0.01)
                keyboard.release(pynput.keyboard.Key.shift)

            cls.instance.text_output_method = text_output_method

        return cls.instance


def get_output() -> Optional[Output]:
    return Output()


class Text(BaseModel):
    text: str


app = FastAPI()


@app.post("/write/")
async def write(
    body: Annotated[
        Text,
        Body(
            openapi_examples={
                "short_audio": {
                    "summary": "A very short audio.",
                    "value": {"text": "Paste this"},
                }
            }
        ),
    ],
    output: Optional[Output] = Depends(get_output),
) -> bool:
    """Type the given message."""
    result = orjson.loads(body.text)
    text = result["text"]
    if text != "":
        text += " "
    output.text_output_method(text)
    return True


def main():
    """
    Main entry point for the for the paste server.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port-typing", type=int, default=8081, dest="port", help="Port to listen on"
    )
    args, _ = parser.parse_known_args()
    # Start the server
    uvicorn.run(app, host="localhost", port=args.port)


if __name__ == "__main__":
    main()
