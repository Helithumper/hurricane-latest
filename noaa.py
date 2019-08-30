import requests
import feedparser
import bs4

def get_latest_graphic():
    rss = feedparser.parse('https://www.nhc.noaa.gov/nhc_at5.xml')
    graphics_entry = next(
        (x for x in rss['entries'] if 'Graphic' in x['title']), 
        None)
    graphics_title = graphics_entry['title']
    published_datetime = graphics_entry['published']
    image_url_items = graphics_entry['summary'].split('\n')
    image_url_tagged = next(
        (x for x in image_url_items if '5day_cone' in x),
        None
    )
    image_url_clean = image_url_tagged.split('\"')[1].replace('_sm2','')
    
    returned_object = {
        'title': graphics_title,
        'image_url': image_url_clean,
        'time_published': published_datetime
    }
    return returned_object


def get_latest_report():
    rss = feedparser.parse('https://www.nhc.noaa.gov/nhc_at5.xml') 
    report_entry = next(
        (x for x in rss['entries'] if 'Summary for' in x['title']),
        None
    )
    report_title = report_entry['title']
    published_datetime = report_entry['published']
    report_link = report_entry['link']
    report_text = get_report(report_link)

    returned_object = {
        'title': report_title,
        'link': report_link,
        'time_published': published_datetime,
        'report_text': report_text
    }
    return returned_object

def get_report(report_link):
    ## Get Raw Text of Report
    report_response = requests.get(report_link)
    soup = bs4.BeautifulSoup(report_response.text, 'html.parser')
    message = soup.findAll('div',{'class':'textproduct'})[0]
    message = message.find('pre')
    message = message.find(text=True)

    ## Clean up leading spaces and trailing spaces
    message = message.strip()

    return message

if __name__ == "__main__":
    print(get_latest_report())