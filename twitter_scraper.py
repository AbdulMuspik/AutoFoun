from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set the path for the webdriver (update if necessary)
webdriver_path = '/Users/abdulmuspik/Downloads/chromedriver-mac-arm64/chromedriver'

# Initialize the Chrome webdriver with Service class
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service)

# Open Twitter trending page
driver.get("https://twitter.com/explore")

# Define the number of hashtags to scrape
num_hashtags = 5 

try:
  # Wait for the trending section to load dynamically
  wait = WebDriverWait(driver, 10)  # Wait for 10 seconds
  wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1dbjc4n")))  # Wait for specific element

  # Define the XPath template (avoid hardcoding specific positions)
  xpath_template = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[{}]/div/div/div/div[2]/div[2]/div[2]/span/a'

  # Scraping hashtags
  hashtags = []
  for i in range(1, num_hashtags + 1):  # Loop for desired number of hashtags
      try:
          # Use formatted XPath for each hashtag element
          xpath = xpath_template.format(i)
          trending_topic = driver.find_element(By.XPATH, xpath)
          hashtags.append(trending_topic.text)
      except Exception as e:
          print(f"Error on hashtag {i}: {e}")

  # Creating URLs for the hashtags
  urls = [f"https://twitter.com/hashtag/{tag.replace('#', '')}" for tag in hashtags]

  # Creating a DataFrame
  data = {'Hashtag': hashtags, 'URL': urls}
  df = pd.DataFrame(data)

  # Saving the DataFrame to a CSV file
  df.to_csv('Twitter_hashtags.csv', index=False)

finally:
  # Close the browser regardless of exceptions
  driver.quit()
  
print("Hashtags scraped successfully!")