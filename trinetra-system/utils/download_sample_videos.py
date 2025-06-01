import os
import requests
from tqdm import tqdm

def download_file(url, filename):
    """
    Download a file with progress bar
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def main():
    # Create test_videos directory if it doesn't exist
    videos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_videos')
    os.makedirs(videos_dir, exist_ok=True)
    
    # Sample video URLs (from Pexels or other free video sites)
    videos = {
        'entrance.mp4': 'https://www.pexels.com/download/video/4113666/',  # People entering/exiting
        'store.mp4': 'https://www.pexels.com/download/video/3873240/',     # Inside store footage
        'billing.mp4': 'https://www.pexels.com/download/video/4100357/',   # Checkout counter
        'parking.mp4': 'https://www.pexels.com/download/video/5307036/'    # Parking lot
    }
    
    print("Downloading sample videos for testing...")
    for filename, url in videos.items():
        filepath = os.path.join(videos_dir, filename)
        if not os.path.exists(filepath):
            try:
                print(f"\nDownloading {filename}...")
                download_file(url, filepath)
                print(f"Successfully downloaded {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
        else:
            print(f"\n{filename} already exists, skipping...")

if __name__ == "__main__":
    main()
