FROM python:3.11.4-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Ensure Flask runs on 0.0.0.0 to be accessible from outside the container
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run the Flask application
CMD python main.py
