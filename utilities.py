from datetime import datetime, timedelta
import requests

def should_post_graphic(graphic):
    return within_bounds(graphic['time_published'])

def should_post_report(report):
    return within_bounds(report['time_published'])

def within_bounds(time, lower_bound=45, upper_bound=45):
    current_time = datetime.now()
    lower_bound = current_time - timedelta(minutes=lower_bound)
    upper_bound = current_time + timedelta(minutes=upper_bound)

    format = "%a, %d %b %Y %H:%M:%S %Z"
    report_time = datetime.strptime(time, format)
    
    if report_time < lower_bound or report_time > upper_bound:
        return False

    return True

def slack_post(payload, slack_url):
    response = requests.post(slack_url, json=payload)
    if response.status_code == 200:
        return True
    else:
        return response.text

def format_graphic(graphic):
    payload = {
        'text': f"*{graphic['title']}*",
        'attachments': [
            {
                'color': 'danger',
                'text': f'Published {graphic["time_published"]}',
                'image_url': graphic['image_url']
            }
        ]
    }
    return payload

def format_report(report):
    payload = {
        'text': f"*{report['title']}*",
        'attachments': [
            {
                'title': report['link'],
                'color': 'danger',
                'text': f"```{report['report_text']}```"
            }
        ]
    }
    return payload