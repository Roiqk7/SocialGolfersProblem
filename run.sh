#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -ueo pipefail

# --- Configuration ---
# Set the path to your C# project
CSHARP_PROJECT_PATH="src/SocialGolfersProblem/webapi"

# Set the path to your frontend files
FRONTEND_DIR="src/wwwroot"

# Set ports
BACKEND_PORT="5001"
FRONTEND_PORT="8080"

# --- Prerequisites Check ---
echo "Checking for 'dotnet' and 'python3'..."
command -v dotnet >/dev/null 2>&1 || { echo >&2 "I require 'dotnet' but it's not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "I require 'python3' but it's not installed. Aborting."; exit 1; }
echo "✅ Prerequisites found."
echo "-----------------------------------"

# --- Start the Backend API ---
echo "▶️ Starting the ASP.NET Core Web API..."
# We explicitly set the URL for the backend
ASPNETCORE_URLS="http://localhost:${BACKEND_PORT}" dotnet run --project "${CSHARP_PROJECT_PATH}" &

echo "✅ Backend API is running on http://localhost:${BACKEND_PORT}"
echo "-----------------------------------"

# --- Start the Frontend Static Server ---
echo "🌐 Serving the static frontend files..."
cd "${FRONTEND_DIR}" || { echo "Error: ${FRONTEND_DIR} directory not found."; exit 1; }

# This serves the static files
python3 -m http.server ${FRONTEND_PORT} &

echo "✅ Frontend is available at http://localhost:${FRONTEND_PORT}"
echo "-----------------------------------"

echo "✨ Both the backend and frontend are now running."
echo "   Access the site at: http://localhost:${FRONTEND_PORT}"
echo "   Press [Ctrl+C] to stop both servers."

# Wait for any background process to exit, and then exit
wait
