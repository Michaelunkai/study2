# Use the official Node.js image
FROM node:16

# Set the working directory
WORKDIR /usr/src/app

# Install TypeScript globally
RUN npm install -g typescript

# Install any other global tools you might need, for example, ts-node
RUN npm install -g ts-node

# Open the development server port
EXPOSE 3000

# Start a shell by default
CMD ["sh"]
