import requests
import time
import os

try:
    from extract_name_from_query import extract_city_from_query
except ImportError:
    print("Cảnh báo: Không tìm thấy hàm extract_city_from_query. Dùng giá trị mặc định.")
    # Lưu ý: Mã tỉnh Hà Nội trong hệ thống là "01"
    def extract_city_from_query(q): return "01" 

API_URL = "http://127.0.0.1:5000/api/v1/recommend"

def print_divider():
    print("-" * 60)

def test_full_pipeline(query, province_id, trip_type="any"):
    print(f" TRIPMIND MULTI-AGENT SYSTEM TEST ".center(60, "="))
    print(f"\nCâu lệnh: '{query}'")
    # Đảm bảo format ID tỉnh chuẩn 2 chữ số
    p_id_str = str(province_id).zfill(2)
    print(f"ID tỉnh: {p_id_str} | Loại hình: {trip_type}")
    print_divider()

    payload = {
        "query": query,
        "province_id": p_id_str,
        "trip_type": trip_type,
        "n_places": 3
    }

    try:
        print(f"Đang gửi yêu cầu đến Gateway (Port 5000)...")
        start_time = time.time()
        response = requests.post(API_URL, json=payload, timeout=30)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            res_data = response.json()
            itinerary = res_data.get('data', [])
            foods = res_data.get('food_recommendations', []) # Dữ liệu từ Agent 5
            meta = res_data.get('metadata', {})

            print(f"\n✅ HOÀN TẤT TRONG {elapsed:.2f} GIÂY")
            print(f"Trạng thái Agents: {meta.get('agents_active', 0)} agents đã tham gia xử lý.")

            # --- PHẦN 1: STORYTELLING (AGENT 4) ---
            print("\n" + " ✨ LỜI KHUYÊN TỪ CHUYÊN GIA TRIPMIND ✨ ".center(60, " "))
            recommendation_text = res_data.get('recommendation_text')
            if recommendation_text:
                print(recommendation_text)
            else:
                print("⚠️ Agent 4 không trả về văn bản gợi ý.")
            
            # --- PHẦN 2: LỘ TRÌNH ĐỊA ĐIỂM (AGENT 1, 2, 3) ---
            print("\n" + " 📍 LỘ TRÌNH THAM QUAN (Đã tối ưu) ".center(60, "-"))
            if not itinerary:
                print("∅ Không tìm thấy địa điểm phù hợp.")
            else:
                for i, place in enumerate(itinerary, 1):
                    name = place.get('name', 'Không rõ tên')
                    score = place.get('final_score', 0)
                    print(f"[{i}] {name} (Khớp: {score*100:.1f}%)")
            
            # --- PHẦN 3: ẨM THỰC (AGENT 5) - CHỈ HIỂN THỊ NẾU CÓ ---
            if foods:
                print("\n" + " 🍜 GỢI Ý MÓN NGON TẠI HÀ NỘI ".center(60, "-"))
                for i, food in enumerate(foods[:5], 1): # Lấy top 5 món
                    dish = food.get('dish_name')
                    price = food.get('price')
                    res_name = food.get('restaurant_id', '').replace('-', ' ').title()
                    print(f" 🍴 {dish:<25} | 💰 {price:,.0f}đ")
                    print(f"    └─ Quán: {res_name}")
            elif p_id_str == "01":
                print("\n⚠️ Không tìm thấy món ăn phù hợp tại Hà Nội cho query này.")

            print("\n" + "="*60)
        else:
            print(f"❌ Lỗi API (Status {response.status_code}):")
            print(response.text)

    except requests.exceptions.Timeout:
        print("❌ Lỗi: Quá thời gian phản hồi (Timeout).")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    print("\n--- HỆ THỐNG KIỂM THỬ TRIPMIND (Hỗ trợ Agent 5) ---")
    user_query = input("Nhập yêu cầu (VD: trà sữa ở Hà Nội): ")
    
    # Logic xác định tỉnh
    extracted_id = extract_city_from_query(user_query)
    
    test_full_pipeline(user_query, extracted_id)