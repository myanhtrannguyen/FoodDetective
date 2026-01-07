import requests
import time
import os

try:
    from extract_name_from_query import extract_city_from_query
except ImportError:
    print("Cảnh báo: Không tìm thấy hàm extract_city_from_query. Dùng giá trị mặc định.")
    def extract_city_from_query(q): return "06" # Mặc định là Hà Nội

API_URL = "http://127.0.0.1:5000/api/v1/recommend"

def print_divider():
    print("-" * 60)

def test_full_pipeline(query, province_id, trip_type="any"):
    print(f" TRIPMIND MULTI-AGENT SYSTEM TEST ".center(60, "="))
    print(f"\nCâu lệnh: '{query}'")
    print(f"ID tỉnh: {province_id} | Loại hình: {trip_type}")
    print_divider()

    payload = {
        "query": query,
        "province_id": str(province_id),
        "trip_type": trip_type,
        "n_places": 3
    }

    try:
        print("Đang gửi yêu cầu đến Gateway (Port 5000)...")
        start_time = time.time()
        response = requests.post(API_URL, json=payload, timeout=30)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            res_data = response.json()
            itinerary = res_data.get('data', [])
            meta = res_data.get('metadata', {})

            print(f"\n✅ HOÀN TẤT TRONG {elapsed:.2f} GIÂY")
            recommendation_text = res_data.get('recommendation_text')

            print("\n" + " LỜI KHUYÊN TỪ CHUYÊN GIA TRIPMIND ".center(60, "✨"))
            if recommendation_text:
                print(recommendation_text)
            else:
                print("⚠️ Agent 4 không trả về văn bản gợi ý.")
            # print("".center(60, "✨"))
            print(f"Thống kê: Agent 1 đã quét {len(itinerary)} ứng viên.")
            
            print("\n" + " LỘ TRÌNH GỢI Ý (Đã tối ưu bởi Agent 3) ".center(60, "-"))
            
            if not itinerary:
                print("∅ Không tìm thấy địa điểm phù hợp.")
            else:
                for i, place in enumerate(itinerary, 1):
                    name = place.get('name', 'Không rõ tên')
                    # Lấy ID linh hoạt từ cả 2 key
                    d_id = place.get('id') or place.get('destination_id', 'N/A')
                    score = place.get('final_score', 0)
                    reviews = place.get('reviews', [])
                    short_rev = reviews[0][:100] + "..." if reviews else "Không có đánh giá."

                    print(f"[{i}] {name}")
                    print(f"   ├─ ID: {d_id}")
                    print(f"   ├─ Độ hài lòng (Agent 2): {score*100:.1f}%")
                    print(f"   └─ Nhận xét: {short_rev}\n")
                
                print_divider()
                print("Lưu ý: Thứ tự trên là lộ trình ngắn nhất do Agent 3 (DQN) tính toán.")
        else:
            print(f"❌ Lỗi API (Status {response.status_code}):")
            print(response.text)

    except requests.exceptions.Timeout:
        print("❌ Lỗi: Quá thời gian phản hồi (Timeout).")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    print("\n--- HỆ THỐNG TRỰC TIẾP TRIPMIND ---")
    user_query = input("Nhập yêu cầu du lịch của bạn: ")
    print("Đang phân tích địa danh...")
    extracted_id = extract_city_from_query(user_query)
    test_full_pipeline(user_query, extracted_id)