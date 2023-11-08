import json
import logging
import os
import time

import click
import structlog

from wscribe.backends.fasterwhisper import FasterWhisperBackend
from wscribe.sources.local import LocalAudio

from ..core import SUPPORTED_MODELS
from ..writers import WRITERS

LOGGER = structlog.get_logger(ui="cli")


@click.group()
def cli():
    """CLI for audio transcription using faster-whisper"""
    pass


@cli.command()
@click.argument(
    "source",
    nargs=1,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.argument(
    "destination",
    nargs=1,
    type=click.Path(exists=False, resolve_path=True),
)
@click.option(
    "-f",
    "--format",
    help="destication file format, currently only json is supported",
    type=click.Choice(list(WRITERS.keys()), case_sensitive=True),
    default="json",
    show_default=True,
)
@click.option(
    "-m",
    "--model",
    help="model should already be downloaded",
    type=click.Choice(SUPPORTED_MODELS, case_sensitive=True),
    default="medium",
    show_default=True,
)
@click.option(
    "-g", "--gpu", help="enable gpu, disabled by default", default=False, is_flag=True
)
@click.option("-l", "--language", help="language code eg. en/fr (skips autodetection)")
@click.option("-d", "--debug", help="show debug logs", default=False, is_flag=True)
@click.option("-s", "--stats", help="print stats", default=False, is_flag=True)
@click.option("-q", "--quiet", help="no progress bar", default=False, is_flag=True)
@click.option(
    "-v",
    "--vad",
    help="use vad filter(better results, slower)",
    default=False,
    is_flag=True,
)
def transcribe(
    source, destination, format, model, gpu, language, debug, stats, quiet, vad
):
    """
    Transcribes SOURCE to DESTINATION. Where SOURCE can be local path to an audio/video file and
    DESTINATION needs to be a local path to a non-existing file.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG, force=True)
    log = LOGGER.bind(
        source=source, destination=destination, format=format, model=model, gpu=gpu
    )

    device, quantization = ("cuda", "float16") if gpu else ("cpu", "int8")
    m = FasterWhisperBackend(model_size=model, device=device, quantization=quantization)
    m.load()
    log.debug(f"model loaded with {device}-{quantization}")

    audio_start_time = time.perf_counter()
    audio = LocalAudio(source=source).convert_audio()
    audio_end_time = time.perf_counter()

    ts_start_time = time.perf_counter()
    result = m.transcribe(input=audio, language=language, silent=quiet, vad=vad)
    ts_end_time = time.perf_counter()

    writer = WRITERS[format](result=result, destination=destination)
    writer.write()

    if stats:
        original_audio_time = audio.shape[0] / LocalAudio.sampling_rate
        transcription_time = ts_end_time - ts_start_time
        audio_conversion_time = audio_end_time - audio_start_time
        click.echo(
            " | ".join(
                [
                    device,
                    quantization,
                    model,
                    str(round(audio_conversion_time, 1)) + "s",
                    str(round(original_audio_time / 60, 1)) + "m",
                    str(round(transcription_time / 60, 1)) + "m",
                    str(int(original_audio_time / transcription_time)) + "x",
                ]
            )
        )


@cli.command()
def info():
    """Information about related files and directories"""
    click.echo(f"WSCRIBE_MODELS_DIR: {os.environ['WSCRIBE_MODELS_DIR']}")


if __name__ == "__main__":
    cli()
