# Use a base image with necessary dependencies
FROM debian:latest

# Install necessary packages (netcat)
RUN apt-get update && apt-get install -y netcat

# Set working directory
WORKDIR /app

# Copy the challenge executable and flag file to the container
COPY challenge /app/challenge
COPY flag.txt /app/flag.txt

# Give executable permission to the challenge
RUN chmod +x /app/challenge

# Expose port 4445 (to be used for nc)
EXPOSE 4445

# Use netcat to listen on port 4445 and execute the challenge
CMD ["nc", "-lk", "-p", "4445", "-e", "./challenge"]
