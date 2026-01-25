import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_noaa():
    url = "https://www.nohrsc.noaa.gov/interactive/html/map.html?var=snowfall_72_h&min_x=-80.366666666669&min_y=37.183333333329&max_x=-72.866666666669&max_y=41.399999999996&bgvar=dem&shdvar=shading&title=1&width=800&height=450&font=0&lbl=m&palette=0&h_o=0&metric=0&lp=1&no_header=0&snap=1&extents=us&o9=1&o11=1&o13=1"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the TD that contains the text "National Gridded Snowfall Analysis"
    # The date follows the word "preceding"
    target_td = soup.find('td', text=re.compile("National Gridded Snowfall Analysis"))
    
    if target_td:
        full_text = target_td.get_text().strip()
        # Extract everything after "preceding "
        match = re.search(r"preceding\s+(.*)$", full_text)
        if match:
            timestamp = match.group(1)
            
            # Save to a JSON file
            with open('timestamp.json', 'w') as f:
                json.dump({"timestamp": timestamp}, f)
            print(f"Successfully scraped: {timestamp}")
            return
            
    print("Could not find timestamp on page.")

if __name__ == "__main__":
    scrape_noaa()
