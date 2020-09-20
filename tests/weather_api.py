import unittest,platform,os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from jsonpath_ng import jsonpath, parse

class WeatherApiTest(unittest.TestCase):
    
    def setUp(self):
        print("--------test started----------")
        self.ApiUrl="https://api.openweathermap.org/data/2.5/weather"
        self.ApiKey="7fe67bf08c80ded756e598d6f8fedaea"
        base_os = platform.platform().lower()
        if(base_os.__contains__("mac")):
            executable = os.path.join(os.path.dirname(os.path.dirname(__file__)),"tests","executables","Mac","geckodriver")
            self.driver = webdriver.Firefox(executable_path=executable)
        elif(base_os.__contains__("linux")):
            executable = os.path.join(os.path.dirname(os.path.dirname(__file__)),"tests","executables","Linux","geckodriver")
            self.driver = webdriver.Firefox(executable_path=executable)
        elif(base_os.__contains__("Windows")):
            executable = os.path.join(os.path.dirname(os.path.dirname(__file__)),"tests","executables","Windows","geckodriver.exe")
            self.driver = webdriver.Firefox(executable_path=executable)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver,30)
    def test_01_weather_details_from_website_by_city_name(self):
        driver = self.driver
        wait = self.wait
        print ("Beginning Weather WEB test")
        driver.get("https://weather.com")  
        wait.until(element_to_be_clickable((By.ID,"LocationSearch_input")))
        driver.find_element(By.ID,"LocationSearch_input").send_keys("Delhi"+Keys.RETURN)
        wait.until(element_to_be_clickable((By.XPATH,"//button[text()='Delhi']")))
        driver.find_element(By.XPATH,"//button[text()='Delhi']").click()
        WeatherApiTest.tempW = driver.find_element(By.XPATH,"(//h1[contains(.,'Delhi')]/parent::*/following-sibling::*//span[@data-testid='TemperatureValue'])[1]").text
        WeatherApiTest.tempW = WeatherApiTest.tempW[0:(len(WeatherApiTest.tempW)-1)]
        print("temperature from web:"+WeatherApiTest.tempW)
    def test_02_weather_details_from_api_by_city_name(self):
        print ("Beginning Weather API test")
        testUrl = (self.ApiUrl+"?q=Delhi,in"+"&APPID="+self.ApiKey+"&units=metric")
        print (testUrl)
        response = requests.get(testUrl)
        
        json_response = response.json()
        print(json_response)
        print ("------------------------------")
        
        print ("The temperature from API is :-" )
        print (json_response["main"]["temp"])
        WeatherApiTest.tempA = json_response["main"]["temp"]
    def test_03_comparator(self):
        print("Comparing tempA="+  (str(WeatherApiTest.tempA))+" and tempW="+WeatherApiTest.tempW)
        tolerance = 3.0
        if((float(WeatherApiTest.tempW))==(float(WeatherApiTest.tempA))):
            print("Two Weather values match exactly")
        else:
            diff = abs((float(WeatherApiTest.tempW))-(float(WeatherApiTest.tempA)))
            if(diff<tolerance):
                print(" Two values match within the expected tolerance range")
            else:
                print("Values do not match, expected tolerance range="+str(tolerance)+", difference="+str(diff))
                raise AssertionError

        
    def tearDown(self):
        self.driver.quit()
        print ("--------test finished---------")
        
if __name__ == "__main__":
    unittest.main()