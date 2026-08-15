'''
Important: **Use headphones**. This script uses the system default audio
input and output, which often won't include echo cancellation. So to prevent
the model from interrupting itself it is important that you use headphones.

Before running this script, ensure the `GOOGLE_API_KEY`, `ELEVENLABS_API_KEY`,
and `MAPS_API_KEY` environment variables are set.
'''

import asyncio

from startup_config import load_and_require


async def main():
    load_and_require(("GOOGLE_API_KEY", "ELEVENLABS_API_KEY", "MAPS_API_KEY"))

    # Import after validation so missing configuration produces one clear error
    # before optional audio, ML, and cloud SDK dependencies initialize.
    from ADA.ADA_Online import ADA

    ada = ADA()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(ada.stt())
        input_message = tg.create_task(ada.input_message())
        tg.create_task(ada.send_prompt())
        tg.create_task(ada.tts())
        tg.create_task(ada.play_audio())

        await input_message


if __name__ == "__main__":
    asyncio.run(main())
