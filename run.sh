#!/bin/bash

# Shopless Docker Runner Script

set -e

case "$1" in
    "start")
        echo "Starting Shopless application..."
        docker-compose up -d
        echo "Application started at http://localhost:8000"
        ;;
    "stop")
        echo "Stopping Shopless application..."
        docker-compose down
        ;;
    "restart")
        echo "Restarting Shopless application..."
        docker-compose restart
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "build")
        echo "Building Shopless application..."
        docker-compose build
        ;;
    "clean")
        echo "Cleaning up containers and volumes..."
        docker-compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: ./run {start|stop|restart|logs|build|clean}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the application"
        echo "  stop    - Stop the application"
        echo "  restart - Restart the application"
        echo "  logs    - View application logs"
        echo "  build   - Build the application"
        echo "  clean   - Clean up containers and volumes"
        exit 1
        ;;
esac
