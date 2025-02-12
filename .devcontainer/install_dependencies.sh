#!/usr/bin/env bash

# Install dependecies
 apt-get update && apt-get install -y --no-install-recommends \
   software-properties-common \
    zip \
    less \
    groff \
    gnupg \
    python3-launchpadlib \
    vim \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*