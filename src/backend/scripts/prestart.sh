#!/usr/bin/env sh

# Check if storage is ready
app storage check

# Create initial data in DB
app storage setup
