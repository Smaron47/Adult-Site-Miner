# Adult-Site-Miner
The Adult Site Miner is a Python application that scrapes adult-genre webpages for media assets (images and embedded videos), extracts metadata (categories, titles, duration, actors), and saves structured data into CSV and text files. A simple Tkinter GUI allows users to input a page URL, trigger scraping, and view progress and output confirmatio
**Adult Site Miner**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack & Dependencies](#technology-stack--dependencies)
4. [Installation & Setup](#installation--setup)
5. [Usage & Workflow](#usage--workflow)
6. [Code Structure & Function Descriptions](#code-structure--function-descriptions)

   * [`get_image_links(url)`](#get_image_linksurl)
   * [`get_video_info(url)`](#get_video_infourl)
   * [`extract_video_id(iframe_src)`](#extract_video_idiframe_src)
   * [GUI Event Handlers](#gui-event-handlers)
7. [Data Storage & Output Files](#data-storage--output-files)
8. [Error Handling & Logging](#error-handling--logging)
9. [Security & Ethical Considerations](#security--ethical-considerations)
10. [Extensibility & Customization](#extensibility--customization)
11. [Troubleshooting & FAQs](#troubleshooting--faqs)
12. [SEO Keywords](#seo-keywords)

---

## 1. Project Overview

The **Adult Site Miner** is a Python application that scrapes adult-genre webpages for media assets (images and embedded videos), extracts metadata (categories, titles, duration, actors), and saves structured data into CSV and text files. A simple Tkinter GUI allows users to input a page URL, trigger scraping, and view progress and output confirmations.

## 2. Key Features

* **Image Extraction**: Gathers all featured image URLs and thumbnail links.
* **Video Metadata**: Fetches video pages to extract categories, title, duration, actors, and iframe source.
* **Regex Parsing**: Derives a unique video ID from the iframe URL to correlate images.
* **CSV Export**: Compiles all video data into `video_data.csv` with matching image lists.
* **Text File Output**: Saves raw image links to `image_links.txt` for reference.
* **GUI Interface**: Lightweight Tkinter window for URL input and status display.

## 3. Technology Stack & Dependencies

* **Python 3.7+**
* **Requests**: HTTP requests to fetch page HTML.
* **BeautifulSoup (bs4)**: Parses HTML documents.
* **Tkinter**: Builds the desktop GUI.
* **CSV**: Standard module for writing CSV files.
* **re**: Regular expressions for parsing IDs.

Install dependencies via pip:

```bash
pip install requests beautifulsoup4
```

## 4. Installation & Setup

1. Ensure Python 3.7 or later is installed.
2. Install required libraries:

   ```bash
   pip install requests beautifulsoup4
   ```
3. Save the script (e.g. `adult_miner.py`) in your working directory.
4. Run the application:

   ```bash
   python adult_miner.py
   ```

## 5. Usage & Workflow

1. Launch the GUI: a window titled **Video Data Scraper** appears.
2. Enter the target page URL in the **Enter URL:** field.
3. Click **Fetch Data** to start scraping.
4. The output text box displays progress messages.
5. Upon completion:

   * `image_links.txt` contains all raw image URLs.
   * `video_data.csv` lists video metadata and associated image chunks.

## 6. Code Structure & Function Descriptions

### `get_image_links(url)`

* **Inputs**: A gallery or listing page URL.
* **Process**:

  1. HTTP GET request to the URL.
  2. Parse response with BeautifulSoup.
  3. Collect `<a>` tags of featured images and `<div>` elements storing image onmouseover scripts.
  4. Extract `changeImage("...")` arguments to form full image URLs.
* **Returns**: Tuple `(video_page_links, image_links)`.

### `get_video_info(url)`

* **Inputs**: A specific video page URL.
* **Process**:

  1. HTTP GET request to the URL.
  2. Parse HTML to find:

     * Categories via `<a class="tag-link">`.
     * Title in `<h1 class="main-h1">`.
     * Duration and actors from `<div class="video-data">` or fallback `<li>` elements.
     * Iframe `src` attribute.
* **Returns**: `(categories, title, link, duration, actors, iframe_src)`.

### `extract_video_id(iframe_src)`

* Uses regex `r'/video/([^/]+)'` to capture the unique video identifier from an iframe URL.

### GUI Event Handlers

* **`on_url_entry_change(event)`**: Clears the output box when the URL field changes.
* **`fetch_data()`**:

  1. Clears previous output.
  2. Calls `get_image_links` to discover pages and images.
  3. Writes raw image links to `image_links.txt`.
  4. Iterates through video page URLs:

     * Calls `get_video_info`.
     * Extracts the video ID via `extract_video_id`.
     * Matches and groups relevant image URLs.
     * Writes combined data into `video_data.csv`.
     * Updates the GUI text box with status notes.

## 7. Data Storage & Output Files

* **`image_links.txt`**: Newline-separated raw image URLs.
* **`video_data.csv`**: Comma-separated file with columns:
  `Categories, Title, Link, Duration, Actors, Iframe src, Image URLs (chunked)`.

## 8. Error Handling & Logging

* HTTP errors reported via status code checks.
* Broad `except` blocks protect against missing elements without halting the entire process.
* GUI remains responsive; failures note in the console and text box.

## 9. Security & Ethical Considerations

* **Responsible Scraping**: Respect the site’s `robots.txt` and rate limits.
* **Age Restrictions**: Ensure legal compliance before mining adult content.
* **Privacy**: Do not store or share personally identifiable information.

## 10. Extensibility & Customization

* **Pagination**: Enhance `get_image_links` to navigate multiple pages.
* **Threading**: Add multithreading to speed up video data fetching.
* **Formats**: Export to JSON or Excel instead of CSV.
* **GUI**: Upgrade to PyQt5 for richer interfaces.

## 11. Troubleshooting & FAQs

* **No Output**: Verify the URL is correct and accessible.
* **Parsing Errors**: Update class names/XPaths if site HTML changes.
* **CSV Write Failures**: Ensure write permissions in the working directory.

## 12. SEO Keywords

```
adult site scraper
beautifulsoup adult miner
tkinter web scraper adult
python video metadata extractor
requests beautifulsoup tutorial
adult content csv export
adult site scraper
beautifulsoup adult miner
tkinter web scraper adult
python video metadata extractor
requests beautifulsoup tutorial
adult content csv export
```
