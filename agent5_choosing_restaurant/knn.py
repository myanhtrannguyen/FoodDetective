import json
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from fastapi import FastAPI, Query
import uvicorn

class RestaurantSearchAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df_items = None
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.scaler = MinMaxScaler()
        self.model = NearestNeighbors(n_neighbors=20, metric='euclidean')
        self.features = None
        
    def _clean_text(self, text):
        if not text: return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def load_and_prepare_data(self):
        data = []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                res_id = item['restaurant_id']
                for dish in item['menu']:
                    data.append({
                        'restaurant_id': res_id,
                        'dish_name': dish['name'],
                        'price': dish['price'],
                        'clean_name': self._clean_text(dish['name'])
                    })
        
        self.df_items = pd.DataFrame(data)
        
        tfidf_matrix = self.vectorizer.fit_transform(self.df_items['clean_name'])
        
        price_scaled = self.scaler.fit_transform(self.df_items[['price']])
        
        self.features = np.hstack([tfidf_matrix.toarray(), price_scaled])
        
        self.model.fit(self.features)
        print(f"Đã tải {len(self.df_items)} món ăn từ {self.df_items['restaurant_id'].nunique()} quán.")

    def search(self, query_text, target_price=None, top_k=10):
        nums = re.findall(r'\d+', query_text)
        if not target_price and nums:
            target_price = float(nums[0])
            query_text = re.sub(r'\d+', '', query_text).strip()
        
        if not target_price:
            target_price = self.df_items['price'].mean() 

        clean_q = self._clean_text(query_text)
        q_tfidf = self.vectorizer.transform([clean_q]).toarray()
        q_price = self.scaler.transform([[target_price]])
        
        query_vec = np.hstack([q_tfidf, q_price])
        
        distances, indices = self.model.kneighbors(query_vec, n_neighbors=50)
        
        results = self.df_items.iloc[indices[0]].copy()
        results['distance'] = distances[0]
        
        unique_restaurants = results.drop_duplicates(subset=['restaurant_id']).head(top_k)
        
        return unique_restaurants[['restaurant_id', 'dish_name', 'price']].to_dict(orient='records')