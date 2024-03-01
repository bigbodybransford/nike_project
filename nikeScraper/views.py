from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Shoes #my app's model/table
from apscheduler.schedulers.background import BackgroundScheduler

url = "https://www.nike.com/launch?s=in-stock"
scheduler = BackgroundScheduler()

def index(request):
 return HttpResponse("Hello!!!")

# def listShoesPageView(request):
#  shoes_in_database = Shoes.objects.all()
#  context = {'shoes': shoes_in_database}
#  return render(request, 'nikeScraper/listshoes.html', context)
 # return HttpResponse(Shoes.objects.all())

# loops through html elements and appends href links for each page/shoe to href_list 
def get_shoe_links(request):
 driver = webdriver.Chrome()
 driver.get(url)
 soup = BeautifulSoup(driver.page_source, 'html.parser')
 shoe_links = driver.find_elements(By.CSS_SELECTOR, "a.card-link.d-sm-b")
 href_list = []
 for link in shoe_links:
  href_link = link.get_attribute('href')
  if href_link not in href_list:
   href_list.append(href_link)

 driver.quit()
 # return JsonResponse({'shoe_links': href_list})
 return href_list

def get_shoe_details(request):
 href_list = get_shoe_links(request)
 driver = webdriver.Chrome()
 shoe_list = []
 for page in href_list:
   categories = []
   names = []
   prices = []
   descriptions = []
   driver.get(page)
   soup = BeautifulSoup(driver.page_source, 'html.parser')
   # noticed that there are class names that differ. im missing some pieces and will
   # need to update these at some point. category_alt? check names too
   category = driver.find_elements(By.CSS_SELECTOR, "h1.headline-5\\=small")
   name_boi = driver.find_elements(By.CSS_SELECTOR, "h2.headline-2")
   price_boi = driver.find_elements(By.CSS_SELECTOR, "div.headline-5.pb6-sm")
   # descriptions contain the SKU number at the very end. i should extract this,
   # save it to a variable, and add it as its own field in the db
   description_boi = driver.find_elements(By.CSS_SELECTOR, "div.description-text.text-color-grey.mb9-sm.ta-sm-c")
   #refactor from here with min_length. for i in range(min_length). throw code under this and comment out descriptions
   for cat in category:
    category_actual = cat.text
    categories.append(category_actual)
   for name in name_boi:
    name_actual = name.text
    names.append(name_actual)
   for price in price_boi:
    price_actual = price.text
    prices.append(price_actual)
   for desc in description_boi:
    try:
     p_element = desc.find_element(By.TAG_NAME, "p")
     description_actual = p_element.text
     # print(descriptions)
    except Exception:
     description_actual = "N/A"
    descriptions.append(description_actual)
   min_length = min(len(categories), len(names), len(prices))
   # print('Weve reached line 51')
   try:
    for i in range(min_length):
     print('weve reached line 54')
     cleaned_price = price_boi[i].text.strip('$').replace(',', '')
     if cleaned_price == 'Price unavailable':
      price_value = -1
     else:
      print('weve reached the else block')
      float_price = float(cleaned_price)
      print(float_price)
      rounded_price = round(float_price, 2)
      price_value = rounded_price
     shoe = Shoes(
      category=categories[i],
      name=names[i],
      price=price_value,
      description=descriptions[i]
     )
     shoe.save()
   except Exception as e:
    print(e)
 return HttpResponse("Done!")

def get_shoe(request, category):
  all_shoe_results = Shoes.objects.filter(category__contains=category.title())
  print(all_shoe_results)
  return HttpResponse(all_shoe_results)