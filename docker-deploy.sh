#!/bin/bash

# Tenderly AI Agent - Docker Deployment Script
# This script helps deploy and manage the Tenderly AI Agent using Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
PROD_COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env"
PROJECT_NAME="tenderly-ai-agent"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Tenderly AI Agent Deployment  ${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
}

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    print_status "Checking requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_status "All requirements met!"
}

setup_environment() {
    print_status "Setting up environment..."
    
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f ".env.docker" ]; then
            print_status "Copying .env.docker to .env"
            cp .env.docker .env
        elif [ -f ".env.example" ]; then
            print_status "Copying .env.example to .env"
            cp .env.example .env
        else
            print_error "No environment file found. Please create .env file."
            exit 1
        fi
        
        print_warning "Please update the .env file with your actual configuration values!"
        echo "Press Enter to continue or Ctrl+C to exit and configure first..."
        read
    fi
}

generate_secrets() {
    print_status "Generating secure secrets..."
    
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET_KEY=$(openssl rand -hex 32)
    API_KEY=$(openssl rand -hex 32)
    
    echo
    echo "Generated secrets (save these securely):"
    echo "SECRET_KEY=$SECRET_KEY"
    echo "JWT_SECRET_KEY=$JWT_SECRET_KEY"
    echo "API_KEY=$API_KEY"
    echo
    echo "Update your .env file with these values!"
}

build_images() {
    print_status "Building Docker images..."
    
    if [ "$1" == "prod" ]; then
        docker-compose -f $PROD_COMPOSE_FILE build --no-cache
    else
        docker-compose -f $COMPOSE_FILE build --no-cache
    fi
    
    print_status "Images built successfully!"
}

start_services() {
    print_status "Starting services..."
    
    if [ "$1" == "prod" ]; then
        docker-compose -f $PROD_COMPOSE_FILE up -d
    else
        docker-compose -f $COMPOSE_FILE up -d
    fi
    
    print_status "Services started!"
}

stop_services() {
    print_status "Stopping services..."
    
    if [ "$1" == "prod" ]; then
        docker-compose -f $PROD_COMPOSE_FILE down
    else
        docker-compose -f $COMPOSE_FILE down
    fi
    
    print_status "Services stopped!"
}

show_status() {
    print_status "Service status:"
    echo
    
    if [ "$1" == "prod" ]; then
        docker-compose -f $PROD_COMPOSE_FILE ps
    else
        docker-compose -f $COMPOSE_FILE ps
    fi
}

show_logs() {
    if [ "$2" ]; then
        SERVICE="$2"
    else
        SERVICE="tenderly-ai-agent"
    fi
    
    print_status "Showing logs for $SERVICE..."
    
    if [ "$1" == "prod" ]; then
        docker-compose -f $PROD_COMPOSE_FILE logs -f $SERVICE
    else
        docker-compose -f $COMPOSE_FILE logs -f $SERVICE
    fi
}

health_check() {
    print_status "Performing health check..."
    
    # Wait a moment for services to start
    sleep 5
    
    # Check main service health
    if curl -f http://localhost:8000/api/v1/health/live > /dev/null 2>&1; then
        print_status "✓ Tenderly AI Agent is healthy"
    else
        print_error "✗ Tenderly AI Agent health check failed"
    fi
    
    # Check Redis - find the correct container name dynamically
    REDIS_CONTAINER=$(docker ps --filter "name=redis" --format "{{.Names}}" | head -n1)
    if [ -n "$REDIS_CONTAINER" ]; then
        if docker exec $REDIS_CONTAINER redis-cli ping > /dev/null 2>&1; then
            print_status "✓ Redis is healthy"
        else
            print_warning "Redis container found but health check failed"
        fi
    else
        print_warning "Redis container not found or not accessible"
    fi
    
    # Additional checks - Redis connectivity from host
    if command -v redis-cli &> /dev/null; then
        if redis-cli -h localhost -p 6379 ping > /dev/null 2>&1; then
            print_status "✓ Redis accessible from host"
        else
            print_warning "Redis not accessible from host (this is normal if Redis auth is enabled)"
        fi
    fi
}

cleanup() {
    print_status "Cleaning up Docker resources..."
    
    # Stop and remove containers
    if [ "$1" == "prod" ]; then
        docker-compose -f $PROD_COMPOSE_FILE down --volumes
    else
        docker-compose -f $COMPOSE_FILE down --volumes
    fi
    
    # Remove unused images
    docker image prune -f
    
    print_status "Cleanup completed!"
}

show_help() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  setup          Set up environment and generate secrets"
    echo "  build [prod]   Build Docker images"
    echo "  start [prod]   Start services"
    echo "  stop [prod]    Stop services"
    echo "  restart [prod] Restart services"
    echo "  status [prod]  Show service status"
    echo "  logs [prod] [service]  Show service logs"
    echo "  health         Perform health check"
    echo "  cleanup [prod] Clean up Docker resources"
    echo "  secrets        Generate new secrets"
    echo "  help           Show this help message"
    echo
    echo "Options:"
    echo "  prod           Use production configuration"
    echo
    echo "Examples:"
    echo "  $0 setup                    # Initial setup"
    echo "  $0 build                    # Build for development"
    echo "  $0 build prod              # Build for production"
    echo "  $0 start                    # Start development services"
    echo "  $0 start prod              # Start production services"
    echo "  $0 logs                     # Show AI agent logs"
    echo "  $0 logs prod redis         # Show Redis logs in production"
}

# Main script
print_header

case "$1" in
    setup)
        check_requirements
        setup_environment
        generate_secrets
        ;;
    build)
        check_requirements
        build_images $2
        ;;
    start)
        check_requirements
        start_services $2
        ;;
    stop)
        stop_services $2
        ;;
    restart)
        stop_services $2
        start_services $2
        ;;
    status)
        show_status $2
        ;;
    logs)
        show_logs $2 $3
        ;;
    health)
        health_check
        ;;
    cleanup)
        cleanup $2
        ;;
    secrets)
        generate_secrets
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use '$0 help' for usage information."
        exit 1
        ;;
esac

echo
print_status "Operation completed!"
