FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt ./

# Install dependencies including Gunicorn
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 4000

# Use Gunicorn to serve the Flask app
# Adjust the number of workers as needed (e.g., 3)
# Replace 'app:app' with 'your_flask_file_name:flask_app_variable_name' if different
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:4000", "app:app"]
