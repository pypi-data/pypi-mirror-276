# Use an official node runtime as a parent image
FROM node:lts-bookworm-slim

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
# COPY package*.json ./

# Install dependencies
RUN npx storybook@latest init

# Copy the rest of the application to the working directory
COPY . .

# Expose the port Storybook will run on
EXPOSE 6006

# Start Storybook
CMD ["npm", "run", "storybook"]
