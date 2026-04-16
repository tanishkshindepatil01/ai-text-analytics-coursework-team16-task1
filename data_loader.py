import requests

def load_data_from_github_url(url: str) -> str:
    """
    Load data from a GitHub URL.
    
    Args:
        url: The URL of the data to load.
    
    Returns:
        The data from the URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to load data from {url}")
