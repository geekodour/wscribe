#!/usr/bin/env bash
#
# A proper description
# of what this script does

# Tips
# - Running directory
#   - The script should be runnable from any directory
#   - If not, it should fail with a bang if run from the wrong directory
# - Default values
#   - Chaining: DOCKER_LABEL=${GIT_TAG:-${GIT_COMMIT_AND_DATE:-latest}}
# - [[  ]]
#   - Use [[ ]] for conditions in if/while, instead of [ ] or test
#   - if [ -f "$file" ] vs if [[ -f $file ]]
#   - if [ "$answer" = y -o "$answer" = yes ] vs if [[ $answer =~ ^y(es)?$ ]]
#   - Use (( … )) or $(( … )) for numericals
# - Misc
#   - Curly brackets { } don't create subshells, round brackets do
#   - Try making use of stdin & stdout redirection vs using filenames
#     - Redirect error echo to >&2
#   - use "local" variables

set -euo pipefail
# -e : common errors fatal, fail early (last command)
# -u : undefined variables are fatal
# -x : (optional) verbose log
# -o pipefail: if using |, exit code will be of the failed command
