## function to send csv file to slack channel

from slack_sdk import WebhookClient, WebClient
import os
import pandas as pd
import tabulate

__all__ = ['send_file_to_slack','send_message_to_slack','get_slack_webhook']

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
    
# slack_webhook = 'https://hooks.slack.com/services/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' ## pp_image_weight_estimation

def get_slack_webhook(slack_channel='pp_image_weight_estimation'):
    """
    Function to get the slack webhook
    """
    if slack_channel=='pp_image_weight_estimation':
        slack_webhook = 'https://hooks.slack.com/services/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'
    else:
        return 'Invalid slack channel'
    return slack_webhook

def send_message_to_slack(message,slack_channel='pp_image_weight_estimation',is_df=False,tabulate_type='orgtbl'):
    """
    Function to send the message to slack channel. Msg should be a json file. (CSV file not good for this function)
    Args:
        message : str : message to be sent
        is_df : bool : whether the message is a dataframe or not. If True, the message will be taken as a string to be loaded in a dataframe
        slack_webhook : str : webhook url for the slack channel
        tabulate_type : str : type of tabulation to be done. Default is 'orgtbl'. Other is 'grid'
    """
    try :
        slack_webhook = get_slack_webhook(slack_channel)
        client = WebhookClient(url=slack_webhook)
        if is_df:
            df = pd.read_csv(message)
            tab = (tabulate(df,headers=list(), tablefmt=tabulate_type))
            response = client.send(text=tab)
        else:
            response = client.send(text=message)
        return response
    except Exception as e:
        return e