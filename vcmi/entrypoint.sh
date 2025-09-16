#!/usr/bin/env bash

set -euo pipefail
set -x

DISPLAY_NUM="${DISPLAY_NUM:-33}"
SCREEN_W="${SCREEN_W:-1920}"
SCREEN_H="${SCREEN_H:-1080}"
SCREEN_D="${SCREEN_D:-24}"
RFBPORT="${RFBPORT:-5900}"
APP_CMD="${APP_CMD:-vcmieditor}"
HOMM_DATA="${HOMM_DATA_PATH}"
RUN_VNC="${RUN_VNC:-1}"
XAUTH_DIR="${XAUTH_DIR:-1}"

export LIBGL_ALWAYS_SOFTWARE=1
export MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
export __GLX_VENDOR_LIBRARY_NAME=mesa
export GDK_BACKEND=x11
export QT_QPA_PLATFORM=xcb
export SDL_VIDEODRIVER=x11
export QSG_RHI_BACKEND=software
export QT_QUICK_BACKEND=software
export QT_XCB_FORCE_SOFTWARE_OPENGL=1

ls -la "$HOMM_DATA"

# Find executable in HOMM_DATA directory
EXE_FILE=$(find "$HOMM_DATA" -name "*.exe" -type f | head -n 1)

if [ -n "$EXE_FILE" ]; then
  echo "Found executable: $EXE_FILE"
  vcmibuilder --gog "$EXE_FILE"
else
  echo "No executable found"
  exit 1
fi

export DISPLAY=":${DISPLAY_NUM}"
Xvfb "${DISPLAY}" -screen 0 "${SCREEN_W}x${SCREEN_H}x${SCREEN_D}" -pn -listen tcp -ac +extension GLX +extension RANDR &

for i in {1..100}; do
  echo "Waiting for X socket"
  [ -S "/tmp/.X11-unix/X${DISPLAY_NUM}" ] && break
  sleep 0.05
done

xauth generate "$DISPLAY" . trusted
cp ~/.Xauthority "$XAUTH_DIR/"
chmod 644 "$XAUTH_DIR/.Xauthority"

openbox >/dev/null 2>&1 &

xset s off -dpms >/dev/null 2>&1 || true
xset s noblank >/dev/null 2>&1 || true

if [ "$RUN_VNC" = "1" ]; then
  x11vnc -display "${DISPLAY}" -rfbport "${RFBPORT}" -listen 0.0.0.0 -forever -shared -nopw -noxdamage -noshm >/tmp/vnc.log 2>&1 &
fi

exec $APP_CMD "$@"
