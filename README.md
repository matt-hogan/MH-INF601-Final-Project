# Final Project
#### INF601 - Advanced Programming in Python  
#### Matt Hogan  
  
## Description  
This is a website built with Django to compare sports bettings odds from different sports books. The data is retrieved from https://the-odds-api.com/. Currently, odds for the NFL, NBA, NCAAF, and NCAAB are able to be compared. The sportsbooks supported are DraftKings, Fanduel, Pointsbet, BetMGM, and Barstool. There is also a feature to track your bets placed and see your profit.  
## Running the App  
1. Clone or download repository  
2. Create and activate a virtual environment  
```
python -m venv .venv  
.\.venv\Scripts\activate.bat
```  
3. Install necessary packages  
```
pip install -r requirements.txt
```
4. Navigate to https://the-odds-api.com/ and get an API key  
5. In `sport_bet_site` folder, create `.env` file. Add your API from the step above to this file  
```
API_KEY=your-api-key
```  
5. Initialize the databases  
```
python manage.py makemigrations odds
python manage.py makemigrations users
python manage.py makemigrations tracker
```
6. Apply the database changes  
```
python manage.py migrate
```
7. Add initial values to the databases  
```
python manage.py loaddata sports.json
python manage.py loaddata bookmakers.json
```
8. Create an admin user  
```
python manage.py createsuperuser
```
9. Run the django app  
```
python manage.py runserver
```
10. Navigate to `http://127.0.0.1:8000/` in a browser