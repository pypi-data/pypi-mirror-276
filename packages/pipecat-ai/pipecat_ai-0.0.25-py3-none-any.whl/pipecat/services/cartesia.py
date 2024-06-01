#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from cartesia.tts import AsyncCartesiaTTS

import time
from typing import AsyncGenerator

from pipecat.frames.frames import AudioRawFrame, ErrorFrame, Frame
from pipecat.services.ai_services import TTSService

from loguru import logger


class CartesiaTTSService(TTSService):

    def __init__(
            self,
            *,
            api_key: str,
            voice_name: str,
            **kwargs):
        super().__init__(**kwargs)

        self._api_key = api_key
        self._voice_name = voice_name

        self._client = None

    async def run_tts(self, text: str) -> AsyncGenerator[Frame, None]:
        logger.debug(f"Transcribing text: [{text}]")

        try:
            if self._client is None:
                self._client = AsyncCartesiaTTS(api_key=self._api_key)
                voices = self._client.get_voices()
                self._voice_id = voices[self._voice_name]["id"]
                self._voice = self._client.get_voice_embedding(voice_id=self._voice_id)

            chunk_generator = await self._client.generate(
                transcript=text, voice=self._voice, stream=True,
                model_id="upbeat-moon", data_rtype='array', output_format='pcm_16000',
                # a chunk_time of 0.1 seems to be the default. there are small audio pops/gaps which
                # we need to debug
                chunk_time=0.1
            )

            async for chunk in chunk_generator:
                # print(f"")
                frame = AudioRawFrame(chunk['audio'], 16000, 1)
                yield frame
        except Exception as e:
            logger.error(f"Exception {e}")
