# Use a base image with necessary dependencies
FROM debian:latest

# Install necessary packages (gcc to compile, ncat for networking)
RUN apt-get update && apt-get install -y gcc ncat

# Set working directory
WORKDIR /app

# Copy the challenge source and flag file to the container
COPY challenge.c /app/challenge.c
COPY flag.txt /app/flag.txt

# Compile the challenge
RUN gcc -o /app/challenge /app/challenge.c

# Expose port 4445 (to be used for nc)
EXPOSE 4445

# Use ncat to listen on port 4445 and execute the challenge
CMD ["ncat", "-lk", "-p", "4445", "-e", "./challenge"]
