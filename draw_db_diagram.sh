#!/usr/bin/env bash
#
# A simple little script to draw a diagram of a subset of the database to a PDF.
./manage.py graph_models -gE -X AbstractUser,Group,Permission \
    auth mentoring training cuedmembers matching \
    | dot -Tpdf >db-diagram.pdf
