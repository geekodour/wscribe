
# Table of Contents

1.  [wscribe](#orgb3cb7b6)
    1.  [Getting started](#org4bfa46d)
        1.  [Installation](#org32caff3)
        2.  [Usage](#org7f7ca72)
    2.  [Roadmap](#org7e84ad8)
        1.  [Processing Backends](#orgb5339b4)
        2.  [Transcription Features](#orga02a040)
        3.  [Inference interfaces](#org5455504)
        4.  [Audio sources](#org3caa573)
        5.  [Distribution](#orgd2b3566)
    3.  [Contributing](#org9388e9b)
        1.  [Testing](#org949fef2)


<a id="orgb3cb7b6"></a>

# wscribe


<a id="org4bfa46d"></a>

## Getting started

`wscribe` is yet another easy to use front-end for [whisper](https://github.com/openai/whisper) specifically for transcription. It aims to be modular so that it can support multiple audio sources, processing backends and inference interfaces. It can run both on CPU and GPU based on the processing backend. Once transcript is generated, editing/correction/visualization of the transcript can be done manually with the [wscribe-editor](https://github.com/geekodour/wscribe-editor).

It was created at [sochara](https://www.sochara.org/) because we have a large volume of audio recordings that need to be transcribed and eventually archived. Another important need was that we needed to verify and manually edit the generated transcript, I could not find any open-source tool that checked all the boxes. Suggested workflow is generating word-level transcript(only supported in `json` export) and then editing the transcript with the [wscribe-editor](https://github.com/geekodour/wscribe-editor).

Currently, it supports the following. Check [roadmap](#org7e84ad8) for upcoming support.

-   Processing backend: [faster-whisper](https://github.com/guillaumekln/faster-whisper)
-   Audio sources: Local files (Audio/Video)
-   Inference interfaces: Python CLI
-   File exports: JSON, SRT, WebVTT


<a id="org32caff3"></a>

### Installation

These instructions were tested on `NixOS:Python3.10` and `ArchLinux:Python3.10` but should work for any other OS, if you face any installation issues please feel free to [create issues](https://github.com/geekodour/wscribe/issues). I&rsquo;ll try to put out a docker image sometime.

1.  1. Set required env var

    -   `WSCRIBE_MODELS_DIR` : Path to the directory where whisper models should be downloaded to.
    
        export WSCRIBE_MODELS_DIR=$XDG_DATA_HOME/whisper-models # example

2.  2. Download the models

    1.  Recommended
    
        -   Recommended way for downloading the models is to use the [helper script](https://github.com/geekodour/wscribe/blob/main/scripts/fw_dw_hf_wo_lfs.sh), it&rsquo;ll download the models to `WSCRIBE_MODELS_DIR`.
            
                cd /tmp # temporary script, only needed to download the models
                curl https://raw.githubusercontent.com/geekodour/wscribe/main/scripts/fw_dw_hf_wo_lfs.sh
                chmod u+x fw_dw_hf_wo_lfs.sh
                ./fw_dw_hf_wo_lfs.sh tiny # other models: tiny, small, medium and large-v2
    
    2.  Manual
    
        You can download the models directly [from here](https://huggingface.co/guillaumekln) using `git lfs`, make sure you download/copy them to `WSCRIBE_MODELS_DIR`

3.  3. Install wscribe

    Assuming you already have a working `python>=3.10` setup
    
        pip install wscribe


<a id="org7f7ca72"></a>

### Usage

    # wscribe transcribe [OPTIONS] SOURCE DESTINATION
    
    # cpu
    wscribe transcribe audio.mp3 transcription.json
    # use gpu
    wscribe transcribe video.mp4 transcription.json --gpu
    # use gpu, srt format
    wscribe transcribe video.mp4 transcription.srt -g -f srt
    # use gpu, srt format, tiny model
    wscribe transcribe video.mp4 transcription.vtt -g -f vtt -m tiny
    wscribe transcribe --help # all help info


<a id="org7e84ad8"></a>

## Roadmap


<a id="orgb5339b4"></a>

### Processing Backends

-   [X] [faster-whisper](https://github.com/guillaumekln/faster-whisper)
-   [ ] [whisper.cpp](https://github.com/ggerganov/whisper.cpp), also see [this explanation about the speed difference](https://github.com/ggerganov/whisper.cpp/issues/1127).
-   [ ] [WhisperX](https://github.com/m-bain/whisperX), diarization is something to look forward to


<a id="orga02a040"></a>

### Transcription Features

-   [ ] Add support for [diarization](https://github.com/guillaumekln/faster-whisper/issues/303)
-   [ ] Add VAD/other de-noising stuff etc.
-   [ ] Add local llm integration with [llama.cpp](https://github.com/ggerganov/llama.cpp/pull/1773) or something similar for summary and [othe possible things](https://news.ycombinator.com/item?id=36900294). It can be also used to generate more accurate transcript. Whisper mostly generates sort of a subtitle, for converting subtitle into transcription we need to group the subtitle. This can be done in various ways. Eg. By speaker if diarization is supported, by time chunks etc. By using LLMs or maybe other NLP techniques we&rsquo;ll also be able to do this with things like break in dialogue etc. Have to explore.


<a id="org5455504"></a>

### Inference interfaces

-   [-] Python CLI
    -   [X] Basic CLI
    -   [ ] Improve summary statistics
-   [ ] REST endpoint
    -   [ ] Basic server to run wscribe via an API.
    -   [ ] Possibly add glue code to expose it via CFtunnels or something similar


<a id="org3caa573"></a>

### Audio sources

-   [X] Local files
-   [ ] Youtube
-   [ ] Google drive


<a id="orgd2b3566"></a>

### Distribution

-   [X] Python packaging
-   [ ] Docker/Podman
-   [ ] Package for Nix
-   [ ] Package for Arch(AUR)


<a id="org9388e9b"></a>

## Contributing

All contribution happens through PRs, any contributions is greatly appreciated, bugfixes are welcome, features are welcome, tests are welcome, suggestions & criticism are welcome.


<a id="org949fef2"></a>

### Testing

-   `make test`
-   See other helper commands in `Makefile`

