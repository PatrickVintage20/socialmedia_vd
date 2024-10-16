# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container to match your project name
WORKDIR /video_downloader

# Install system dependencies required by Playwright, yt-dlp, Selenium, and other tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    ffmpeg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libharfbuzz0b \
    libxcb1 \
    libx11-xcb1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and set it up for scraping
RUN pip install playwright==1.47.0 && playwright install-deps && playwright install

# Install Selenium dependencies
RUN pip install selenium==4.25.0 && pip install webdriver-manager

# Install yt-dlp for video downloading
RUN pip install yt-dlp==2024.9.27

# Copy the requirements.txt to the container and install Python dependencies
COPY requirements.txt /video_downloader/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /video_downloader/

# Collect static files (if using static files in Django)
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on (default is 8000 for Django)
EXPOSE 8000

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
