#!/usr/bin/env sh

python csv_to_mongo.py
exec uwsgi -s "$SOCKET_PATH" -C --manage-script-name --mount "/api=chemy:create_app()"
