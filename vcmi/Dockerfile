FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 python3-venv python3-pip \
  xvfb x11-xkb-utils x11-apps xdotool wmctrl \
  openbox twm \
  imagemagick xauth \
  x11vnc tigervnc-standalone-server \
  mesa-utils mesa-utils-extra libgl1-mesa-dri libglu1-mesa \
  libxkbcommon-x11-0 \
  libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-render-util0 libxcb-xinerama0 libxcb-xinput0 libxcb-shm0 \
  libxrandr2 libxrender1 libxi6 \
  innoextract

RUN apt-get update \
  && apt-get install -y software-properties-common

RUN apt-add-repository ppa:vcmi/ppa \
  && apt update \
  && apt install -y vcmi

RUN rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash app
USER app
WORKDIR /home/app

COPY --chown=app:app entrypoint.sh /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh

EXPOSE 5900

ENV PATH="/usr/games:${PATH}"

RUN vcmibuilder --help

ENTRYPOINT ["/home/app/entrypoint.sh"]
