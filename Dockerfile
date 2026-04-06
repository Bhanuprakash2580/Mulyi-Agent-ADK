FROM python:3.12-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

EXPOSE 8080

WORKDIR /app/adk_multiagent_systems/workflow_agents
# Start the ADK web server, binding to 0.0.0.0 so Cloud Run can route traffic to it
CMD ["adk", "run", "agent.py", "--port", "8080", "--host", "0.0.0.0"]