


pyinstaller \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-shell-integration/*:PyQt5/Qt5/plugins/wayland-shell-integration \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-graphics-integration-client/*:PyQt5/Qt5/plugins/wayland-graphics-integration-client \
--add-binary $VIRTUAL_ENV/lib/python3.8/site-packages/PyQt5/Qt5/plugins/wayland-decoration-client/*:PyQt5/Qt5/plugins/wayland-decoration-client \
--additional-hooks-dir=./__pyinstaller \
--exclude-module resources \
--noconfirm \
--onedir \
--windowed \
kultoraclemain.py -n kultoracle 

