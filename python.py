import requests
import time
import os
import random
import string
from concurrent.futures import ThreadPoolExecutor

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def banner():
    print(BLUE + "╔═══════════════════════════════════════════╗")
    print("║ Tool Spam Comment - FB: Quang Huy (huycayf) ║")
    print("╚═══════════════════════════════════════════╝" + RESET)

def get_token_from_cookie(cookie):
    api_url = f"https://adidaphat.site/facebook/tokentocookie?type=EAAD6V7&cookie={cookie}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if "token" in data:
            return data["token"]
        else:
            return None
    except:
        return None

def random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_comment(post_id, token, message, image_url=None):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {"access_token": token}

    if image_url:
        payload["message"] = message
        payload["attachment_url"] = image_url
    else:
        payload["message"] = message

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(GREEN + f"[Thành Công]: {message}" + (f" | Ảnh: {image_url}" if image_url else "") + RESET)
        else:
            print(RED + f"[Thất Bại]: {response.text}" + RESET)
    except Exception as e:
        print(RED + f"[Lỗi]: {e}" + RESET)

def worker(post_id, token, comments, delay, count, images=None):
    for _ in range(count):
        base_comment = random.choice(comments)
        message = f"{base_comment} {random_string()}"
        image_url = None

        if images:
            image_url = random.choice(images)

        send_comment(post_id, token, message, image_url)
        time.sleep(delay)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()

    cookie = input(YELLOW + "Nhập Cookie Facebook: " + RESET).strip()
    token = get_token_from_cookie(cookie)
    if not token:
        print(RED + "Không lấy được token!" + RESET)
        return

    post_id = input(YELLOW + "Nhập ID Bài Viết FB: " + RESET).strip()

    print(YELLOW + "Chọn nguồn nội dung comment:" + RESET)
    print("1. Nhập thủ công")
    print("2. Lấy từ file cmt.txt")
    choice = input(YELLOW + "Lựa chọn (1 hoặc 2): " + RESET).strip()

    comments = []
    if choice == "1":
        raw_comments = input(YELLOW + "Nhập Nội Dung Comment (Ngăn Cách Bằng Dấu ,): " + RESET).strip()
        comments = [c.strip() for c in raw_comments.split(",") if c.strip()]
    elif choice == "2":
        try:
            with open("cmt.txt", "r", encoding="utf-8") as f:
                comments = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(RED + "Không tìm thấy file cmt.txt" + RESET)
            return
    else:
        print(RED + "Lựa chọn không hợp lệ!" + RESET)
        return

    if not comments:
        print(RED + "Không có nội dung comment để gửi!" + RESET)
        return

    use_image = input(YELLOW + "Có Muốn Gửi Kèm Ảnh Không? (y/n): " + RESET).strip().lower()
    images = None
    if use_image == "y":
        print(YELLOW + "Chọn nguồn ảnh:" + RESET)
        print("1. Nhập thủ công 1 link ảnh")
        print("2. Lấy random từ file images.txt")
        img_choice = input(YELLOW + "Lựa chọn (1 hoặc 2): " + RESET).strip()
        if img_choice == "1":
            link = input(YELLOW + "Nhập link ảnh: " + RESET).strip()
            if link:
                images = [link]
        elif img_choice == "2":
            try:
                with open("images.txt", "r", encoding="utf-8") as f:
                    images = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(RED + "Không tìm thấy file images.txt" + RESET)
                return

    try:
        delay = float(input(YELLOW + "Nhập Delay Giữa Các Comment (Giây): " + RESET))
        total_comments = int(input(YELLOW + "Nhập Số Lượng Comment: " + RESET))
        num_threads = int(input(YELLOW + "Nhập Số Lượng Thread (luồng): " + RESET))
    except ValueError:
        print(RED + "Delay, số lượng comment hoặc số thread không hợp lệ!" + RESET)
        return

    per_thread = total_comments // num_threads
    extra = total_comments % num_threads

    print(BLUE + f"Bắt đầu gửi {total_comments} comment với {num_threads} thread..." + RESET)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            count = per_thread + (1 if i < extra else 0)
            executor.submit(worker, post_id, token, comments, delay, count, images)

    print(GREEN + "Hoàn tất gửi comment!" + RESET)

if __name__ == "__main__":
    main()
