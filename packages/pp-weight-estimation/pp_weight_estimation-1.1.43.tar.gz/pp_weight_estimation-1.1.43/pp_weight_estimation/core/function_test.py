import transformers as t
from PIL import Image
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mb_utils.src import logging
from pp_weight_estimation.core.get_weight import get_seg, get_final_mask, get_final_img, get_histogram, get_val
from pp_weight_estimation.core.s3_io import get_client, download_image
from pp_weight_estimation.core.gpt_support import get_count
from urllib.parse import urlparse
from typing import List,Dict,Union
import cv2
import yaml
import boto3

logger = logging.logger 
#model_checkpoint = '/Users/test/test1/mit-segformer-s' 
#model = t.TFSegformerForSemanticSegmentation.from_pretrained(model_checkpoint)

__all__ = ["load_color_values", "process_pipeline"]

def load_config(yaml_path: str) -> dict:
    """
    Function to load configurations from a YAML file
    Args:
        yaml_path (str): Path to the YAML file
    Returns:
        dict: Dictionary containing configurations
    """
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_color_values(csv_path : str, logger: logging.Logger = None) -> Dict:
    """
    Function to load color values from a CSV file
    Args:
        csv_path (str): Path to the CSV file
        logger (Logger): Logger object
    Returns:
        dict: Dictionary containing color values
    """
    if logger:
        logger.info("Loading color values from CSV")
    color_dict = {}
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        taxcode = row['taxonomy_code']
        site = row['site_id']
        color = row['colors']
        if taxcode and site and color:
            composed_key = f"{site}_{taxcode}"
            color_list = eval(color)
            color_dict[composed_key] = color_list
    return color_dict

def process_pipeline(config_path: str, logger: logging.Logger = None, **kwargs) -> Union[pd.DataFrame, List]:
    """
    Function to process the pipeline of Production Planning.
    
    This function automates the process of downloading images from an S3 bucket, applying segmentation and masking,
    calculating histograms, and saving the results to an output CSV file. The function uses configurations provided
    in a YAML file for flexibility.

    Args:
        config_path (str): Path to the YAML configuration file.
        logger (logging.Logger): Logger object for logging messages (optional).
        **kwargs: Additional keyword arguments (optional).
        
    Returns:
        tuple: A tuple containing:
            - str: The path to the output CSV file.
            - list: A list of results for each processed image.
    """
    config = load_config(config_path)

    input_csv_path = config['data']['input_csv_path']
    gt_csv_path = config['data']['gt_csv_path']
    val_color_csv_path = config['data']['val_color_csv_path']
    path_to_save_images = config['data']['path_to_save_images']
    
    save_plots = config['results'].get('save_plots', False)
    final_mask_vals = config['results'].get('final_mask_vals', 50)
    mask_val = config['results'].get('model_val', 0.08)
    new_bg_removal = config['results'].get('background_removal', True)
    equalizer_items = config['results'].get('equalizer_items')

    model_path = config['model']['model_path']
    model_name = config['model']['model_name']
    model_version = config['model']['model_version']

    bucket = config['aws_data']['bucket_name']
    profile = config['aws_data']['profile']

    gpt_response = config['gpt_res'].get('gpt_response', False)
    gpt_token = config['gpt_res'].get('gpt_token', None)
    gpt_model = config['gpt_res'].get('gpt_model', None)
    gpt_prompt = config['gpt_res'].get('gpt_prompt', None)
    gpt_file_path = config['gpt_res'].get('gpt_file_path', None)
    gpt_api_key = config['gpt_res']['gpt_api_key']

    model = t.TFSegformerForSemanticSegmentation.from_pretrained(model_path)  

    #might have to be change this
    session = boto3.Session(profile_name=profile)
    client = session.client('s3')

    color_dict = load_color_values(val_color_csv_path)
    groundtruth_df = pd.read_csv(gt_csv_path)
    input_df = pd.read_csv(input_csv_path)
    input_df['mask'] = ''
    input_df['final_image'] = ''
    input_df['pixel_count'] = 0
    input_df['histogram'] = ''
    input_df['pred_w2'] = 0.0
    input_df['error'] = 0.0
    input_df['success'] = False

    use_input_groundtruth = 'input_groundtruth' in input_df.columns

    entries = []
    for _, row in input_df.iterrows():
        local_image_path = row['s3_image_path']
        site_id = row['site_id']
        taxonomy_code = row['taxonomy_code']
        food_item = row['food_item']
        input_groundtruth = row['input_groundtruth'] if use_input_groundtruth else 0
        if local_image_path and site_id and taxonomy_code:
            composed_key = f"{site_id}_{taxonomy_code}"
            entries.append((site_id, local_image_path, composed_key, taxonomy_code))
    
    if not entries:
        if logger:
            logger.error("No valid entries found in the CSV file")
        raise ValueError("No valid entries found in the CSV file")
    
    results = []
    for index, (site_id, local_image_path, composed_key, taxonomy_code) in enumerate(entries):
        try:
            if composed_key not in color_dict:
                if logger:
                    logger.error(f"No color found for key {composed_key}. Skipping image {local_image_path}.")
                input_df.at[index, 'success'] = False
                continue
            colors = color_dict[composed_key]
        
            site_dir = os.path.join(path_to_save_images, 'images' , site_id)
            os.makedirs(site_dir, exist_ok=True)
        
            original_filename = os.path.basename(local_image_path)
            save_filename, _ = os.path.splitext(os.path.basename(local_image_path))
            download_path = os.path.join(site_dir, original_filename)
        
            if logger:
                logger.info(f"Processing image: {local_image_path}")

            image = download_image(bucket, local_image_path, client)
            image.save(download_path)
            ori_img = cv2.imread(download_path)

            masked_img = get_seg(local_image_path, model, mask_val=mask_val, resize=True, new_bg_removal=new_bg_removal, equalize=True)

            final_mask = None
            for color in colors:
                mask = get_final_mask(ori_img, masked_img, color=color, val=final_mask_vals, logger=logger)
                if final_mask is None:
                    final_mask = mask
                else:
                    final_mask = cv2.bitwise_or(final_mask, mask)

            masks_dir = os.path.join(path_to_save_images, 'masks')
            os.makedirs(masks_dir, exist_ok=True)
            mask_save_path = os.path.join(masks_dir, f"{save_filename}_mask_{final_mask_vals}.png")
            mask_image = Image.fromarray(final_mask.astype(np.uint8))
            mask_image.save(mask_save_path)
            input_df.at[index, 'mask'] = mask_save_path

            new_final_img = get_final_img(masked_img, final_mask, mask_val=mask_val)

            final_images_dir = os.path.join(path_to_save_images, 'final_image')
            os.makedirs(final_images_dir, exist_ok=True)
            final_img_save_path = os.path.join(final_images_dir, f"{save_filename}_final.png")
            final_image = Image.fromarray(new_final_img.astype(np.uint8))
            final_image.save(final_img_save_path)
            input_df.at[index, 'final_image'] = final_img_save_path

            final_image_np = np.array(final_image)

            new_histogram, bin_edges = get_histogram(final_image_np)

            pixel_count = new_histogram[-1]
            pixel_count = pixel_count.astype(int)
            input_df.at[index, 'pixel_count'] = pixel_count

            if save_plots:
                plots_dir = os.path.join(path_to_save_images, 'image_plots')
                os.makedirs(plots_dir, exist_ok=True)
                
                hist_plot_path = os.path.join(plots_dir, f"{save_filename}_hist_plot.png")
                input_df.at[index, 'histogram'] = hist_plot_path             
                plt.savefig(hist_plot_path)
                plt.close()
            else:
                plt.close()

            reference_row = groundtruth_df[groundtruth_df['taxonomy_code'] == taxonomy_code]
            if not reference_row.empty:
                reference_pixel_count = reference_row.iloc[0]['reference_pixel_count']
                groundtruth_weight = reference_row.iloc[0]['groundtruth']

                weight2 = input_groundtruth if input_groundtruth else 0
                pred_w2, error = get_val(reference_pixel_count, pixel_count, groundtruth_weight, weight2)
            else:
                if logger:
                    logger.error(f"No groundtruth data found for taxonomy_code {taxonomy_code}.")

            input_df.at[index, 'pred_w2'] = pred_w2
            input_df.at[index, 'error'] = error

            if gpt_response:
                gpt_result = get_count(image_path = local_image_path, item = food_item, api_key = gpt_api_key, df_loc = gpt_file_path, prompt = gpt_prompt)
                gpt_error = (weight2-gpt_result)/weight2
                input_df.at[index, 'gpt_result'] = gpt_result
                input_df.at[index, 'gpt_error'] = gpt_error
                input_df.at[index, 'success'] = True if gpt_result is not None else False
            else:    
                input_df.at[index, 'success'] = True if pred_w2 is not None else False

            results.append((masked_img, final_mask, new_final_img, new_histogram, pred_w2, error, gpt_result, gpt_error))
        except Exception as e:
            if logger:
                logger.error(f"Error processing image {local_image_path}: {e}")
            input_df.at[index, 'success'] = False
            continue
    
    output_csv_dir = os.path.join(path_to_save_images, 'csv', site_id, 'output_csv')
    os.makedirs(output_csv_dir, exist_ok=True)
    output_csv_path = os.path.join(output_csv_dir, "output.csv")
    input_df.to_csv(output_csv_path, index=False)

    if logger:
        logger.info(f"Processing complete. Output saved to {output_csv_path}")
        
    return output_csv_path, results


# add logger - done
# error if there is not taxcode and skip that image - done
# column to output with failure or success -done
# new csv with refrence image and groundtruth, and histogram pixel inside segmentation, model-checkpoint - done
# download to GH2  particular location - done
# save everything mask(save the 50 val in the name of file as _50) histogram and final image - done 
# save everything locally - done
# save the plots locally only when input is given add plot boolean input to process_pipeline at images_plot folder - done
# yaml file for inputs -done
# write the _mask after the name - done
# s3cmd ls s3://pp-image-capture-processed-useast1-prod/siteId=33263/mealService=b514a5da-2bcf-4330-8a3c-f17e7f85a922/
# get-repsonse -> get-image -> download image -> 
# aslo csv files