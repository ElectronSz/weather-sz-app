import typer
from prettytable import PrettyTable
import requests
import json
import time
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(verbose=True)
env_path = Path('.') / '.env'

appid= os.getenv("APP_ID")


def main(city: str, units: str = typer.Option(...)):
    if city == "root":
        typer.echo("The root user is reserved")
        raise typer.Exit(code=1)
    else:
        getWaether(city, units)
    
def getWaether(city: str, units = "metric"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={appid}"

    response = requests.get(url)

    if(response.ok):
        
        data = json.loads(response.content)
        tb = PrettyTable()
        tb.field_names = ["City name", "Feels Like", "Temp Min", "Temp Max","Weather", "Humidity","Wind Speed", "Sunset", "Sunrise"]
        tb.add_row([ data["name"]+","+data["sys"]["country"],data["main"]["feels_like"],
                    data["main"]["temp_min"], data["main"]["temp_max"],
                    data["weather"][0]["description"], data["main"]["humidity"],
                    data["wind"]["speed"], time.strftime('%H:%M:%S', time.localtime(data["sys"]["sunset"])),
                    time.strftime('%H:%M:%S', time.localtime(data["sys"]["sunrise"]))])
        print(tb)
        
        
    else:
        response.raise_for_status()
    
   
if __name__ == "__main__":
    typer.run(main)
    

