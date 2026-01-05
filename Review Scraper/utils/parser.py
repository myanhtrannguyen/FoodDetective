import re

def safe_text(el):
    return el.inner_text().strip() if el else None


def extract_user_id(item):
    """
    UserID thường nằm trong link profile:
    /thanh-vien/123456
    """
    user_link = item.query_selector("a[href*='/thanh-vien/']")
    if not user_link:
        return None

    href = user_link.get_attribute("href")
    if not href:
        return None

    match = re.search(r"/thanh-vien/(\d+)", href)
    return match.group(1) if match else None


def extract_created_at(item):
    """
    Foody render time dạng text:
    '3 ngày trước', '2 tháng trước', '12/08/2021'
    """
    time_el = item.query_selector(".review-time, .time, span[title]")
    return safe_text(time_el)


def parse_reviews(page, url):
    restaurant_id = page.get_attribute("[data-res-id]", "data-res-id")
    reviews = []

    review_items = page.query_selector_all(".review-item")

    for item in review_items:
        # Hover để Foody render thêm DOM nếu có
        try:
            item.hover(timeout=500)
        except:
            pass

        review_id = item.get_attribute("data-review-id")

        reviews.append({
            "ID": review_id if review_id else None,
            "RestaurantID": restaurant_id,
            "UserID": extract_user_id(item),
            "Rating": safe_text(item.query_selector(".review-points")),
            "Content": safe_text(item.query_selector(".review-des")),
            "CreatedAt": extract_created_at(item)
        })

    return {
        "url": url,
        "review": reviews,
        "initData": {}
    }
