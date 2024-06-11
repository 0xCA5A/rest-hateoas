FROM python:3.12-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
COPY requirements.txt .
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install -r requirements.txt

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY app.py .

# Expose the server port
EXPOSE 5000

# Run the application
CMD ["/opt/venv/bin/python3", "app.py"]
