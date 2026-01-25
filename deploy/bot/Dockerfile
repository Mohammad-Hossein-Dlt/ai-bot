FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get -y install -y weasyprint

RUN apt-get update && apt-get install -y fonts-dejavu fontconfig && rm -rf /var/lib/apt/lists/
COPY fonts/shabnam-light.ttf /usr/share/fonts/truetype/myfont/
COPY fonts/shabnam.ttf /usr/share/fonts/truetype/myfont/
COPY fonts/shabnam-bold.ttf /usr/share/fonts/truetype/myfont/
RUN fc-cache -f -v
RUN echo "FONT=shabnam" >> /etc/environment

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

RUN uv sync --upgrade --no-cache

CMD ["uv", "run", "bot.py"]