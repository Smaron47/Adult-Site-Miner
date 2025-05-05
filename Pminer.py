
import requests
from bs4 import BeautifulSoup
import csv
import re
import tkinter as tk
from tkinter import ttk

def extract_video_id(iframe_src):
    match = re.search(r'/video/([^/]+)', iframe_src)
    return match.group(1) if match else None

def get_image_links(url):
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        a_tags = [url + src['href'] for src in soup.find_all('a', class_='image featured non-overlay atfib')]
        print(a_tags)
        # Extract image links from the 'div' tags with the specified class
        div_tags = soup.find_all('div', class_='w403px')
        image_links = []
        for div_tag in div_tags:
            try:
                onmouseout_values = [i["onmouseover"] for i in div_tag.find_all('div', class_="hide_noscript")]
                for onmouseout_value in onmouseout_values:
                    start_index = onmouseout_value.find('changeImage(') + len('changeImage("')
                    end_index = onmouseout_value.find('"', start_index)
                    img_src = onmouseout_value[start_index:end_index]
                    image_links.append('https:'+img_src)
            except:
                print("Error extracting image links")

        return a_tags, image_links

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def get_video_info(url):
    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract categories as a list
        categories = [tag.text for tag in soup.find_all('a', class_='tag-link click-trigger')]

        # Extract title
        title = soup.find('h1', class_='main-h1').text.strip()

        # Extract link
        link = url

        # Extract duration and actors from the header
        header_div = soup.find('div', class_='video-data')
        if header_div:
            # Extract duration
            duration = header_div.find('span', class_='duration').text.strip()

            # Extract actors
            actors = header_div.find('span', class_='starring').text.strip()

        else:
            duration = soup.find('li', class_='icon fa-clock-o').text.strip()
            actors = soup.find('li', class_='icon fa-star-o').text.strip()

        # Extract iframe src attribute
        iframe_tag = soup.find('iframe')
        iframe_src = iframe_tag['src'] if iframe_tag else None

        # Return the extracted information
        return categories, title, link, duration, actors, 'https:'+iframe_src

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def on_url_entry_change(event):
    # Clear the output text widget when the URL entry is changed
    output_text.delete(1.0, tk.END)

def fetch_data():
    # Clear the output text widget
    output_text.delete(1.0, tk.END)
    uv=0
    # Get the URL from the entry widget
    url = url_entry.get().strip()

    # Get image links from the URL
    a_tags, image_links = get_image_links(url)

    if image_links:
        output_text.insert(tk.END, "Image links:\n")
        for img_link in image_links:
            output_text.insert(tk.END, f"{img_link}\n")

        # Create a CSV file to write the data
        with open('video_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write header
            csv_writer.writerow(['Categories', 'Title', 'Link', 'Duration', 'Actors', 'Iframe src', 'Image URLs'])

            # Iterate through each video URL
            for a_tag in a_tags:
                second_code_url = a_tag

                # Get video information from the second code URL
                video_info = get_video_info(second_code_url)

                if video_info:
                    # Extract video ID from iframe src
                    video_id = extract_video_id(video_info[-1])

                    # Check if video ID is in image links
                    matched_image_links = [img_link for img_link in image_links if video_id in img_link]

                    # Save image links to a file
                    with open('image_links.txt', 'w') as img_file:
                        for img_link in image_links:
                            img_file.write(img_link + '\n')
                    output_text.insert(tk.END, "Image links saved to 'image_links.txt'\n")

                    # Write video information along with matched image URLs to the CSV file
                    # Split image links into chunks of 10
                    matched_image_chunks = [image_links[i:i + 10] for i in range(0, len(image_links), 10)]
                    j=0
                    while j < len(matched_image_chunks):
                        matched_image_chunks[j] = str(matched_image_chunks[j])
                        j=j+1
                    k=list(video_info)
                    
                    # print(matched_image_chunks,list(video_info),k)
                    print(matched_image_chunks[uv])
                    
                    csv_writer.writerow(list(video_info) + [matched_image_chunks[uv]])
                    uv=uv+1
                    for image_chunk in matched_image_chunks:
                        output_text.insert(tk.END, "Video information saved to 'video_data.csv'\n")

                        # Print matched image links
                        output_text.insert(tk.END, "Matched Image Links:\n")
                        

                    # Print a separator between videos
                    output_text.insert(tk.END, "\n" + "="*50 + "\n")

# Create the main window
root = tk.Tk()
root.title("Video Data Scraper")

# Create and place widgets
url_label = tk.Label(root, text="Enter URL:")
url_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W)

url_var = tk.StringVar()
url_var.trace_add("write", on_url_entry_change)
url_entry = tk.Entry(root, textvariable=url_var, width=50)
url_entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=0, column=2, pady=10, padx=10, sticky=tk.W)

output_text = tk.Text(root, height=20, width=80)
output_text.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky=tk.W)

# Run the Tkinter event loop
root.mainloop()
