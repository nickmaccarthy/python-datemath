# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the contents of your project to the working directory
COPY . .

# Install the required dependencies
RUN pip install -r requirements.txt

# Run setup.py to install your module
RUN python3 setup.py install

# Run your tests to ensure everything works as expected
RUN python3 -m unittest discover

# Set the entrypoint command to run your module
CMD ["python3", "verify.py"]