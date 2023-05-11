import requests
from bs4 import BeautifulSoup
from termcolor import colored
import re

# Function to add scheme to URL if missing
def prepare_url(url):
    if not re.match('^https?://', url):
        url = 'http://' + url
    return url

# Function to perform SEO audit
def seo_audit(url):
    # Send a GET request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the title of the page
    title = soup.title.string

    # Check if the title is empty
    if title.strip() == '':
        print(colored("Title: Missing", "magenta"))
    else:
        print(colored(f"Title: {title}", "magenta"))

    # Check the length of the title
    title_length = len(title)
    if title_length > 70:
        print(colored(f"Title Length: {title_length} (Too Long)", "yellow"))
    else:
        print(colored(f"Title Length: {title_length}", "yellow"))

    # Check if the page contains meta description
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        print(colored(f"Meta Description: {meta_description['content']}", "yellow"))
    else:
        print(colored("Meta Description: Missing", "yellow"))

    # Check if the page contains H1 heading
    h1_heading = soup.find('h1')
    if h1_heading:
        print(colored(f"H1 Heading: {h1_heading.string}", "yellow"))
    else:
        print(colored("H1 Heading: Missing", "yellow"))

    # Check if the page contains images with alt text
    images = soup.find_all('img')
    missing_alt_text = 0
    images_without_alt = []
    for image in images:
        if not image.has_attr('alt') or image['alt'].strip() == '':
            missing_alt_text += 1
            images_without_alt.append(image['src'])
    if missing_alt_text > 0:
        print(colored(f"Images with Missing Alt Text: {missing_alt_text}", "yellow"))
        print(colored("Links to Images without Alt Text:", "yellow"))
        for image_url in images_without_alt:
            print(image_url)
    else:
        print(colored("All Images have Alt Text", "yellow"))

    # Check if the page contains internal and external links
    internal_links = soup.find_all('a', href=re.compile(url))
    external_links = soup.find_all('a', href=lambda href: href and not re.compile(url).search(href))
    print(colored(f"Internal Links: {len(internal_links)}", "yellow"))
    print(colored(f"External Links: {len(external_links)}", "yellow"))

    # Calculate the overall rating based on certain criteria
    rating = 0
    if title.strip() != '':
        rating += 1
    if title_length <= 70:
        rating += 1
    if meta_description:
        rating += 1
    if h1_heading:
        rating += 1
    if missing_alt_text == 0:
        rating += 1
    if len(internal_links) > 0:
        rating += 1

    # Display the rating
    print(colored(f"SEO Rating: {rating}/6", "yellow"))

# Main script
website_url = input("Enter the website URL: ")
website_url = prepare_url(website_url)
seo_audit(website_url)
