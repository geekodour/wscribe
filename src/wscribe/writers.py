# Based on code from https://github.com/openai/whisper

import json
import os
import typing
from dataclasses import dataclass
from typing import Any, Mapping, TextIO


def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


@dataclass(kw_only=True)
class ResultWriter:
    result: Mapping[str, Any]
    destination: os.PathLike

    def write(self):
        with open(self.destination, "w", encoding="utf-8") as f:
            self._write_result(self.result, f)

    def _write_result(self, result: Mapping[str, Any], file: TextIO):
        raise NotImplementedError


@dataclass(kw_only=True)
class SubtitlesWriter(ResultWriter):
    always_include_hours: bool
    decimal_marker: str

    def iterate_result(self, result: Mapping[str, Any]):
        for segment in result["data"]:
            segment_start = self.format_timestamp(segment["start"])
            segment_end = self.format_timestamp(segment["end"])
            segment_text = segment["text"].strip()
            yield segment_start, segment_end, segment_text

    def format_timestamp(self, seconds: float):
        return format_timestamp(
            seconds=seconds,
            always_include_hours=self.always_include_hours,
            decimal_marker=self.decimal_marker,
        )


@dataclass(kw_only=True)
class WriteSRT(SubtitlesWriter):
    always_include_hours: bool = True
    decimal_marker: str = ","

    def _write_result(self, result: Mapping[str, Any], file: TextIO):
        for i, (start, end, text) in enumerate(self.iterate_result(result), start=1):
            print(f"{i}\n{start} --> {end}\n{text}\n", file=file, flush=True)


@dataclass(kw_only=True)
class WriteVTT(SubtitlesWriter):
    always_include_hours: bool = False
    decimal_marker: str = "."

    def _write_result(self, result: Mapping[str, Any], file: TextIO):
        print("WEBVTT\n", file=file)
        for start, end, text in self.iterate_result(result):
            print(f"{start} --> {end}\n{text}\n", file=file, flush=True)


@dataclass(kw_only=True)
class WriteJSON(ResultWriter):
    def _write_result(self, result: Mapping[str, Any], file: TextIO):
        self.transform_result(result)
        json.dump(result, file)

    def transform_result(self, result: Mapping[str, Any]):
        for s in result["data"]:
            s["start"] = self.format_timestamp(s["start"])
            s["end"] = self.format_timestamp(s["end"])
            s["text"] = s["text"].strip()
            if len(s["words"]) > 0:
                for w in s["words"]:
                    w["start"] = self.format_timestamp(w["start"])
                    w["end"] = self.format_timestamp(w["end"])
                    w["text"] = w["text"].strip()

    def format_timestamp(self, seconds: float):
        return format_timestamp(seconds=seconds, always_include_hours=True)


WRITERS: Mapping[str, typing.Type[ResultWriter]] = {
    "json": WriteJSON,
    "srt": WriteSRT,
    "vtt": WriteVTT,
}
