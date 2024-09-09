FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
# Make port 8080 available to the world outside this container
EXPOSE 8080

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Define environment variable
ENV PORT 8080

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
