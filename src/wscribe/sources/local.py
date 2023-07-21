import os
from dataclasses import dataclass

from ..core import Audio


@dataclass(kw_only=True)
class LocalAudio(Audio):
    def __post_init__(self):
        self.fetch_audio()

    def fetch_audio(self):
        if os.path.exists(self.source):
            self.local_source_path = self.source
        else:
            raise RuntimeError("specified local path doesn't exist")
