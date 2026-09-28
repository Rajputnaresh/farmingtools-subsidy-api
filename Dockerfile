FROM python:3.11-slim

WORKDIR /app

# The service uses standard library only (no pip dependencies required)
COPY requirements.txt ./

# Copy application files
COPY subsidy_api.py subsidy_calculator.py state_portal_utils.py ./
COPY subsidy_widget.html subsidy_widget_docs_steps.js ./
COPY data/ ./data/
COPY subsidy_data/ ./subsidy_data/

# Expose HTTP port
EXPOSE 8080

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run built-in HTTP server
CMD ["python3", "subsidy_api.py"]
