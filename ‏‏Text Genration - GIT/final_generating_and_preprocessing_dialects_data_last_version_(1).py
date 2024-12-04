# -*- coding: utf-8 -*-
"""Final_Generating_and_Preprocessing_Dialects_Data_last_version (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/116ZqaKO7edCDYYQz75HuKv6ASqxDndHt

# **Getting Data**
"""

!gdown 1xwoKclfvbkDyHBbLaMOGKCF1yQrM-Q6A

from google.colab import drive
drive.mount('/content/drive')

!pip install langchain
!pip install openai
!pip install langchain_community

from google.colab import drive
import pandas as pd
# Read the CSV file
df_MSA = pd.read_csv('/content/longest_captions_dataset -1500 samples.csv')
df_MSA.head()

df_MSA['text'] = df_MSA['text'].str.replace(',', '')
df_MSA['text'] = df_MSA['text'].str.replace('،', '')

# numbering the sentences
df_MSA['text'] = df_MSA.index.to_series().apply(str) + '-' + df_MSA['text']
df_MSA.head()

df_MSA['text'].head(10)

"""# **Generating Fuction for Egyptain Dataset**"""

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the ChatOpenAI model with your API key
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="") #Put your API here

def generate_response(sentences):
    # Define the prompt template for the MSA to multiple Arabic dialects translation
    # Removed placeholders for dialect outputs as they will be generated by the LLM
    template = """
تصرّف كمترجم من اللغة العربية الفصحى الحديثة إلى اللهجه المصريه العامية جدًا كما يتحدث بها الناس في حياتهم اليومية.أجب فقط بالشكل المطلوب دون إضافة كلمات إضافية.
    ملاحظة: كل جملة بالعربية الفصحى مرقمة، أعد الجملة المترجمة إلى اللهجة المصرية بنفس الترقيم، لا تضف أو تحذف أي شيء.
    الجمل بالعربية الفصحى:
    {arabic_sentences}
    اللهجة المصرية:

"""

    # Create a prompt template object using LangChain
    prompt_template = PromptTemplate(
        input_variables=["arabic_sentences"],
        template=template
    )

    # Format the prompt by inserting the MSA sentences
    formatted_prompt = prompt_template.format(
        arabic_sentences=sentences
    )

    # Send the prompt to the OpenAI model and get the response
    result = llm([HumanMessage(content=formatted_prompt)])

    # Process the response and extract the three dialect outputs separately
    response = result.content
    return response


# Example usage with multiple samples
chunk = df_MSA['text'][0:50]
chunk_string = " ".join(chunk.astype(str))
response = generate_response(chunk_string)
response

df_output = pd.DataFrame()
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__egyptain_dialect_output.csv'
df_output.to_csv(output_file_path, index=False)
print(f"CSV file saved to: {output_file_path}")

import pandas as pd
import os
import time
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Function to split response by newline or numbered prefix
def split_response(response):
    # Split by numbered prefix or newline
    return [sent.strip() for sent in response.splitlines() if sent.strip()]

# Define your Google Drive CSV file path
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__egyptain_dialect_output.csv'


# Process in chunks of 50 and append results to CSV
for i in range(0, len(df_MSA), 50):
    # Sleep for rate-limiting purposes
    if i % 3 == 0:
        time.sleep(30)

    # Get chunk of 50 sentences
    chunk = df_MSA['text'][i:i+50]
    chunk_string = " ".join(chunk.astype(str))  # Convert to a single string

    # Generate the response
    response = generate_response(chunk_string)

    # Split the response into individual lines (by newline or numbered prefix)
    response_list = split_response(response)

    # Convert to DataFrame for CSV storage
    df_results = pd.DataFrame(response_list, columns=['Khaleeji'])

    # Write to CSV
    if i == 0:
        df_results.to_csv(output_file_path, mode='w', index=False)  # Write with header
    else:
        df_results.to_csv(output_file_path, mode='a', index=False, header=False)  # Append without header

    print(f"Processed chunk {i} to {i+50}")

print(f"All data has been processed and saved to {output_file_path}.")

"""# **Khaleji Dialect Generation**"""

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the ChatOpenAI model with your API key
llm = ChatOpenAI(model="gpt-4o", openai_api_key="")

def generate_response(sentences):
    # Define the prompt template for the MSA to multiple Arabic dialects translation
    # Removed placeholders for dialect outputs as they will be generated by the LLM
    template = """
تصرّف كمترجم من اللغة العربية الفصحى الحديثة إلى اللهجه الخليجيه  جدًا كما يتحدث بها الناس في حياتهم اليومية.أجب فقط بالشكل المطلوب دون إضافة كلمات إضافية.
    ملاحظة: كل جملة بالعربية الفصحى مرقمة، أعد الجملة المترجمة إلى اللهجة الخليجيه بنفس الترقيم، لا تضف أو تحذف أي شيء و اضف سطر جديد بعد كل جمله و الاخرى.
    الجمل بالعربية الفصحى:
    {arabic_sentences}
    اللهجة الخليجيه :

"""

    # Create a prompt template object using LangChain
    prompt_template = PromptTemplate(
        input_variables=["arabic_sentences"],
        template=template
    )

    # Format the prompt by inserting the MSA sentences
    formatted_prompt = prompt_template.format(
        arabic_sentences=sentences
    )

    # Send the prompt to the OpenAI model and get the response
    result = llm([HumanMessage(content=formatted_prompt)])

    # Process the response and extract the three dialect outputs separately
    response = result.content
    return response


# Example usage with multiple samples
chunk = df_MSA['text'][0:50]
chunk_string = " ".join(chunk.astype(str))
response = generate_response(chunk_string)
response

df_output = pd.DataFrame()
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__khaleji_dialect_output.csv'
df_output.to_csv(output_file_path, index=False)
print(f"CSV file saved to: {output_file_path}")

df_MSA_1500_SAMPLES= df_MSA.head(1500)
df_MSA_1500_SAMPLES.tail()

import pandas as pd
import os
import time
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Function to split response by newline or numbered prefix
def split_response(response):
    # Split by numbered prefix or newline
    return [sent.strip() for sent in response.splitlines() if sent.strip()]

# Define your Google Drive CSV file path
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__khaleji_dialect_output.csv'


# Process in chunks of 50 and append results to CSV
for i in range(0, len(df_MSA_1500_SAMPLES), 50):
    # Sleep for rate-limiting purposes
    if i % 3 == 0:
        time.sleep(30)

    # Get chunk of 50 sentences
    chunk = df_MSA_1500_SAMPLES['text'][i:i+50]
    chunk_string = " ".join(chunk.astype(str))  # Convert to a single string

    # Generate the response
    response = generate_response(chunk_string)

    # Split the response into individual lines (by newline or numbered prefix)
    response_list = split_response(response)

    # Convert to DataFrame for CSV storage
    df_results = pd.DataFrame(response_list, columns=['Khaleeji'])

    # Write to CSV
    if i == 0:
        df_results.to_csv(output_file_path, mode='w', index=False)  # Write with header
    else:
        df_results.to_csv(output_file_path, mode='a', index=False, header=False)  # Append without header

    print(f"Processed chunk {i} to {i+50}")

print(f"All data has been processed and saved to {output_file_path}.")



"""# **Khaleji saudi arabia Dialect Generation**"""

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the ChatOpenAI model with your API key
llm = ChatOpenAI(model="gpt-4o", openai_api_key="")

def generate_response(sentences):
    # Define the prompt template for the MSA to multiple Arabic dialects translation
    # Removed placeholders for dialect outputs as they will be generated by the LLM
    template = """
تصرّف كمترجم من اللغة العربية الفصحى الحديثة إلى اللهجه السعوديه العاميه جدًا كما يتحدث بها الناس في حياتهم اليومية.أجب فقط بالشكل المطلوب دون إضافة كلمات إضافية.
    ملاحظة: كل جملة بالعربية الفصحى مرقمة، أعد الجملة المترجمة إلى اللهجة السعوديه بنفس الترقيم، لا تضف أو تحذف أي شيء و اضف سطر جديد بعد كل جمله و الاخرى.
    الجمل بالعربية الفصحى:
    {arabic_sentences}
     اللهجة السعوديه:

"""

    # Create a prompt template object using LangChain
    prompt_template = PromptTemplate(
        input_variables=["arabic_sentences"],
        template=template
    )

    # Format the prompt by inserting the MSA sentences
    formatted_prompt = prompt_template.format(
        arabic_sentences=sentences
    )

    # Send the prompt to the OpenAI model and get the response
    result = llm([HumanMessage(content=formatted_prompt)])

    # Process the response and extract the three dialect outputs separately
    response = result.content
    return response


# Example usage with multiple samples
chunk = df_MSA['text'][0:50]
chunk_string = " ".join(chunk.astype(str))
response = generate_response(chunk_string)
response

df_output = pd.DataFrame()
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__khaleji_saudi_arabia_dialect_output.csv'
df_output.to_csv(output_file_path, index=False)
print(f"CSV file saved to: {output_file_path}")

import pandas as pd
import os
import time
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Function to split response by newline or numbered prefix
def split_response(response):
    # Split by numbered prefix or newline
    return [sent.strip() for sent in response.splitlines() if sent.strip()]

# Define your Google Drive CSV file path
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__khaleji_saudi_arabia_dialect_output.csv'


# Process in chunks of 50 and append results to CSV
for i in range(0, len(df_MSA_1500_SAMPLES), 50):
    # Sleep for rate-limiting purposes
    if i % 3 == 0:
        time.sleep(30)

    # Get chunk of 50 sentences
    chunk = df_MSA_1500_SAMPLES['text'][i:i+50]
    chunk_string = " ".join(chunk.astype(str))  # Convert to a single string

    # Generate the response
    response = generate_response(chunk_string)

    # Split the response into individual lines (by newline or numbered prefix)
    response_list = split_response(response)

    # Convert to DataFrame for CSV storage
    df_results = pd.DataFrame(response_list, columns=['Khaleeji'])

    # Write to CSV
    if i == 0:
        df_results.to_csv(output_file_path, mode='w', index=False)  # Write with header
    else:
        df_results.to_csv(output_file_path, mode='a', index=False, header=False)  # Append without header

    print(f"Processed chunk {i} to {i+50}")

print(f"All data has been processed and saved to {output_file_path}.")

"""# **Morrocon Dialect Generation**"""

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the ChatOpenAI model with your API key
llm = ChatOpenAI(model="gpt-4o", openai_api_key="")

def generate_response(sentences):
    # Define the prompt template for the MSA to multiple Arabic dialects translation
    # Removed placeholders for dialect outputs as they will be generated by the LLM
    template = """
تصرّف كمترجم من اللغة العربية الفصحى الحديثة إلى اللهجه المغربيه العامية جدًا كما يتحدث بها الناس في حياتهم اليومية.أجب فقط بالشكل المطلوب دون إضافة كلمات إضافية.
     و ملاحظة: كل جملة بالعربية الفصحى مرقمة، أعد الجملة المترجمة إلى اللهجة المغربيه بنفس الترقيم، لا تضف أو تحذف أي شيء و اضف سطر جديد بعد كل جمله و الاخرى.
    الجمل بالعربية الفصحى:
    {arabic_sentences}
    اللهجة المغربيه العاميه :

"""

    # Create a prompt template object using LangChain
    prompt_template = PromptTemplate(
        input_variables=["arabic_sentences"],
        template=template
    )

    # Format the prompt by inserting the MSA sentences
    formatted_prompt = prompt_template.format(
        arabic_sentences=sentences
    )

    # Send the prompt to the OpenAI model and get the response
    result = llm([HumanMessage(content=formatted_prompt)])

    # Process the response and extract the three dialect outputs separately
    response = result.content
    return response


# Example usage with multiple samples
chunk = df_MSA['text'][0:50]
chunk_string = " ".join(chunk.astype(str))
response = generate_response(chunk_string)
response

df_output = pd.DataFrame()
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__morrocon_dialect_output.csv'
df_output.to_csv(output_file_path, index=False)
print(f"CSV file saved to: {output_file_path}")

import pandas as pd
import os
import time
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Function to split response by newline or numbered prefix
def split_response(response):
    # Split by numbered prefix or newline
    return [sent.strip() for sent in response.splitlines() if sent.strip()]

# Define your Google Drive CSV file path
output_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__morrocon_dialect_output.csv'


# Process in chunks of 50 and append results to CSV
for i in range(0, len(df_MSA_1500_SAMPLES), 50):
    # Sleep for rate-limiting purposes
    if i % 3 == 0:
        time.sleep(30)

    # Get chunk of 50 sentences
    chunk = df_MSA_1500_SAMPLES['text'][i:i+50]
    chunk_string = " ".join(chunk.astype(str))  # Convert to a single string

    # Generate the response
    response = generate_response(chunk_string)

    # Split the response into individual lines (by newline or numbered prefix)
    response_list = split_response(response)

    # Convert to DataFrame for CSV storage
    df_results = pd.DataFrame(response_list, columns=['Morrocon'])

    # Write to CSV
    if i == 0:
        df_results.to_csv(output_file_path, mode='w', index=False)  # Write with header
    else:
        df_results.to_csv(output_file_path, mode='a', index=False, header=False)  # Append without header

    print(f"Processed chunk {i} to {i+50}")

print(f"All data has been processed and saved to {output_file_path}.")

"""# **Data Preproccesing**"""

import re
# Function to remove digits and dashes from data frame
def preprocess_text(text):
    # Remove digits and dashes
    cleaned_text = re.sub(r'\d+-', '', text)
    return cleaned_text

khaleji_df = pd.read_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/khaleji_dialect_before cleaning.csv')
morrocon_df = pd.read_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/morrocon_dialect _before cleaning.csv')
egyptian_df = pd.read_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/egyptain_dialect_before cleaning.csv')

df_khaleji_saudi_arabia = pd.read_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects Generation before Cleaning and Processing/arabic__khaleji_saudi_arabia_dialect_output.csv')
df_khaleji_saudi_arabia.head()

#check shape
df_khaleji_saudi_arabia.shape

df_khaleji_saudi_arabia.head(10)

df_khaleji_saudi_arabia['Khaleeji'] = df_khaleji_saudi_arabia['Khaleeji'].astype(str).apply(preprocess_text)
df_khaleji_saudi_arabia.head(10)

df_khaleji_saudi_arabia.tail(10)

#apply preprocess text to morrocon and egyptain
morrocon_df['Morrocon'] = morrocon_df['Morrocon'].astype(str).apply(preprocess_text)
egyptian_df['Egyptian'] = egyptian_df['Egyptian'].astype(str).apply(preprocess_text)

#search for and count digits in this data frame
egyptian_df[egyptian_df['Egyptian'].str.contains(r'\d')]


morrocon_df.to_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects data after Cleaning/morrocon_dialect_after_cleaning.csv', index=False)


df_khaleji_saudi_arabia.to_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects data after Cleaning/khaleji_saudi_arabia_dialect_after_cleaning.csv', index=False)

"""# **Most repeated words**"""

import pandas as pd
from collections import Counter
import re

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Define stop words for Arabic language
arabic_stop_words = set(stopwords.words('arabic'))

# You can access and use the stop words like this:
print(arabic_stop_words)

#remove stop words from the three data frames afetr creating a copy from them

# Create copies of the dataframes
khaleji_df_copy = khaleji_df.copy()
morrocon_df_copy = morrocon_df.copy()
egyptian_df_copy = egyptian_df.copy()

# Function to remove stop words from a column
def remove_stop_words(text):
  if isinstance(text, str):
    words = text.split()
    filtered_words = [word for word in words if word not in arabic_stop_words]
    return " ".join(filtered_words)
  else:
    return text

# Apply the function to remove stop words from the relevant columns
khaleji_df_copy['Khaleeji'] = khaleji_df_copy['Khaleeji'].apply(remove_stop_words)
morrocon_df_copy['Morrocon'] = morrocon_df_copy['Morrocon'].apply(remove_stop_words)
egyptian_df_copy['Egyptian'] = egyptian_df_copy['Egyptian'].apply(remove_stop_words)

# Function to clean and split the text into words
def clean_text(text):
    # Remove non-alphabetic characters and split into words
    cleaned_text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = cleaned_text.split()
    return words

# Function to extract the most repeated words and their counts from a DataFrame
def most_repeated_words(df, num_words=5, dialect='text'):
    all_words = []

    # Iterate over each text in the DataFrame and clean it
    for text in df[dialect]:
        words = clean_text(text)
        all_words.extend(words)

    # Use Counter to count word frequencies
    word_counts = Counter(all_words)

    # Get the most common words
    most_common_words = word_counts.most_common(num_words)

    return most_common_words

# Extract the most repeated words for each DataFrame
khaleeji_common = most_repeated_words(khaleji_df_copy,50,'Khaleeji')
morrocon_common = most_repeated_words(morrocon_df_copy, 30, 'Morrocon')
egyptian_common = most_repeated_words(egyptian_df_copy, 50, 'Egyptian')

# Print the results
print("Most repeated words in Khaleeji DataFrame:", khaleeji_common)
print("Most repeated words in Morrocon DataFrame:", morrocon_common)
print("Most repeated words in Egyptian DataFrame:", egyptian_common)

"""### **Replace Egyptain Words**"""

""" Egyptain :
 "بيقفز" to "بينط"
"العشب" : "الزرع"
"الشاطئ" : "الشط"
"الثلج": "التلج"
  "فمه": "بقه"
"بيعبر" : بيعدي"
"عبر ": "على "
"حديقة" : "جنينه"
"ملابس" : "لبس"
 """
 # Dictionary of words to replace (Egyptian dialect changes)
replace_dict = {
    "بيقفز": "بينط",
    "العشب": "الزرع",
    "الشاطئ": "الشط",
    "الثلج": "التلج",
    "فمه": "بقه",
    "بيعبر": "بيعدي",
    "عبر": "على",
    "حديقة": "جنينه",
    "ملابس": "لبس"
}

# Function to replace specific words in the Egyptian DataFrame
def replace_words_in_text(text, replace_dict):
    for word, replacement in replace_dict.items():
        text = text.replace(word, replacement)
    return text

# Create a copy of the original Egyptian DataFrame
egyptian_df_copy = egyptian_df.copy()

# Apply the replacement function to the 'Egyptian' column in the DataFrame
egyptian_df_copy['Egyptian'] = egyptian_df_copy['Egyptian'].apply(lambda x: replace_words_in_text(x, replace_dict))

# Display the updated DataFrame
print(egyptian_df_copy.head())

egyptian_df_copy.shape

# Create a new DataFrame that only contains rows where the text has been changed
changed_rows_df = egyptian_df_copy[egyptian_df_copy['Egyptian'] != egyptian_df['Egyptian']]

# Display the new DataFrame with the changed rows
print(changed_rows_df.head())

changed_rows_df.shape

#create csv file that has the changed row after and before

# Create a new DataFrame with 'before' and 'after' columns
comparison_df = pd.DataFrame({
    'before': egyptian_df['Egyptian'],  # Original text
    'after': egyptian_df_copy['Egyptian']  # Changed text
})

# Filter out rows where 'before' and 'after' are the same
comparison_df = comparison_df[comparison_df['before'] != comparison_df['after']]

# Specify the path for your CSV file
csv_file_path = '/content/drive/MyDrive/Final V Project 283/project Draft/changed_rows_Egyptain.csv'

# Save the comparison DataFrame to CSV
comparison_df.to_csv(csv_file_path, index=False)

print(f"CSV file with changed rows saved to: {csv_file_path}")

# Save egyptian_df_copy to a CSV file in Google Drive
egyptian_df_copy.to_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects data after Cleaning/cleaned_egyptain_dialect_data.csv', index=False)

"""### **Replace Khaleji Words**"""

# Updated dictionary of words to replace (Khaleeji dialect changes)
replace_dict_khaleeji = {
    "بنت": "صبيانة",
    "طفل": "يّهال",
    "الشاطئ": "السيف",  # Updated from "الشاطئ" to "السيف"
    "كرة": "طابه",  # Added new replacement for "كرة"
    "قدام": "چدام",  # Added new replacement for "قدام"
    "يمشي": "يسير",
    "قميص": "ثوب",
    "حرمة": "مرة",
    "واقف": "قائم",
    "مجموعة": "ربعة",
    "يلعبون": "يلعبونّه",
    "أسود": "كحلي"  # Added new replacement for "أسود"
}

# Function to replace specific words in the Khaleeji DataFrame
def replace_words_in_text(text, replace_dict):
    for word, replacement in replace_dict.items():
        text = text.replace(word, replacement)
    return text

# Create a copy of the original Khaleeji DataFrame
khaleeji_df_copy = khaleji_df.copy()

# Apply the replacement function to the 'Khaleeji' column in the DataFrame
khaleeji_df_copy['Khaleeji'] = khaleeji_df_copy['Khaleeji'].apply(lambda x: replace_words_in_text(x, replace_dict_khaleeji))

# Display the updated DataFrame
print(khaleeji_df_copy.head())

khaleeji_df_copy.shape

# Create a new DataFrame that only contains rows where the text has been changed
changed_rows_df = khaleeji_df_copy[khaleeji_df_copy['Khaleeji'] != khaleji_df['Khaleeji']]

# Display the new DataFrame with the changed rows
print(changed_rows_df.head())

changed_rows_df.shape

#create csv file that has the changed row after and before

# Create a new DataFrame with 'before' and 'after' columns for Khaleeji
comparison_df_khaleeji = pd.DataFrame({
    'before': khaleji_df['Khaleeji'],  # Original text
    'after': khaleeji_df_copy['Khaleeji']  # Changed text
})

# Filter out rows where 'before' and 'after' are the same
comparison_df_khaleeji = comparison_df_khaleeji[comparison_df_khaleeji['before'] != comparison_df_khaleeji['after']]

# Specify the path for your CSV file for Khaleeji
csv_file_path_khaleeji = '/content/drive/MyDrive/Final V Project 283/project Draft/changed_rows_Khaleeji.csv'

# Save the comparison DataFrame to CSV for Khaleeji
comparison_df_khaleeji.to_csv(csv_file_path_khaleeji, index=False)

print(f"CSV file with changed rows saved to: {csv_file_path_khaleeji}")

# Save khaleeji_df_copy to a CSV file in Google Drive
khaleeji_df_copy.to_csv('/content/drive/MyDrive/Final V Project 283/project Draft/Dialects data after Cleaning/cleaned_khaleeji_dialect_data.csv', index=False)



