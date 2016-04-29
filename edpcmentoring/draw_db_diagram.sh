#!/usr/bin/env bash
set -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "${PYTHON}" ]; then
    PYTHON=$(which python)
fi
if [ ! -x "${PYTHON}" ]; then
    echo "Python interpreter not found. Set PYTHON environment variable." >&2
    exit 1
fi


# A simple little script to draw a diagram of a subset of the database to a PDF.
"${PYTHON}" "${DIR}/manage.py" graph_models -gE -X AbstractUser,Group,Permission \
    auth mentoring training cuedmembers matching \
    | dot -Tpdf >db-diagram.pdf
