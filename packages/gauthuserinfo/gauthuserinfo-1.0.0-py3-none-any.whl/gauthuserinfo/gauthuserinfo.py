import requests
import sys

def get_user_info(access_token):
    url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        return {
            "error": False,
            "status_code": response.status_code,
            "data": response.json()
        }

    except requests.exceptions.HTTPError as e:
        return {
            "error": True,
            "status_code": response.status_code,
            "message": f"HTTP error occurred: {str(e)}"
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "error": True,
            "message": f"Connection error occurred: {str(e)}"
        }
    except requests.exceptions.Timeout as e:
        return {
            "error": True,
            "message": f"Timeout error occurred: {str(e)}"
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "message": f"An error occurred: {str(e)}"
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: gauthuserinfo <access_token>")
        sys.exit(1)

    access_token = sys.argv[1]
    result = get_user_info(access_token)
    print(result)