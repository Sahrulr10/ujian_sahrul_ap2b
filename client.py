import requests
import threading
import time
from datetime import datetime

BASE_API_URL = "http://127.0.0.1:5000/get_order_status"
ORDERS_TO_TRACK = ["ORD-101", "ORD-103", "ORD-999", "ORD-102", "ORD-105"]
NUM_REQUESTS = len(ORDERS_TO_TRACK)
CLIENT_LOG_FILE = "pizza_tracker_log.txt"

client_log_lock = threading.Lock()

with open(CLIENT_LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"--- Pizza Tracker Log Started: {datetime.now()} ---\n")

# ==============================================================================
# SOAL 1: Implementasi Logging Thread-Safe
# ==============================================================================
def log_client_activity_safe(thread_name, message):
    """
    TUGAS ANDA (Soal 1):
    Lengkapi fungsi ini untuk mencatat 'message' dari 'thread_name' ke
    CLIENT_LOG_FILE secara thread-safe menggunakan 'client_log_lock'.

    Langkah-langkah:
    1. Dapatkan 'client_log_lock' (gunakan 'with' statement untuk kemudahan).
    2. Buat timestamp (contoh: datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")).
    3. Format pesan log (contoh: f"[{timestamp}] [{thread_name}] {message}\n").
    4. Tulis pesan log ke CLIENT_LOG_FILE (mode append 'a', encoding 'utf-8').
    5. (Opsional) Cetak pesan log ke konsol juga.
    """
    # ===== TULIS KODE ANDA UNTUK SOAL 1 DI SINI =====
    for count in range(5):
        with client_log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            log_line = f"[{timestamp}] [{thread_name}] {message}\n"
            with open("pizza_tracker_log.txt", "a", encoding="utf-8") as f:
                f.write(log_line)
        time.sleep(0.05)
    # =================================================


# ==============================================================================
# SOAL 2: Implementasi Fungsi Permintaan API
# ==============================================================================
def request_order_status_from_api(order_id, current_thread_name):
    """
    TUGAS ANDA (Soal 2):
    Lengkapi fungsi ini untuk mengirim permintaan GET ke API status pesanan pizza
    dan mencatat hasilnya menggunakan fungsi 'log_client_activity_safe' yang
    telah Anda implementasikan di Soal 1.

    Langkah-langkah:
    1. Bentuk 'target_url' dengan menggunakan BASE_API_URL dan 'order_id' yang diberikan.
    2. Catat (menggunakan 'log_client_activity_safe') bahwa permintaan akan dikirim.
    3. Gunakan blok 'try-except' untuk menangani potensi error saat request.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke 'target_url' menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan sukses. Contoh: f"Berhasil! Pesanan {data.get('order_id', order_id)} untuk {data.get('customer', 'N/A')} status: {data.get('status', 'N/A')}"
              - Jika 404 (pesanan tidak ditemukan):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan error. Contoh: f"Error: ID Pesanan {order_id} tidak ditemukan. Pesan: {data.get('message', 'Not found')}"
              - Untuk status code lain:
                  - Catat pesan error umum. Contoh: f"Menerima status error dari API: {response.status_code} - {response.text[:100]}"
       b. Di blok 'except requests.exceptions.Timeout':
          - Catat pesan timeout.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Catat pesan error permintaan umum.
       d. Di blok 'except Exception as e':
          - Catat pesan kesalahan tak terduga.
    4. Setelah blok try-except, catat bahwa tugas untuk ID pesanan ini selesai.
    """
    target_url = f"{BASE_API_URL}?order_id={order_id}"
    # ===== TULIS KODE ANDA UNTUK SOAL 2 DI SINI =====
    try:
        response = requests.get(target_url, timeout=10)
        target_url = response.json()["url"]
    except requests.ecxeptions.Timeout:
        f"Berhasil! Pesanan {data.get('order_id', order_id)} untuk {data.get('customer', 'N/A')} status: {data.get('status', 'N/A')}"
    except requests.exceptions.RequestException as e:
        f"Menerima status error dari API: {response.status_code} - {response.text[:100]}"
    except Exception as e:
         f"Error: ID Pesanan {order_id} tidak ditemukan. Pesan: {data.get('message', 'Not found')}"
    # =================================================

def worker_thread_task(order_id, task_id):
    """Fungsi yang dijalankan oleh setiap worker thread."""
    thread_name = f"Worker-{task_id}"
    log_client_activity_safe(thread_name, f"Memulai pelacakan untuk ID Pesanan: {order_id}")
    request_order_status_from_api(order_id, thread_name)
    log_client_activity_safe(thread_name, f"Selesai pelacakan untuk ID Pesanan: {order_id}")

if __name__ == "__main__":
    log_client_activity_safe("MainClient", f"Memulai {NUM_REQUESTS} pelacakan pesanan pizza secara concurrent.")
    
    threads = []
    start_time = time.time()

    for i, order_id in enumerate(ORDERS_TO_TRACK):
        thread = threading.Thread(target=worker_thread_task, args=(order_id, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    log_client_activity_safe("MainClient", f"Semua pelacakan pesanan selesai dalam {total_time:.2f} detik.")
    print(f"\nLog aktivitas klien disimpan di: {CLIENT_LOG_FILE}")
    print(f"Total waktu eksekusi: {total_time:.2f} detik.")