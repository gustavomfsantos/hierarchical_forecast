# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 16:41:52 2023

@author: gusta
"""


import os 
import time
import pandas as pd

import selenium
print(selenium.__version__)
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path_raw_data = r'C:\Users\gusta\Desktop\Personal_Projects\Nixtla_Forecast\Raw_Data'
path_processed_data = r'C:\Users\gusta\Desktop\Personal_Projects\Nixtla_Forecast\Processed_Data'
scrap_link = 'https://dados.turismo.gov.br/dataset/chegada-de-turistas-internacionais'

def download_raw_data():
    
    
    chrome_options = Options()
    
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome( chrome_options)    
    driver.get(scrap_link)
    
    resource_items = driver.find_elements(By.CLASS_NAME,"resource-item a")
    
    
    
    link_list = []
    for resource_item in resource_items:
        # print(resource_item.text) 
        # print(resource_item.get_attribute("href"))
        link_list.append(resource_item.get_attribute("href"))
    
    
    csv_files = [item for item in link_list if item.endswith(".csv")]
    
    driver.quit()
    
    chrome_options_aux = Options()
    chrome_options_aux.add_argument("--window-size=1920,1080")#("--headless")
    chrome_options_aux.add_experimental_option("prefs", {
        "download.default_directory": path_raw_data
    })
    driver_aux = webdriver.Chrome( chrome_options_aux)    
    
    
    files = os.listdir(path_raw_data)
    if len(files)>0:
        for file in files:
            os.remove(os.path.join(path_raw_data, f'{file}'))
            
    for link in csv_files:
        print(link)
        
        driver_aux.get(link)
        time.sleep(5)
        
    driver_aux.quit()

    return "Download Done"

def transform_data():
    files = os.listdir(path_raw_data)
    
    final_df = pd.DataFrame()
    
    for file in files:
        print(file)
        df = pd.read_csv(os.path.join(path_raw_data, file),  encoding = "ISO-8859-1", sep = ';')
        df = df.rename(columns = {'Ano':'ano', 'cod mes':'Ordem mês', 'Via':'Via de acesso'})
        df = df.groupby(['UF', 'ano', 'Ordem mês', 'Mês', 'Via de acesso']).sum(['Chegadas'])
        df = df[[ 'Chegadas']].reset_index()
        df['Ordem mês'] = df['Ordem mês'].astype(str).str.zfill(2)
        df['Date'] = pd.to_datetime(df['ano'].astype(str) + '-' +  df['Ordem mês'] + '-01')
        df = df.drop ([ 'ano', 'Ordem mês', 'Mês'], axis =1)
        final_df = pd.concat([final_df, df], ignore_index=True)
    

    final_df['top_level'] = 'Brasil'
    final_df['middle_level'] = final_df['UF']
    final_df['bottom_level'] = final_df['Via de acesso']
    final_df = final_df.rename(columns = {'Date':'ds', 'Chegadas':'y'})
   
    final_df = final_df[[ 'ds', 'top_level', 'middle_level', 'bottom_level', 'y']]
    final_df.to_csv(os.path.join(path_processed_data, 'processed_data.csv'), sep = ';')
    
    #Delete Raw Data after processed Data 
    for file in files:
        os.remove(os.path.join(path_raw_data, f'{file}'))
    return 'Processed Data Saved'
    

if __name__ == "__main__":
    

    download_raw_data()
    transform_data()
    
    
    