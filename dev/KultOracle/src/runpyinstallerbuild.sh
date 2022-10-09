#!/bin/sh

# --exclude-module resources \

pyinstaller \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-shell-integration/*:PyQt5/Qt5/plugins/wayland-shell-integration \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-graphics-integration-client/*:PyQt5/Qt5/plugins/wayland-graphics-integration-client \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-decoration-client/*:PyQt5/Qt5/plugins/wayland-decoration-client \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/fitz/*:fitz \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/tqdm/*:tqdm \
--add-data /home/columbus/dev/KultOracle/src/sqlscripts/DDL.sql:sqlscripts \
--hidden-import json \
--hidden-import tqdm \
--hidden-import tqdm_auto \
--additional-hooks-dir=./__pyinstaller \
--noconfirm \
--onefile \
--windowed \
kultoraclemain.py -n kultoracle 

