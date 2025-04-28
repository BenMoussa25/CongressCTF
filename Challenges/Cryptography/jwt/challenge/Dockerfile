FROM python:3.9-slim-buster
# Set the working directory inside the container
WORKDIR /app

# Copy necessary files
COPY . .

# Install dependencies
RUN pip install Flask
RUN pip install pyjwt==1.4.2
RUN pip install cryptography==2.7

# Expose the Flask app's port
EXPOSE 6002

# Command to run the application
CMD ["python", "app.py"]
