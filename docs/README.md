
# Table of Contents

1.  [wscribe](#org1632b4f)
    1.  [Getting started](#orgd9a15cb)
        1.  [Installation](#orga61a0c4)
        2.  [Usage](#orge14eae7)
    2.  [Numbers](#orgf991a19)
    3.  [Roadmap](#orgc5a9de8)
        1.  [Processing Backends](#orge4bd8ac)
        2.  [Transcription Features](#org9d0954e)
        3.  [Inference interfaces](#org7e090eb)
        4.  [Audio sources](#orgff145da)
        5.  [Distribution](#org22885fe)
    4.  [Contributing](#orgefbdcb3)
        1.  [Testing](#orge2159a9)


<a id="org1632b4f"></a>

# wscribe


<a id="orgd9a15cb"></a>

## Getting started

`wscribe` is yet another easy to use front-end for [whisper](https://github.com/openai/whisper) specifically for transcription. It aims to be modular so that it can support multiple audio sources, processing backends and inference interfaces. It can run both on CPU and GPU based on the processing backend. Once transcript is generated, editing/correction/visualization of the transcript can be done manually with the [wscribe-editor](https://github.com/geekodour/wscribe-editor).

It was created at [sochara](https://www.sochara.org/) because we have a large volume of audio recordings that need to be transcribed and eventually archived. Another important need was that we needed to verify and manually edit the generated transcript, I could not find any open-source tool that checked all the boxes. Suggested workflow is generating word-level transcript(only supported in `json` export) and then editing the transcript with the [wscribe-editor](https://github.com/geekodour/wscribe-editor).

Currently, it supports the following. Check [roadmap](#orgc5a9de8) for upcoming support.

-   Processing backend: [faster-whisper](https://github.com/guillaumekln/faster-whisper)
-   Audio sources: Local files (Audio/Video)
-   Inference interfaces: Python CLI
-   File exports: JSON, SRT, WebVTT


<a id="orga61a0c4"></a>

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


<a id="orge14eae7"></a>

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


<a id="orgf991a19"></a>

## Numbers

-   These numbers are from machine under normal web-browsing workload running on a single RTX3050
-   Audio conversion takes around 1s
-   Also check [this explanation about the speed difference](https://github.com/ggerganov/whisper.cpp/issues/1127).

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">device</th>
<th scope="col" class="org-left">quant</th>
<th scope="col" class="org-left">model</th>
<th scope="col" class="org-left">original playback</th>
<th scope="col" class="org-left">transcription</th>
<th scope="col" class="org-right">playback/transcription</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">cuda</td>
<td class="org-left">float16</td>
<td class="org-left">tiny</td>
<td class="org-left">6.3m</td>
<td class="org-left">0.1m</td>
<td class="org-right">68x</td>
</tr>


<tr>
<td class="org-left">cuda</td>
<td class="org-left">float16</td>
<td class="org-left">small</td>
<td class="org-left">6.3m</td>
<td class="org-left">0.2m</td>
<td class="org-right">29x</td>
</tr>


<tr>
<td class="org-left">cuda</td>
<td class="org-left">float16</td>
<td class="org-left">medium</td>
<td class="org-left">6.3m</td>
<td class="org-left">0.4m</td>
<td class="org-right">14x</td>
</tr>


<tr>
<td class="org-left">cuda</td>
<td class="org-left">float16</td>
<td class="org-left">large-v2</td>
<td class="org-left">6.3m</td>
<td class="org-left">0.8m</td>
<td class="org-right">7x</td>
</tr>


<tr>
<td class="org-left">cpu</td>
<td class="org-left">int8</td>
<td class="org-left">tiny</td>
<td class="org-left">6.3m</td>
<td class="org-left">0.2m</td>
<td class="org-right">25x</td>
</tr>


<tr>
<td class="org-left">cpu</td>
<td class="org-left">int8</td>
<td class="org-left">small</td>
<td class="org-left">6.3m</td>
<td class="org-left">1.3m</td>
<td class="org-right">4x</td>
</tr>


<tr>
<td class="org-left">cpu</td>
<td class="org-left">int8</td>
<td class="org-left">medium</td>
<td class="org-left">6.3m</td>
<td class="org-left">3.6m</td>
<td class="org-right">~1.7x</td>
</tr>


<tr>
<td class="org-left">cpu</td>
<td class="org-left">int8</td>
<td class="org-left">large-v2</td>
<td class="org-left">6.3m</td>
<td class="org-left">3.6m</td>
<td class="org-right">~0.9x</td>
</tr>
</tbody>
</table>


<a id="orgc5a9de8"></a>

## Roadmap


<a id="orge4bd8ac"></a>

### Processing Backends

-   [X] [faster-whisper](https://github.com/guillaumekln/faster-whisper)
-   [ ] [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
-   [ ] [WhisperX](https://github.com/m-bain/whisperX), diarization is something to look forward to


<a id="org9d0954e"></a>

### Transcription Features

-   [ ] Add support for [diarization](https://github.com/guillaumekln/faster-whisper/issues/303)
-   [ ] Add translation
-   [ ] Add VAD/other de-noising stuff etc.
-   [ ] Add local llm integration with [llama.cpp](https://github.com/ggerganov/llama.cpp/pull/1773) or something similar for summary and [othe possible things](https://news.ycombinator.com/item?id=36900294). It can be also used to generate more accurate transcript. Whisper mostly generates sort of a subtitle, for [converting](https://www.reddit.com/r/MLQuestions/comments/ks5ez5/how_are_automatic_video_chapters_for_youtube/) subtitle [into transcription](https://www.reddit.com/r/accessibility/comments/xnfibv/most_accurate_way_to_turn_a_srt_file_into_a/) we need to group the subtitle. This can be done in various ways. Eg. By speaker if diarization is supported, by time chunks etc. By using LLMs or maybe other NLP techniques we&rsquo;ll also be able to do this with things like break in dialogue etc. Have to explore.


<a id="org7e090eb"></a>

### Inference interfaces

-   [-] Python CLI
    -   [X] Basic CLI
    -   [ ] Improve summary statistics
-   [ ] REST endpoint
    -   [ ] Basic server to run wscribe via an API.
    -   [ ] Possibly add glue code to expose it via CFtunnels or something similar


<a id="orgff145da"></a>

### Audio sources

-   [X] Local files
-   [ ] Youtube
-   [ ] Google drive


<a id="org22885fe"></a>

### Distribution

-   [X] Python packaging
-   [ ] Docker/Podman
-   [ ] Package for Nix
-   [ ] Package for Arch(AUR)


<a id="orgefbdcb3"></a>

## Contributing

All contribution happens through PRs, any contributions is greatly appreciated, bugfixes are welcome, features are welcome, tests are welcome, suggestions & criticism are welcome.


<a id="orge2159a9"></a>

### Testing

-   `make test`
-   See other helper commands in `Makefile`

