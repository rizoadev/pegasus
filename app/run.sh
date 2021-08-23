#!/bin/bash
cd /home

if [ "$1" == "app" ]; then
    python -m uvicorn main:app --reload --port 6071 --host 0.0.0.0 --workers 1
else
    python -u worker.py
fi
