Code for a website that scrapes the websites of popular sneaker brands for upcoming drops, and uses a model fitted to past resell data to predict what the shoe will resell for after being sold out.

This is intended to be both an attempt at analysis of shoe prices and resell data, which I hope to improve by finding a larger dataset or getting access to official StockX APIs to create one, and for new resellers to get into reselling by showing them the shoes they can make the most profit on. I'm hoping to make improvements to these predictions as well as possibly get data from other places, including data of shoes currently on resale websites that can be predicted to go up or down in price. 

Made using a variety of cross-validated regressor models for prediction, selenium scrapers, and some simple Flaks and Express for the api and app respectively.

Site link: https://shoe-price-app.onrender.com

API link (Daily updated JSON of scraped data and predictions on prices): https://shoe-price-api.onrender.com/data
