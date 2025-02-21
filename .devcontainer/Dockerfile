FROM python:3.11-slim

# Copy files
RUN mkdir settings

COPY install_dependencies.sh requirements.txt settings/
RUN bash ./settings/install_dependencies.sh
RUN apt-get update && apt-get install -y git

# Install AWS CLI
RUN curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip -qq awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip ./aws

# Install Docker (optional, only needed if Docker isn't already installed)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    gnupg \
    lsb-release \
    && curl -fsSL https://get.docker.com | sh

RUN pip install  --no-cache-dir -r ./settings/requirements.txt
