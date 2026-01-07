from flask import Flask, request, jsonify
import requests
import torch
import pickle
import os
import logging
from together import Together 
from model import TripMindEncoder
from database import get_provinces_stats, agent_1_output
from flask_cors import CORS 
from extract_name_from_query import extract_city_from_query

# CONFIG
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TripMind-Gateway")

app = Flask(__name__)
CORS(app) 

MODEL = None
WORD2IDX = None
ASSETS = None
DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
PROVINCE_STATS = None

# Định nghĩa URL các Agent
AGENT_2_URL = "http://localhost:8000/ranking"
AGENT_3_URL = "http://localhost:9000/optimize"
AGENT_5_URL = "http://localhost:8001/api/recommend" # Giả định Agent 5 chạy ở port 8001

TOGETHER_CLIENT = Together(api_key="YOUR_TOGETHER_API_KEY_HERE")

def load_system():
    global MODEL, ASSETS, WORD2IDX, PROVINCE_STATS
    try:
        logger.info(f"Khởi tạo hệ thống trên thiết bị: {DEVICE}...")
        weights_path = "TripMind/agent1_choosing_destination/weights"
        
        with open(os.path.join(weights_path, "assets.pkl"), "rb") as f:
            ASSETS = pickle.load(f)
        
        WORD2IDX = ASSETS['word2idx']
        vocab_size = ASSETS['vocab_size']
        num_categories = len(ASSETS['cat_encoder'].classes_)
        
        MODEL = TripMindEncoder(
            vocab_size=vocab_size,
            num_categories=num_categories,
            d_model=128,   
            nhead=8,
            num_layers=4   
        ).to(DEVICE)
        
        weights_file = os.path.join(weights_path, "encoder_weights.pth")
        state_dict = torch.load(weights_file, map_location=DEVICE)
        MODEL.load_state_dict(state_dict)
        MODEL.eval()
        
        PROVINCE_STATS = get_provinces_stats()
        
        logger.info("Hệ thống Gateway tích hợp 4 Agent đã sẵn sàng!")
        
    except Exception as e:
        logger.error(f"Lỗi khởi động hệ thống: {str(e)}")
        raise e

def generate_storytelling(itinerary_data, user_query, food_data=None):
    """Cập nhật Agent 4 để nhận thêm thông tin món ăn"""
    if not itinerary_data or not isinstance(itinerary_data, list):
        return "Tôi đã tìm thấy thông tin cho bạn, hãy kiểm tra danh sách bên dưới nhé!"

    try:
        places_summary = ""
        for i, p in enumerate(itinerary_data, 1):
            name = p.get('name', 'Địa điểm không tên')
            score_pct = round(p.get('final_score', 0) * 100, 1)
            places_summary += f"{i}. {name} (Độ hài lòng: {score_pct}%)\n"
        
        # Thêm thông tin món ăn vào prompt nếu có
        food_context = ""
        if food_data:
            food_list = ", ".join([f"{f['dish_name']} ({f['price']}đ)" for f in food_data[:5]])
            food_context = f"\nNgoài ra, tại Hà Nội, tôi gợi ý bạn thử các món sau: {food_list}."

        prompt = f"""
                Bạn là chuyên gia tư vấn du lịch của TripMind.
                Khi người dùng hỏi: "{user_query}"

                Lộ trình di chuyển:
                {places_summary}
                {food_context}

                Hãy viết một đoạn phản hồi ngắn gọn, thân thiện. 
                Nếu có thông tin món ăn, hãy lồng ghép khéo léo để mời gọi người dùng thưởng thức ẩm thực địa phương.
                Yêu cầu:
                - Không giải thích suy luận.
                - Giải thích lộ trình đã tối ưu.
                - Trình bày bằng tiếng Việt gần gũi.
                """

        response = TOGETHER_CLIENT.chat.completions.create(
            model="ServiceNow-AI/Apriel-1.6-15b-Thinker",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Agent 4 LLM Error: {e}")
        return "Chúc bạn có một hành trình tuyệt vời tại Hà Nội!"

@app.route('/api/v1/recommend', methods=['POST'])
def recommend_places():
    try:
        data = request.get_json()
        query = data.get('query')
        province_id = data.get('province_id')

        if not query:
            return jsonify({"success": False, "error": "Missing query"}), 400

        if province_id is None:
            province_id = extract_city_from_query(query)
        
        p_id_str = str(province_id).zfill(2) 
        trip_type = data.get('trip_type', 'any')
        n_places = min(int(data.get('n_places', 5)), 10)
        
        # --- Step 1: AGENT 1 (Recall) ---
        candidates = agent_1_output(
            user_query=query, model=MODEL, word2idx=WORD2IDX, assets=ASSETS,
            device=DEVICE, province_id=p_id_str, trip_type=trip_type,
            n_places=5, max_reviews_per_place=5
        )
        
        if not candidates:
            return jsonify({"success": True, "data": [], "message": "Không tìm thấy kết quả"}), 200

        # --- Step 2: AGENT 2 (Ranking) ---
        ranked_places = candidates
        try:
            res2 = requests.post(AGENT_2_URL, json=candidates, timeout=10)
            if res2.status_code == 200: ranked_places = res2.json()
        except Exception as e: logger.warning(f"Agent 2 failed: {e}")

        top_candidates = ranked_places[:n_places]

        # --- Step 3: AGENT 3 (Route Optimization) ---
        final_itinerary = top_candidates 
        try:
            res3 = requests.post(AGENT_3_URL, json=top_candidates, timeout=10)
            if res3.status_code == 200:
                optimized_ids = res3.json()
                lookup = {str(p['id']): p for p in top_candidates}
                final_itinerary = [lookup[str(idx)] for idx in optimized_ids if str(idx) in lookup]
        except Exception as e: logger.warning(f"Agent 3 failed: {e}")

        # --- MỚI: GỌI AGENT 5 NẾU LÀ HÀ NỘI (Mã 01) ---
        recommended_foods = []
        if p_id_str == "01":
            logger.info("Phát hiện khu vực Hà Nội, đang gọi Agent 5 để tìm món ăn...")
            try:
                # Gọi Agent 5 với query của người dùng
                res5 = requests.get(AGENT_5_URL, params={"query": query}, timeout=5)
                if res5.status_code == 200:
                    food_response = res5.json()
                    recommended_foods = food_response.get('data', [])
            except Exception as e:
                logger.error(f"Lỗi khi gọi Agent 5: {e}")

        # --- Step 4: AGENT 4 (Storytelling) ---
        # Truyền thêm recommended_foods vào hàm generate
        ai_message = generate_storytelling(final_itinerary, query, food_data=recommended_foods)

        return jsonify({
            "success": True,
            "recommendation_text": ai_message,
            "data": final_itinerary,
            "food_recommendations": recommended_foods, # Trả về thêm list món ăn cho frontend           
            "metadata": {
                "province_id": p_id_str,
                "status": "Success",
                "agents_active": 5 if p_id_str == "01" else 4
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Pipeline Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# Khối này bây giờ sẽ không còn bị SyntaxError nữa vì try bên trên đã được đóng
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "device": str(DEVICE),
        "agents": {"A2": AGENT_2_URL, "A3": AGENT_3_URL}
    }), 200

if __name__ == "__main__":
    load_system()
    app.run(host='0.0.0.0', port=5000, debug=False)
