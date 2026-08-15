#!/bin/bash
mkdir static/avatar
mkdir static/uploads
uuidgen > secret.key
pip install -r req.txt