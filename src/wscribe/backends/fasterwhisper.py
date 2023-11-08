import math
import os
from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping, Optional

import numpy as np
import structlog
from faster_whisper import WhisperModel  # type: ignore
from tqdm import tqdm  # type: ignore

from ..core import Backend, TranscribedData
from ..writers import format_timestamp

DEFAULT_BEAM = 5
LOGGER = structlog.get_logger()


@dataclass(kw_only=True)
class FasterWhisperBackend(Backend):
    device: str = "cpu"  # cpu, cuda
    quantization: str = "int8"  # int8, float16
    model: WhisperModel | None = None

    def model_path(self) -> str:
        local_model_path = os.path.join(
            os.environ["WSCRIBE_MODELS_DIR"], f"faster-whisper-{self.model_size}"
        )

        if os.path.exists(local_model_path):
            return local_model_path
        else:
            raise RuntimeError(f"model not found in {local_model_path}")

    def load(self) -> None:
        self.model = WhisperModel(
            self.model_path(), device=self.device, compute_type=self.quantization
        )

    def transcribe(
        self,
        input: np.ndarray,
        language: Optional[str] = None,
        silent: bool = False,
        vad: bool = False,
    ) -> list[TranscribedData]:
        """
        Return word level transcription data.
        World level probabities are calculated by ctranslate2.models.Whisper.align
        """
        result: list[TranscribedData] = []
        assert self.model is not None
        segments, info = self.model.transcribe(
            input,
            beam_size=DEFAULT_BEAM,
            word_timestamps=True,
            language=language,
            vad_filter=vad,
        )
        # ps = playback seconds
        with tqdm(
            total=info.duration, unit_scale=True, unit="ps", disable=silent
        ) as pbar:
            for segment in segments:
                if segment.words is None:
                    continue
                segment_extract: TranscribedData = {
                    "text": segment.text,
                    "start": segment.start,
                    "end": segment.end,
                    "score": round(math.exp(segment.avg_logprob), 2),
                    "words": [
                        {
                            "start": w.start,
                            "end": w.end,
                            "text": w.word,
                            "score": round(w.probability, 2),
                        }
                        for w in segment.words
                    ],
                }
                result.append(segment_extract)
                if not silent:
                    pbar.update(segment.end - pbar.last_print_n)
        return result
