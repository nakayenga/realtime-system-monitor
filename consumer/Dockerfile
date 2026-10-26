
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install prerequisites for Microsoft ODBC Driver 18.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
        unixodbc \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Register Microsoft's Debian 12 package repository.
RUN curl -fsSL \
        https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
        -o /tmp/packages-microsoft-prod.deb \
    && dpkg -i /tmp/packages-microsoft-prod.deb \
    && rm /tmp/packages-microsoft-prod.deb

# Install Microsoft ODBC Driver 18 for SQL Server.
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Verify the ODBC driver is registered.
RUN odbcinst -q -d

# Install Python dependencies.
COPY consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the existing consumer application.
COPY consumer/ ./consumer/

# Run as a non-root user.
RUN useradd --create-home appuser

USER appuser

EXPOSE 8000
EXPOSE 8080

CMD ["python", "-m", "consumer.app"]
