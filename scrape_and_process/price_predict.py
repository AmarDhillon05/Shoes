from scrape_and_process import scrapers
import joblib
import pandas as pd
import string
import os

highest_bid_predictor = joblib.load('model/highest_bid_predictor.pkl')
lowest_ask_predictor = joblib.load('model/lowest_ask_predictor.pkl')
brand_le = joblib.load('model/brand_le.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')


'''
columns_for_highest_bid = ['retail', 'highestBid', 'brand'] + item_cols
columns_for_lowest_ask = ['retail', 'lowestAsk', 'brand', 'days_since_release', 'volatility', 'numberOfBids'] + item_cols
'''


#Using models on dictionaries

def predict_highest_bid(shoe_dict):
    input_dict = {'retail' : [shoe_dict['price']],
                  'brand' : [brand_le.transform([shoe_dict['brand'].lower()])[0]]}
    vects = vectorizer.transform([shoe_dict['name'].lower().replace("\n", "").translate(str.maketrans('', '', string.punctuation))]).toarray()[0]
    for idx in range(vects.shape[0]):
        input_dict[f"item_{idx}"] = [vects[idx]]
    pred = highest_bid_predictor.predict(pd.DataFrame(input_dict))[0]
    return pred

def predict_lowest_ask(shoe_dict, days_since_release):
    input_dict = {'retail' : [shoe_dict['price']],
                  'brand' : [brand_le.transform([shoe_dict['brand'].lower()])[0]],
                  'days_since_release' : [days_since_release],
                  'highestBid' : [shoe_dict['predicted_prices']]}
    vects = vectorizer.transform([shoe_dict['name'].lower().replace("\n", "").translate(str.maketrans('', '', string.punctuation))]).toarray()[0]
    for idx in range(vects.shape[0]):
        input_dict[f"item_{idx}"] = [vects[idx]]
    pred = highest_bid_predictor.predict(pd.DataFrame(input_dict))[0]
    return pred
    


#Predicting highest bids/what the price will rise to after dropping and which shoes will be most profitable

def get_sorted_drops():
    all_shoes = scrapers.get_adidas_drops() + scrapers.get_new_balance_drops() + scrapers.get_nike_drops()
    os.system("cls")
    all_shoes = pd.DataFrame(all_shoes)
    predicted_prices = []
    idx_to_remove = []
    for idx, row in all_shoes.iterrows():
        try: #In case scraper returns null values or bad data due to scraping error
            predicted_prices.append(predict_highest_bid(row.to_dict()))
        except:
            idx_to_remove.append(idx)
    all_shoes = all_shoes.drop(idx_to_remove)
    all_shoes['predicted_prices'] = predicted_prices
    all_shoes['predicted_profit'] = all_shoes['predicted_prices'] - all_shoes['price']
    all_shoes = all_shoes.sort_values(by = "predicted_profit", ascending = False)
    return all_shoes
    

#Predicting how the price will change in a week, two weeks, and a month and saving data to csv to be used by api

def predict_price_over_time(save_to_csv = False, path = "shoe_data.csv"):
    all_shoes = get_sorted_drops()
    after_week, after_2_weeks, after_month = [], [], []
    for idx, row in all_shoes.iterrows():
        row_dict = row.to_dict()
        after_week.append(predict_lowest_ask(row_dict, 700))
        after_2_weeks.append(predict_lowest_ask(row_dict, 1400))
        after_month.append(predict_lowest_ask(row_dict, 3000))

    all_shoes['price_after_week'] = after_week
    all_shoes['price_after_two_weeks'] = after_2_weeks
    all_shoes['price_after_month'] = after_month

    if save_to_csv:
        if os.path.exists(path):
            os.remove(path)
        all_shoes.to_csv(path)
    else:
        return all_shoes
    

