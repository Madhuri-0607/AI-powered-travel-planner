# AI-powered-travel-planner
An AI-powered travel planner that personalizes itineraries based on user preferences, optimizes routes, suggests attractions, and provides real-time recommendations for a seamless and smart travel experience.  

AI Travel Itinerary Planner  
A web-based application that generates personalized travel itineraries for various cities, including weather information, local cuisine, landmarks, restaurants, and attractions tailored to user preferences, budget, and interests.  

Features  
Personalized Itineraries: Generate daily travel plans for 1–30 days based on destination, budget, and interests (e.g., Food, Adventure, Culture, Nature, Shopping).  
Weather Integration: Fetch real-time weather data for the destination using OpenWeatherMap API.  
Local Cuisine & Restaurants: Suggest famous local foods and restaurants based on budget (Economy, Standard, Luxury) using Spoonacular API.  
Landmarks & Attractions: Recommend iconic landmarks and attractions tailored to user interests using Geoapify API.  
City Information: Provide a brief description and image of the destination via Wikipedia API.  
Interactive Frontend: Built with Streamlit for a user-friendly interface to input preferences and view itineraries.  
Predefined City Database: Includes popular cities (e.g., Paris, New York, Tokyo, Delhi, Mumbai, Bangalore) with famous landmarks and foods.  

Tech Stack  
Backend: Python, Flask, Flask-CORS  
Frontend: Streamlit  
APIs:  
OpenWeatherMap (Weather)  
Spoonacular (Restaurants)  
Geoapify (Places/Attractions)    
Wikipedia (City Information)  
Dependencies: Requests, PIL (Python Imaging Library)  
Environment: Python 3.12.4, Jupyter Notebook  

Installation  
1.Clone the Repository  

git clone <repository-url>  
cd ai-travel-itinerary-planner  

2.Set Up a Virtual Environment (recommended):  
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  

3.Install Dependencies  
pip install flask flask_cors requests streamlit  

4.Obtain API Keys:  
Sign up for API keys from:  
OpenWeatherMap    
Spoonacular  
Geoapify  

Replace the placeholder API keys in travel_itinerary1.py with your own:  
OPENWEATHER_API_KEY = "your_openweather_api_key"  
SPOONACULAR_API_KEY = "your_spoonacular_api_key"  
GEOAPIFY_API_KEY = "your_geoapify_api_key"  

Usage  
1.Run the Backend (Flask Server):  
python travel_itinerary1.py  

2.The Flask server will start at http://127.0.0.1:5000.     
Run the Frontend (Streamlit): Open a new terminal, activate the virtual environment, and run  
streamlit run travel_frontend.py  

3.Interact with the App:  
Enter a destination or select from popular cities (e.g., Paris, Delhi, Tokyo).  
Choose trip duration, start date, budget, and interests.  
Click "Generate Itinerary" to view a detailed plan with daily activities, weather, local foods, landmarks, restaurants, and attractions  

API Keys   
The application relies on the following APIs. Ensure you have valid keys and update them in travel_itinerary1.py:    

OpenWeatherMap: For weather data.   
Spoonacular: For restaurant recommendations.  
Geoapify: For attractions and places of interest.  
Wikipedia: No API key required for basic summary and image retrieval.  
Note: The provided API keys in the notebook are placeholders and may not work. Obtain your own keys to avoid rate limits or errors  

File Structure:  
ai-travel-itinerary-planner/  
│
├── aitravel.ipynb          # Jupyter Notebook with code and setup  
├── travel_itinerary1.py    # Flask backend for API logic  
├── travel_frontend.py      # Streamlit frontend for user interface  
└── README.md               # Project documentation  

aitravel.ipynb: Contains the setup, dependency installation, backend, and frontend code in a Jupyter Notebook format.  
travel_itinerary1.py: Flask application handling itinerary generation, API integrations, and city data.  
travel_frontend.py: Streamlit application for the interactive user interface.  



