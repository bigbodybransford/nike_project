from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Shoes #my app's model/table
from apscheduler.schedulers.background import BackgroundScheduler

url = 'https://www.nike.com/launch?s=upcoming'
scheduler = BackgroundScheduler()

def 