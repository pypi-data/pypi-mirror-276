#!/bin/bash

# Function to install all dependencies from package.json and package-lock.json
install_all_dependencies() {
  local dir=$1
  docker compose run --rm -v "$(pwd)/${dir}:/app" storybook npm install
}

# Function to install specific dependencies
install_dependencies() {
  local dir=$1
  shift
  if [ -z "$1" ]; then
    echo "Please provide at least one package to install."
    exit 1
  fi
  docker-compose run --rm -v "$(pwd)/${dir}:/app" storybook npm install "$@"
}

# Function to uninstall specific dependencies
uninstall_dependencies() {
  local dir=$1
  shift
  if [ -z "$1" ]; then
    echo "Please provide at least one package to uninstall."
    exit 1
  fi
  docker compose run --rm -v "$(pwd)/${dir}:/app" storybook npm uninstall "$@"
}

# Function to start the development environment
start() {
  docker compose up --build
}

# Function to stop the development environment
stop() {
  docker compose down
}

# Function to initialize Storybook
initialize_storybook() {
  local dir=$1
  docker compose run --rm -v "$(pwd)/${dir}:/app" storybook npx storybook init
}

# Function to generate stories using the Python script
generate_stories() {
  local dir=$1
  python setup_storybook.py "$dir/src/components"
}

# Function to show usage
usage() {
  echo "Usage: $0 {install-all|install|uninstall|start|stop|init-storybook|generate-stories} [directory] [package...]"
  exit 1
}

# Parse command line arguments
command=$1
directory=$2
shift 2

case "$command" in
  install-all)
    install_all_dependencies "$directory"
    ;;
  install)
    install_dependencies "$directory" "$@"
    ;;
  uninstall)
    uninstall_dependencies "$directory" "$@"
    ;;
  start)
    start
    ;;
  stop)
    stop
    ;;
  init-storybook)
    initialize_storybook "$directory"
    ;;
  generate-stories)
    generate_stories "$directory"
    ;;
  *)
    usage
    ;;
esac
