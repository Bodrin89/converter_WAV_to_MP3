#!/bin/bash


# Путь к папке с wav файлами
AUDIO_WAV_DIR="./audio_file/file_wav"
# Путь к папке с mp3 файлами
AUDIO_MP3_DIR="./audio_file/file_mp3"
# Путь к папке с загрузками
DOWNLOAD_DIR="./download"


# Создание папки с wav файлами (если не существует)
if [ ! -d "$AUDIO_WAV_DIR" ]; then
    mkdir -p "$AUDIO_WAV_DIR"

fi
# Создание папки с mp3 файлами (если не существует)
if [ ! -d "$AUDIO_MP3_DIR" ]; then
    mkdir -p "$AUDIO_MP3_DIR"

fi

# Создание папки с загрузками (если не существует)
if [ ! -d "$DOWNLOAD_DIR" ]; then
    mkdir -p "$DOWNLOAD_DIR"

fi

exec "$@"