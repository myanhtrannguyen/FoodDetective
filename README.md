🍔 Food Detective – Scrape Review (Foody.vn)
⚠️ BẮT BUỘC ĐỌC TRƯỚC KHI CHẠY

Script này dùng để scrape REVIEW từ Foody.vn.

Foody hiện có cơ chế chống bot rất mạnh.
👉 Nếu KHÔNG đăng nhập Foody trong trình duyệt Playwright, script sẽ:

❌ Chỉ lấy được ~10–13 review / nhà hàng

❌ KHÔNG scrape được toàn bộ review

❌ Kết quả KHÔNG đạt yêu cầu

✅ YÊU CẦU BẮT BUỘC

Python ≥ 3.9

Playwright đã cài browser

Tài khoản Foody hợp lệ

Trình duyệt KHÔNG chạy headless

🔧 CÀI ĐẶT (CHỈ CẦN 1 LẦN)
pip install playwright beautifulsoup4 requests
python3 -m playwright install chromium

🧪 BƯỚC 1 – TEST (BẮT BUỘC)

👉 Luôn chạy test trước khi scrape hàng loạt

cd review
python test_review.py

🔐 QUY TRÌNH ĐĂNG NHẬP FOODY (BẮT BUỘC)

Khi chạy script:

Một cửa sổ Chromium sẽ mở ra

Script sẽ dừng và hiển thị:

👉 Vui lòng đăng nhập Foody trong browser

TESTER PHẢI:

Đăng nhập Foody bằng tài khoản thật

Có thể đăng nhập bằng:

Email / Password

Google

Facebook

Sau khi đăng nhập thành công:

Phải thấy avatar hoặc tên user trên trang Foody

Quay lại Terminal và nhấn ENTER

❗ NẾU KHÔNG ĐĂNG NHẬP

Script vẫn chạy

Nhưng kết quả sẽ là:

🧾 Reviews scraped: 13


👉 ĐÂY LÀ KẾT QUẢ SAI

✅ DẤU HIỆU CHẠY ĐÚNG

Trong Terminal phải thấy:

🧾 Reviews scraped: 40
🧾 Reviews scraped: 85
🧾 Reviews scraped: 120


👉 Lớn hơn 13 review → OK

🚀 CÁC SCRIPT CÓ SẴN
1️⃣ test_review.py

Test 1 URL

Xác nhận login + scroll OK

Dùng để debug

2️⃣ scrape_review.py

Chạy nhiều URL (số lượng ít)

❌ Không checkpoint

❌ Không resume

Dùng cho demo / test nhỏ

3️⃣ scrape_review_advanced.py ⭐

Chạy toàn bộ dữ liệu

✅ Có checkpoint

✅ Resume khi dừng

✅ Auto retry

Dùng cho production

⛔ NHỮNG ĐIỀU KHÔNG ĐƯỢC LÀM

❌ Không chạy headless=True

❌ Không nhấn ENTER khi chưa đăng nhập

❌ Không scroll quá nhanh

❌ Không mở thêm tab trong browser

❌ Không đóng browser khi script đang chạy

🐛 XỬ LÝ LỖI THƯỜNG GẶP
❌ Chỉ scrape được 13 review

👉 Chưa đăng nhập Foody
👉 Login lại, chạy lại script

❌ Browser không mở

👉 Chưa cài browser cho Playwright

python3 -m playwright install chromium

❌ File không được tạo

👉 Chưa tạo thư mục data/

mkdir data

📊 OUTPUT FORMAT
{
  "url": "https://www.foody.vn/...",
  "review": [
    {
      "ID": "...",
      "RestaurantID": "...",
      "UserID": "...",
      "Rating": "...",
      "Content": "...",
      "CreatedAt": "..."
    }
  ],
  "initData": {}
}

🧠 GHI NHỚ QUAN TRỌNG NHẤT

Scrape review Foody = BẮT BUỘC LOGIN + BROWSER THẬT + SCROLL THẬT

Nếu thiếu 1 trong 3, kết quả sẽ KHÔNG ĐÚNG.

✅ CHECKLIST TRƯỚC KHI CHẠY FULL

 Đã chạy test_review.py

 Đăng nhập Foody thành công (thấy avatar)

 Review > 13

 Browser không headless

 Thư mục data/ tồn tại

🎯 KẾT LUẬN

Pipeline scrape review đã sẵn sàng.
Tester chỉ cần:

cd review
python test_review.py


Nếu OK → chạy:

python scrape_review_advanced.py

🍔 Food Detective – Tóm Tắt Hoàn Chỉnh (Scrape Review)
✅ ĐÃ TẠO XONG

Tôi đã tạo đầy đủ các công cụ để scrape REVIEW từ Foody.vn bằng browser automation (Playwright), vượt qua giới hạn ~13 review.

📦 CÁC FILE ĐÃ TẠO
🔧 Scripts (5 files)

test_review.py ⭐ BẮT ĐẦU TỪ ĐÂY

Test với 1 URL nhà hàng

Kiểm tra đăng nhập Foody

Kiểm tra scroll load review

Xác nhận scrape được >13 review

scrape_review.py

Script đơn giản để scrape review cho nhiều URLs

❌ Không có checkpoint

Phù hợp test data nhỏ / demo

scrape_review_advanced.py ⭐ KHUYÊN DÙNG

Script nâng cao để scrape toàn bộ URLs

✅ Có checkpoint

✅ Có thể dừng (Ctrl+C) và resume

✅ Auto-retry khi lỗi

Hiển thị progress và ETA

run.py

Menu tương tác để chọn script

Giống cấu trúc run.py của initData

demo.py

Hiển thị thống kê tổng quan review

Không thực hiện scrape

📖 Documentation (2 files)

README.md – Hướng dẫn đầy đủ và chi tiết (file này)

QUICKSTART.md – Hướng dẫn nhanh để bắt đầu

📊 Data Files

final_result_link.json – 7,579 links nhà hàng ở Hà Nội (dùng chung với initData)

data/test_review_result.json – Kết quả test mẫu (1 nhà hàng)

data/review_result.json – Kết quả scrape review

data/checkpoint.json – Trạng thái resume

data/scrape_errors.json – Log lỗi khi scrape

🚀 CÁCH SỬ DỤNG NHANH
Bước 1: Cài đặt (chỉ cần 1 lần)
pip3 install playwright beautifulsoup4 requests
python3 -m playwright install chromium

Bước 2: Test thử với 1 nhà hàng (BẮT BUỘC)
cd review
python3 test_review.py


➡️ Khi browser mở ra:

Đăng nhập Foody bằng tài khoản thật

Sau khi thấy avatar → quay lại terminal → nhấn ENTER
➡️ Xem kết quả trong data/test_review_result.json

❗ Nếu số review ≤ 13 → đăng nhập chưa đúng, KHÔNG chạy bước tiếp theo

Bước 3: Chạy cho TẤT CẢ nhà hàng
python3 scrape_review_advanced.py


Lưu ý:

⏱️ Mất khoảng 4–6 giờ (phụ thuộc số review)

✅ Có thể dừng (Ctrl+C) và chạy lại để resume

💾 Tự động lưu kết quả theo checkpoint

🎯 DỮ LIỆU NHẬN ĐƯỢC

Mỗi nhà hàng sẽ có đầy đủ danh sách review:

🧾 Thông tin Review

Review ID

RestaurantID

UserID

Điểm đánh giá

Nội dung review

Thời gian tạo (relative time từ Foody)

📊 VÍ DỤ DỮ LIỆU
{
  "url": "https://www.foody.vn/ha-noi/pizza-hut-xuan-thuy",
  "review": [
    {
      "ID": "12345678",
      "RestaurantID": "35998",
      "UserID": "998877",
      "Rating": "8.0",
      "Content": "Pizza ngon, phục vụ ổn",
      "CreatedAt": "3 ngày trước"
    }
  ],
  "initData": {}
}

💡 MẸO QUAN TRỌNG
✅ Nên làm:

Luôn chạy test_review.py trước

Kiểm tra review >13 trước khi chạy full

Dùng scrape_review_advanced.py cho production

Để máy chạy qua đêm

⚠️ Lưu ý:

❗ BẮT BUỘC đăng nhập Foody

❌ Không chạy headless=True

❌ Không scroll quá nhanh

❌ Không mở nhiều tab trong browser

Có delay ~1.5–2s giữa các lần scroll

🐛 Nếu gặp lỗi:

Chạy python3 test_review.py để kiểm tra login + scroll

Kiểm tra thư mục data/ đã tồn tại chưa

Xem file data/scrape_errors.json để biết URL lỗi

Đảm bảo đã chạy:

python3 -m playwright install chromium

📈 TIẾN ĐỘ DỰ KIẾN
📊 Tổng số: 7,579 nhà hàng
🧾 Tổng review: hàng trăm nghìn
⏱️  Thời gian: ~4–6 giờ
💾 Kích thước output: ~300–500 MB

🎬 BẮT ĐẦU NGAY
# 1. Test (1 phút)
python3 test_review.py

# 2. Xem thống kê
python3 demo.py

# 3. Chạy full
python3 scrape_review_advanced.py

📁 KẾT QUẢ CUỐI CÙNG

File data/review_result.json chứa:

✅ Review đầy đủ của 7,579 nhà hàng

✅ Không bị giới hạn 13 review

✅ Format JSON thống nhất với initData

✅ Sẵn sàng gộp dataset & phân tích


Nếu OK → chạy:

python scrape_review_advanced.py

