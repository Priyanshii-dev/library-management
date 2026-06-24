"""
Gunicorn configuration for production deployment.
"""

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "library-management-system"

# Server mechanics
daemon = False
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (for HTTPS)
keyfile = None
certfile = None

# Application
raw_env = []
