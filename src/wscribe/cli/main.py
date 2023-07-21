import json
import logging
import os

import click
import structlog

from wscribe.backends.fasterwhisper import FasterWhisperBackend
from wscribe.sources.local import LocalAudio

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
    type=click.Choice(["json"], case_sensitive=True),
    default="json",
    show_default=True,
)
@click.option(
    "-m",
    "--model",
    help="model should already be downloaded",
    type=click.Choice(["small", "medium", "large-v2"], case_sensitive=True),
    default="medium",
    show_default=True,
)
@click.option(
    "-g", "--gpu", help="enable gpu, disabled by default", default=False, is_flag=True
)
@click.option("-d", "--debug", help="show debug logs", default=False, is_flag=True)
def transcribe(source, destination, format, model, gpu, debug):
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
    audio = LocalAudio(source=source).convert_audio()
    result = m.transcribe(input=audio)
    with open(destination, "w") as f:
        json.dump(result, f)


@cli.command()
def info():
    """Information about related files and directories"""
    click.echo(f"Model directory: {os.environ['WSCRIBE_MODELS_DIR']}")


if __name__ == "__main__":
    cli()
