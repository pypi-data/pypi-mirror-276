## function to send csv file to slack channel

from slack_sdk import WebhookClient, WebClient
import os

slack_token = os.environ['SLACK_API_TOKEN'] 

def send_file_to_slack(file_path,slack_token,slack_channel):
    """
    Function to send the file to slack channel
    """
    try :
        
        client = WebClient(token=slack_token)
        response = client.files_upload(
            channels=slack_channel,
            file=file_path)
        return response
    except Exception as e:
        return e
    
slack_webhook = os.environ['SLACK_WEBHOOK'] ##  https://hooks.slack.com/services/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

def send_message_to_slack(message,slack_webhook):
    """
    Function to send the message to slack channel. Msg should be a json file. (CSV file not good for this function)
    """
    try :
        client = WebhookClient(url=slack_webhook)
        response = client.send(text=message)
        return response
    except Exception as e:
        return e