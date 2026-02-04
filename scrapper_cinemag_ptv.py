import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Channel URLs with their corresponding IDs - UPDATED WITH ALL LINKS
CHANNEL_URLS = {
    "DIGI24 HD": {"url": "https://m.cinemagia.ro/program-tv/digi-24-hd/", "id": 1},
    "ANTENA3": {"url": "https://programtv.ro/canal-tv/antena-3-cnn", "id": 2},
    "B1": {"url": "https://programtv.ro/canal-tv/b1-tv", "id": 3},
    "PROTV": {"url": "https://programtv.ro/canal-tv/pro-tv", "id": 7},
    "ANTENA1": {"url": "https://m.cinemagia.ro/program-tv/antena-1-hd/", "id": 8},
    "TVR1": {"url": "https://m.cinemagia.ro/program-tv/tvr-1-hd/", "id": 4},
    "TVR2": {"url": "https://m.cinemagia.ro/program-tv/tvr-2-hd/", "id": 5},
    "Kanal D": {"url": "https://m.cinemagia.ro/program-tv/kanal-d-hd/", "id": 9},
    "Prima TV": {"url": "https://m.cinemagia.ro/program-tv/prima-tv-hd/", "id": 10},
    "TVR3": {"url": "https://m.cinemagia.ro/program-tv/tvr-3/", "id": 11},
    "TVR International": {"url": "https://m.cinemagia.ro/program-tv/tvr-international/", "id": 12},
    "Digi 24": {"url": "https://m.cinemagia.ro/program-tv/digi-24-hd/", "id": 13},
    "PROCINEMA": {"url": "https://m.cinemagia.ro/program-tv/pro-cinema/", "id": 14},
    "ANTENA STARS": {"url": "https://m.cinemagia.ro/program-tv/antena-stars-hd/", "id": 15},
    "National Geographic": {"url": "https://m.cinemagia.ro/program-tv/national-geographic-hd/", "id": 16},
    "TVR Cultural": {"url": "https://programtv.ro/canal-tv/tvr-cultural", "id": 17},
    "HBO": {"url": "https://m.cinemagia.ro/program-tv/hbo/", "id": 20},
    "HBO_2": {"url": "https://m.cinemagia.ro/program-tv/hbo-2/", "id": 21},
    "FilmNow": {"url": "https://m.cinemagia.ro/program-tv/film-now-hd/", "id": 25},
    "Atomic-TV": {"url": "https://programtv.ro/canal-tv/atomic-tv", "id": 26},
    "ZU-TV": {"url": "https://m.cinemagia.ro/program-tv/zu-tv/", "id": 27},
    "MUSIC-CHANNEL": {"url": "https://m.cinemagia.ro/program-tv/music-channel/", "id": 28},
    "KISS-TV": {"url": "https://m.cinemagia.ro/program-tv/kiss-tv/", "id": 29},
    "TVR Folclor": {"url": "https://programtv.ro/canal-tv/tvr-folclor", "id": 30},
    "ETNO TV": {"url": "https://m.cinemagia.ro/program-tv/etno-tv/", "id": 80},
    "REALITATEA": {"url": "https://m.cinemagia.ro/program-tv/realitatea-plus/", "id": 31},
    "PRIMA-NEWS": {"url": "https://programtv.ro/canal-tv/prima-news", "id": 32},
    "EURO-NEWS": {"url": "https://programtv.ro/canal-tv/euronews-romania-hd", "id": 33},
    "CNN-LIVE": {"url": "https://m.cinemagia.ro/program-tv/cnn/", "id": 34},
    "BBC-NEWS": {"url": "https://m.cinemagia.ro/program-tv/bbc-world-news/", "id": 35},
    "CBS-REALITY": {"url": "https://m.cinemagia.ro/program-tv/cbs-reality/", "id": 36},
    "PRS-1": {"url": "https://programtv.ro/canal-tv/prima-sport-1", "id": 38},
    "PRS-2": {"url": "https://programtv.ro/canal-tv/prima-sport-2", "id": 39},
    "ER1": {"url": "https://m.cinemagia.ro/program-tv/eurosport-1/", "id": 40},
    "ER2": {"url": "https://m.cinemagia.ro/program-tv/eurosport-2/", "id": 41},
    "CARTOON": {"url": "https://m.cinemagia.ro/program-tv/cartoon-network/", "id": 42},
    "DISCOVERY-CHANNEL": {"url": "https://programtv.ro/canal-tv/discovery-channel", "id": 44},
    "VIA-HIS": {"url": "https://m.cinemagia.ro/program-tv/viasat-history/", "id": 44},
    "VIA-EXPLORER": {"url": "https://m.cinemagia.ro/program-tv/viasat-explore/", "id": 46},
    "BBC-EARTH": {"url": "https://m.cinemagia.ro/program-tv/bbc-earth-hd/", "id": 47},
    "Rock TV": {"url": "https://m.cinemagia.ro/program-tv/rock-tv-hd/", "id": 50},
    "Canal32": {"url": "https://programtv.ro/canal-tv/canal-32", "id": 51},
    "Magic TV": {"url": "https://m.cinemagia.ro/program-tv/magic-tv-hd/", "id": 52},
    "CBS News": {"url": "https://programtv.ro/canal-tv/cbs-news", "id": 55},
    "DigiSport 1": {"url": "https://m.cinemagia.ro/program-tv/digi-sport-1/", "id": 56},
    "France24": {"url": "https://m.cinemagia.ro/program-tv/france-24/", "id": 74},
    "TVR Sport": {"url": "https://programtv.ro/canal-tv/tvr-sport", "id": 77},
    "Romania TV": {"url": "https://m.cinemagia.ro/program-tv/romania-tv/", "id": 78},
    "AMC": {"url": "https://m.cinemagia.ro/program-tv/amc-hd/", "id": 23},
    "DigiSport 2": {"url": "https://m.cinemagia.ro/program-tv/digi-sport-2/", "id": 91},
    "CineMax": {"url": "https://m.cinemagia.ro/program-tv/cinemax/", "id": 321},
    "CineMax2": {"url": "https://m.cinemagia.ro/program-tv/cinemax-2/", "id": 322},
    "Viasat-Nature": {"url": "https://m.cinemagia.ro/program-tv/viasat-nature/", "id": 99935},
    "HBO3": {"url": "https://m.cinemagia.ro/program-tv/hbo-3-hd/", "id": 538722},
    "CineMaraton": {"url": "https://m.cinemagia.ro/program-tv/cinemaraton/", "id": 26563}
}


def scrape_programtv_ro(channel_name, url, soup):
    """Scrape program list from programtv.ro channel page"""
    program_list = []

    # Find the main container for programtv.ro
    main_container = soup.find("div", class_="background-white")
    if not main_container:
        print(f"⚠️ Could not find schedule container for {channel_name} (programtv.ro)")
        return []

    entries = main_container.find_all("div", class_="d-flex justify-content-start")

    for entry in entries:
        time_tag = entry.find("p", class_="px-3 pt-2 fw-bold")
        title_tag = entry.find("h2")
        live_tag = entry.find("span", class_="tv-show-live")

        time = time_tag.get_text(strip=True) if time_tag else ""
        title = title_tag.get_text(" ", strip=True) if title_tag else ""
        live = f" ({live_tag.get_text(strip=True)})" if live_tag else ""

        if title:
            full_text = f"{time} - {title}{live}".strip()

            # Remove unwanted fragments
            full_text = re.sub(r"👉 Vezi detalii", "", full_text, flags=re.IGNORECASE)
            full_text = re.sub(r"\(ACUM\)", "", full_text, flags=re.IGNORECASE)
            full_text = re.sub(r"\bACUM\b", "", full_text, flags=re.IGNORECASE)

            # Remove duplicated titles like "Pasagerii - Pasagerii"
            full_text = re.sub(
                r"^(.*? - )(.+?)\s*-\s*\2(\b|$)",
                r"\1\2",
                full_text,
                flags=re.IGNORECASE
            )

            # Clean up extra spaces
            full_text = re.sub(r"\s{2,}", " ", full_text).strip()

            program_list.append(full_text)

    return program_list


def scrape_cinemagia_ro(channel_name, url, soup):
    """Scrape program list from m.cinemagia.ro channel page"""
    program_list = []

    # Find the main container for m.cinemagia.ro
    main_container = soup.find("ul", class_="show_list", id="ShowList")

    if not main_container:
        print(f"⚠️ Could not find show_list container for {channel_name} (cinemagia.ro)")
        return []

    # Find all list items within the show_list container
    entries = main_container.find_all("li")

    for entry in entries:
        # Find time element
        time_tag = entry.find("div", class_="hour") or entry.find("span", class_="time")

        # Find title element
        title_tag = entry.find("a") or entry.find("span", class_="title") or entry.find("div", class_="title")

        # Find live indicator if exists
        live_tag = entry.find("span", class_="live") or entry.find("span", class_="tv-show-live")

        # Extract text
        time = time_tag.get_text(strip=True) if time_tag else ""
        title = title_tag.get_text(" ", strip=True) if title_tag else ""
        live = f" ({live_tag.get_text(strip=True)})" if live_tag else ""

        if title:
            # Remove the time from the beginning of the title if it starts with the same time
            time_pattern = re.compile(rf"^{re.escape(time)}\s*[-:\s]\s*")
            title = time_pattern.sub("", title)

            # Alternative: Remove any duplicate time that appears at the start of title
            if title.startswith(time):
                title = title[len(time):].lstrip(" -:")

            full_text = f"{time} - {title}{live}".strip()

            # Remove unwanted fragments
            full_text = re.sub(r"👉 Vezi detalii", "", full_text, flags=re.IGNORECASE)
            full_text = re.sub(r"\(ACUM\)", "", full_text, flags=re.IGNORECASE)
            full_text = re.sub(r"\bACUM\b", "", full_text, flags=re.IGNORECASE)

            # Remove duplicated titles like "Pasagerii - Pasagerii"
            full_text = re.sub(
                r"^(.*? - )(.+?)\s*-\s*\2(\b|$)",
                r"\1\2",
                full_text,
                flags=re.IGNORECASE
            )

            # Clean up extra spaces
            full_text = re.sub(r"\s{2,}", " ", full_text).strip()

            program_list.append(full_text)

    return program_list


def scrape_programtv(channel_name, url):
    """Main function to scrape program list - detects website type automatically"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching {channel_name}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Determine which website we're scraping based on the URL
    if "programtv.ro" in url:
        return scrape_programtv_ro(channel_name, url, soup)
    elif "cinemagia.ro" in url:
        return scrape_cinemagia_ro(channel_name, url, soup)
    else:
        print(f"⚠️ Unknown website for {channel_name}, trying both methods...")
        # Try both methods
        program = scrape_programtv_ro(channel_name, url, soup)
        if not program:
            program = scrape_cinemagia_ro(channel_name, url, soup)
        return program


def scrape_all_channels(channel_urls):
    """Scrape all channels and format output for JSON"""
    all_channels = []

    for name, channel_data in channel_urls.items():
        print(f"🔎 Scraping {name}...")
        program = scrape_programtv(name, channel_data["url"])

        if program:
            print(f"   ✓ Found {len(program)} programs")
        else:
            print(f"   ⚠️ No programs found")

        all_channels.append({
            "id": channel_data["id"],
            "tv_channel": name,
            "tv_program": program
        })

    return all_channels


def save_to_json(data, filename="tv_schedule.json"):
    """Save results to JSON"""
    if not data:
        print("⚠️ No data to save.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Saved schedule for {len(data)} channels to {filename}")


if __name__ == "__main__":
    print("🎬 Starting TV schedule scraping...")
    print("📺 Sources: programtv.ro and m.cinemagia.ro")
    print("=" * 50)

    results = scrape_all_channels(CHANNEL_URLS)

    # Count successful channels
    successful = sum(1 for channel in results if channel["tv_program"])
    print(f"\n📊 Results: {successful}/{len(results)} channels scraped successfully")

    save_to_json(results, "tv_schedule.json")
    print("🏁 Done at", datetime.now().strftime("%H:%M:%S"))
