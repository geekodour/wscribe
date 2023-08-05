from ctypes import Union
from dataclasses import dataclass
from typing import Any, Mapping, TypedDict

import numpy as np
import structlog
from faster_whisper.audio import decode_audio  # type: ignore

LOGGER = structlog.get_logger()
SUPPORTED_MODELS = ["tiny", "small", "medium", "large-v2"]

WordData = TypedDict(
    "WordData", {"text": str, "start": float | str, "end": float | str, "score": float}
)
TranscribedData = TypedDict(
    "TranscribedData",
    {
        "text": str,
        "start": float | str,
        "end": float | str,
        "score": float,
        "words": list[WordData],
    },
)


@dataclass(kw_only=True)
class Backend:
    name: str = "faster-whisper"
    model_size: str

    def __post_init__(self):
        if self.model_size not in self.supported_model_sizes():
            raise ValueError(f"model must be one of {self.supported_model_sizes()}")

    def supported_backends(self):
        """
        This is of not much use as of the moment, If we ever support multiple
        backends this can be utilized.
        """
        return ["faster-whisper"]

    def model_path(self) -> str:
        """
        Returns the local path to the model, error-out if unavailable
        """
        raise NotImplementedError()

    def supported_model_sizes(self) -> list[str]:
        return SUPPORTED_MODELS

    def load(self):
        raise NotImplementedError()

    def transcribe(self, input: np.ndarray) -> list[TranscribedData]:
        """
        This should return word level transcription data.
        """
        raise NotImplementedError()


@dataclass(kw_only=True)
class Audio:
    source: str
    local_source_path: str = ""
    sampling_rate: int = 16000

    def fetch_audio(self):
        """
        Fetches audio and sets local_source_path
        Should be implemented by inherited class
        """
        raise NotImplementedError()

    @staticmethod
    def determine_source_type(source: str) -> str:
        """
        regex match
        User is supposed to initialte appropriate class based on this
        """
        raise NotImplementedError()

    def convert_audio(self) -> np.ndarray:
        return decode_audio(self.local_source_path, split_stereo=False, sampling_rate=self.sampling_rate)  # type: ignore
