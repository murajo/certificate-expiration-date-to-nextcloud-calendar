# SSL Certificate Add script with NextcloudCalenderManage

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-yellow?logo=python&logoColor=white)
![NextCloud](https://img.shields.io/badge/NextCloud-blue?logo=nextcloud&logoColor=white)


## Overview

This project is a script that uses the following "Nextcloud Calender Manage API"

https://github.com/murajo/nextcloud-calender-manage-api

It contains a Python script that checks for an SSL certificate for the specified domain and automatically adds the event to the NextCloud calendar if not present.

## Prerequisite.
Need "Nextcloud Calender Manage API" running and able to connect.

https://github.com/murajo/nextcloud-calender-manage-api

## Quick Start

### Option1: Running with Python

1. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

2. Create a `config.yaml` file in the root directory with the following structure:
    ```yaml
    domains:
      - example.com
      - anotherdomain.com
    nextcloud:
      api_url: "http://<your-nextcloud-calendar-manage-api-url>:<port>"
      calendar_name: "<your-calendar-name>"
    ```

3. Running the Script
    ```bash
    python main.py
    ```

### Option2: Running with Docker

1. Build the Docker image:

    ```bash
    docker build -t ssl-certificate-add-to-calendar .
    ```

2. Create a `config.yaml` file in an arbitrary directory with the following structure:
    ```yaml
    domains:
      - example.com
      - anotherdomain.com
    nextcloud:
      api_url: "http://<your-nextcloud-calendar-manage-api-url>:<port>"
      calendar_name: "<your-calendar-name>"
    ```

3. Run the Docker container:

    ```bash
    docker run -v /path/to/your/config.yaml:/app/config.yaml ssl-certificate-add-to-calendar
    ```

## Functions

### 1. Get SSL Information
- **Function**: `get_ssl_info(host, port=443)`
- **Description**: Retrieves SSL certificate information for the specified host.
- **Parameters**:
  - `host`: Domain to check.
  - `port`: Port (default is 443).
- **Returns**: A dictionary with the common name and validity dates of the SSL certificate, or `None` if an error occurs.

### 2. Check if Event Exists
- **Function**: `check_event_exists(calendar_name, summary)`
- **Description**: Checks if a specific event exists in the NextCloud calendar.
- **Parameters**:
  - `calendar_name`: Name of the calendar.
  - `summary`: Event summary.
- **Returns**: `True` if the event exists; otherwise, `False`.

### 3. Create Event
- **Function**: `create_event(calendar_name, start_time, end_time, summary, description, timezone="Asia/Tokyo")`
- **Description**: Adds a new event to the specified calendar.
- **Parameters**:
  - `calendar_name`: Name of the calendar.
  - `start_time`: Event start time.
  - `end_time`: Event end time.
  - `summary`: Event summary.
  - `description`: Event description.
  - `timezone`: Timezone for the event (default is "Asia/Tokyo").
- **Returns**: Outputs the response status after adding the event.
