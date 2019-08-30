import json
import os
import time
import sys

from noaa import get_latest_graphic, get_latest_report
from utilities import should_post_graphic, format_graphic, slack_post, format_report, should_post_report


def get_latest_graphic_and_post(event, context):
    graphic = get_latest_graphic()
    print(f"Newest Graphic Time {graphic['time_published']}")
    if should_post_graphic(graphic):
        print("Determined correct time to post graphic")
        graphic_content = format_graphic(graphic)
        response = slack_post(graphic_content, 
                              os.environ.get('SLACK_URL'))
        if response != True:
            print(f"Error Posting to Slack: {response}")
    else:
        print("Incorrect time to post graphic.")
    return "Completed"

def get_latest_report_and_post(event, context):
    report = get_latest_report()
    print(f"Newest Report Time {report['time_published']}")
    if should_post_report(report):
        print("Determined correct time to post report")
        slack_payload = format_report(report)
        response = slack_post(slack_payload,
                              os.environ.get('SLACK_URL'))
        if response != True:
            print(f"Error posting to Slack: {response}")
    else:
        print("Incorrect time to post report.")
    return "Completed"

if __name__ == "__main__":
    get_latest_graphic_and_post(None, None)