### Step 1: Create a Dockerfile

Create a file named `Dockerfile` (without any file extension) in the same directory as your Flask script. Open the `Dockerfile` and add the following content:

Dockerfile
# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run your Flask script when the container launches
CMD ["python", "Base.py"]

Replace `"Base.py"` with the actual filename of your Flask script.

### Step 2: Create a Requirements File (if not exists)

If you don't already have a `requirements.txt` file that lists your Python dependencies, create one in the same directory as your `Dockerfile`. List the dependencies, each on a new line.

### Step 3: Build the Docker Image

Open a terminal or command prompt in the same directory as your `Dockerfile` and run the following command to build your Docker image:

bash docker build -t your-image-name .

Replace `"your-image-name"` with the desired name for your Docker image.

### Step 4: Run the Docker Container

Once the image is built, you can run your Docker container using the following command:

bash docker run -p 5000:5000 your-image-name

This maps port 5000 on your local machine to port 5000 in the Docker container. Adjust the port mapping as needed.

### Step 5: Access Your Web Server

Visit `http://localhost:5000` in your web browser to access your Flask web server running inside the Docker container.
