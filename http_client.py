import requests

def http_client():
    url = "https://httpbin.org"  # Test API
    
    try:
        # GET request
        response_get = requests.get(f"{url}/get", params={"sample": "data"})
        print("=== GET Request ===")
        print("Status Code:", response_get.status_code)
        print("Headers:", response_get.headers)
        print("Body:", response_get.text[:200], "...\n")  # truncated for readability

        # POST request
        response_post = requests.post(f"{url}/post", data={"username": "test", "password": "123"})
        print("=== POST Request ===")
        print("Status Code:", response_post.status_code)
        print("Headers:", response_post.headers)
        print("Body:", response_post.text[:200], "...\n")

    except requests.exceptions.RequestException as e:
        print("HTTP Error:", e)

if __name__ == "__main__":
    http_client()
