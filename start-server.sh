#!/bin/bash

echo "================================================================"
echo "                    AI School Backend Server"
echo "================================================================"
echo

cd "$(dirname "$0")/backend"

if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and update with your Azure credentials."
    echo
    exit 1
fi

echo "Starting server..."
echo
python app.py
