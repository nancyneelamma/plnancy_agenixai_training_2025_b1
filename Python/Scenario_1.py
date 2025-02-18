#Importing necessary libraries

import psycopg2
import requests
import json

#Creating a class

class WeatherData:

    #Initializing the constructor
    
    def __init__(self,api_key,api_url,db_config):

        self.api_key=api_key
        self.api_url=api_url 
        self.db_config=db_config

    #Connecting to the database
        
    def database_connect(self):
        
        try:
            conn = psycopg2.connect(
                host=self.db_config["host"],
                database=self.db_config["database"],
                user=self.db_config["user"],   
                password=self.db_config["password"]
            )
            print("Connection Established")
            return conn
        
        except Exception as e:
            print("Error:",e)
            
    # Fetching the data requesting the name of the city
    
    def get_data(self,city):
    
        params={"access_key":self.api_key,"query":city}
        response=requests.get(self.api_url,params=params)
    
        if response.status_code==200:
            return response.json()
        else:
            print(f"No data found for the {city}")

    # Insering the data into the database
    def insert_data(self,conn,data):

        if not data:
            print("No data to insert")

        cursor = conn.cursor()

        city_name = data['location']['name']
        country = data['location']['country']
        temperature = data['current']['temperature']
        humidity = data['current']['humidity']
        wind_direction = data['current']['wind_dir']
        visibility = data['current']['visibility']
        latitude = data['location']['lat']
        longitude = data['location']['lon']

        query= "INSERT INTO weather_data(city_name,country,temperature,humidity,wind_direction,visibility,latitude,longitude) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.execute(query,(city_name,country,temperature,humidity,wind_direction,visibility,latitude,longitude))

        conn.commit()
    
        print("Weather Data has been successfully inserted")

    #Taking input from the user, fetching the data from the api, connecting to database, inserting the weather data to the database
    def main(self):

        city=input("Enter the name of the city:")
        data=self.get_data(city)
        if data:
            conn=self.database_connect()
            self.insert_data(conn,data)
            conn.close()

#Main Code
            
if __name__ == "__main__":

    api_key="8764147c03a8311835f0f1ce50d484ac" #API Token
    
    api_url="https://api.weatherstack.com/current" #Base URL 

    #Database Connection Details
    
    db_config = {
        'host':"localhost",  
        'database':"scenario1_db",
        'user':"postgres",   
        'password':"newpassword"
    }
    
    output=WeatherData(api_key,api_url,db_config)

    output.main()

