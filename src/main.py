import os
import requests
import ssl
import OpenSSL
import yaml

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../config.yaml")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()

NextCloud_API_URL = config['nextcloud']['api_url']
NextCloud_CALENDAR_NAME = config['nextcloud']['calendar_name']

def get_ssl_info(host, port=443):
    try:
        cert = ssl.get_server_certificate((host, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        common_name = x509.get_subject().CN
        not_before = x509.get_notBefore().decode('utf-8')
        not_after = x509.get_notAfter().decode('utf-8')

        valid_from = f"{not_before[:4]}-{not_before[4:6]}-{not_before[6:8]}"
        valid_until = f"{not_after[:4]}-{not_after[4:6]}-{not_after[6:8]}"

        return {"common_name": common_name, "valid_from": valid_from, "valid_until": valid_until}
    except Exception as e:
        print(f"Error getting SSL info from {host}: {e}")
        return None

def check_event_exists(calendar_name, summary):
    try:
        response = requests.get(f"{NextCloud_API_URL}/event_exists", params={"calendar_name": calendar_name, "summary": summary})
        if response.status_code == 200:
            return response.json().get("exists", False)
        else:
            print(f"Error checking event: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    return False

def create_event(calendar_name, start_time, end_time, summary, description, timezone="Asia/Tokyo"):
    try:
        event_data = {
            "calendar_name": calendar_name,
            "start_time": start_time,
            "end_time": end_time,
            "summary": summary,
            "description": description,
            "timezone": timezone
        }
        response = requests.post(f"{NextCloud_API_URL}/add_event", json=event_data)
        if response.status_code == 200:
            print(f"Event added: {response.json()}")
        else:
            print(f"Error adding event: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    for host in config['domains']:
        ssl_info = get_ssl_info(host)
        if not ssl_info:
            continue
        common_name = ssl_info["common_name"]
        valid_from = ssl_info["valid_from"]
        valid_until = ssl_info["valid_until"]
        
        summary = f"{common_name} {valid_from}"
        
        if not check_event_exists(NextCloud_CALENDAR_NAME, summary):
            event_time = f"{valid_until}T00:00:00"
            description = f"SSL Certificate valid from {valid_from} to {valid_until}"
            create_event(NextCloud_CALENDAR_NAME, event_time, event_time, summary, description)
        else:
            print(f"Event '{summary}' already exists.")

if __name__ == "__main__":
    main()
