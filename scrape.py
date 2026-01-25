import requests
from bs4 import BeautifulSoup
import json
import re
import os  # <--- NEW: Needed to check if the file exists

def scrape_noaa():
    url = "https://www.nohrsc.noaa.gov/interactive/html/map.html?var=snowfall_72_h&min_x=-80.366666666669&min_y=37.183333333329&max_x=-72.866666666669&max_y=41.399999999996&bgvar=dem&shdvar=shading&title=1&width=800&height=450&font=0&lbl=m&palette=0&h_o=0&metric=0&lp=1&no_header=0&snap=1&extents=us&o9=1&o11=1&o13=1"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the TD that contains the text "National Gridded Snowfall Analysis"
    target_td = soup.find('td', string=re.compile("National Gridded Snowfall Analysis"))
    
    if target_td:
        full_text = target_td.get_text().strip()
        match = re.search(r"preceding\s+(.*)$", full_text)
        
        if match:
            new_timestamp = match.group(1)
            
            # --- START OF NEW LOGIC ---
            # 1. Load the existing timestamp if the file exists
            existing_timestamp = None
            if os.path.exists('timestamp.json'):
                with open('timestamp.json', 'r') as f:
                    try:
                        data = json.load(f)
                        existing_timestamp = data.get("timestamp")
                    except json.JSONDecodeError:
                        pass # File is empty or corrupt, ignore it

            # 2. Only write if the timestamp has actually changed
            if new_timestamp == existing_timestamp:
                print(f"No change detected. Current timestamp is still: {new_timestamp}")
                return # Exit without writing or committing
            
            # 3. Save the new timestamp
            with open('timestamp.json', 'w') as f:
                json.dump({"timestamp": new_timestamp}, f)
            
            print(f"NEW timestamp found and saved: {new_timestamp}")
            return
            # --- END OF NEW LOGIC ---
            
    print("Could not find timestamp on page.")

if __name__ == "__main__":
    scrape_noaa()
