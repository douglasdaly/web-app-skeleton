# -*- coding: utf-8 -*-
"""
Gunicorn configuration
"""
import json
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

protocol = os.getenv("SERVER_PROTOCOL", "http")
host = os.getenv("SERVER_HOST", "0.0.0.0")
port = os.getenv("SERVER_PORT", "3000")
bind = os.getenv("BIND", f"{host}:{port}")

loglevel = os.getenv("LOG_LEVEL", "info")

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
workers = web_concurrency
keepalive = 120

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}
print(json.dumps(log_data))
