#!/usr/bin/env bash
#
# Runs wscribe with basic settings and diffent audio and prints reports to
# stdout

set -euo pipefail

# gpu
wscribe transcribe ./test.mp3 test.json -m tiny -g -q -s
wscribe transcribe ./test.mp3 test.json -m small -g -q -s
wscribe transcribe ./test.mp3 test.json -m medium -g -q -s
wscribe transcribe ./test.mp3 test.json -m large-v2 -g -q -s

# cpu
wscribe transcribe ./test.mp3 test.json -m tiny -q -s
wscribe transcribe ./test.mp3 test.json -m small -q -s
wscribe transcribe ./test.mp3 test.json -m medium -q -s
wscribe transcribe ./test.mp3 test.json -m large-v2 -q -s
