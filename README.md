# Ballistic

Ballistic is a tool for maintaining a data service using Yahoo Finance for loading stock data for easy storage and real-time access. It uses Redis and MongoDB for real-time cache and backup storage. An user can subscribe to a stock symbol at intraday (per-minute) time scale. The data are all stored in UTC Time. Ballistic provides a Python API for developers to subscribe to real-time stock data while buliding up a historical stock dataset.

## Run Ballistic

chmod +x fire.sh

./fire.sh [symbols-path]
