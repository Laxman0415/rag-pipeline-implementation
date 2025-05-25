# Use official Python slim image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /frontend-app

# Copy the rest of the app source code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app, listening on all interfaces
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
