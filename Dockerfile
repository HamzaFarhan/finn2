# Use Python base image
FROM python:3.12

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Verify installations
RUN node --version && npm --version && npx --version

# Set the working directory
WORKDIR /app

# Copy toml and Readme file
COPY pyproject.toml /app
COPY README.md /app

# Install pip and hatch globally
RUN pip install --no-cache-dir hatch

# Copy project files
COPY . /app/

# Install uv globally
RUN pip install uv

# Expose ports as needed
EXPOSE 5588

WORKDIR /app/src/finn2

# Command to run your application
CMD ["sh", "-c", "uv run test_ui.py --host 0.0.0.0 --port 5588"]


#docker build . -f Dockerfile -t gcr.io/dreamai-pocs/finn2-bkend-app:v1

