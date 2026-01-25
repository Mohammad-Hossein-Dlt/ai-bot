FROM python:3.12.12-slim

WORKDIR /app

COPY . .

RUN apt-get -y update
RUN apt-get -y upgrade

# -----------------------------
# Install Weasyprint
# -----------------------------
RUN apt-get -y install -y weasyprint
RUN apt-get update && apt-get install -y fonts-dejavu fontconfig && rm -rf /var/lib/apt/lists/

# -----------------------------
# Fonts (Persian / Shabnam)
# -----------------------------
# COPY fonts/shabnam-light.ttf /usr/share/fonts/truetype/myfont/
# COPY fonts/shabnam.ttf /usr/share/fonts/truetype/myfont/
# COPY fonts/shabnam-bold.ttf /usr/share/fonts/truetype/myfont/
# RUN fc-cache -f -v
# RUN echo "FONT=shabnam" >> /etc/environment

# -----------------------------
# Install Curl
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# -----------------------------
# Install uv
# -----------------------------
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# -----------------------------
# Install Python deps
# -----------------------------
RUN uv sync --upgrade --no-cache

# -----------------------------
# Run service
# -----------------------------
EXPOSE 80
CMD ["uv", "run", "fastapi", "run", "./src/main.py", "--proxy-headers", "--port", "80"]