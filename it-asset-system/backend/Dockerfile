FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application files
COPY . .

# Create directories for uploads and QR codes
RUN mkdir -p uploads public/qrcodes

# Expose port
EXPOSE 5000

# Start application
CMD ["npm", "run", "dev"]
