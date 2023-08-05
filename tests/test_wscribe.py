import os

import pytest

from wscribe.backends.fasterwhisper import FasterWhisperBackend
from wscribe.sources.local import LocalAudio


class TestFastWhisper:
    def test_json(self, faster_whisper_tools):
        model, sample_path = faster_whisper_tools
        audio = LocalAudio(source=sample_path).convert_audio()
        model.load()
        data = model.transcribe(input=audio)
        assert set(data[0].keys()) == {"text", "start", "end", "score", "words"}
        assert set(data[0]["words"][0].keys()) == {
            "text",
            "start",
            "end",
            "score",
        }


@pytest.fixture
def faster_whisper_tools():
    model = FasterWhisperBackend(model_size="tiny", device="cpu", quantization="int8")
    sample_audio_path = os.path.join(
        os.environ["PROJECT_ROOT"], "examples", "assets", "jfk.wav"
    )
    return model, sample_audio_path
