# Ứng dụng so sánh thuật toán giải mê cung

Ứng dụng trực quan hóa và so sánh 3 thuật toán tìm đường trên **cùng một mê cung có trọng số**:

- **Uniform Cost Search (UCS)**
- **A\***
- **Greedy Best-First Search**

Mục tiêu là giúp người học quan sát rõ khác biệt giữa:

1. chiến lược chọn ô kế tiếp,  
2. số ô đã duyệt,  
3. chi phí đường đi và thời gian chạy.

---

## 1. Yêu cầu môi trường

- Python **3.14**
- `pygame-ce`
- `numpy`
- `matplotlib`

Cài thư viện:

```bash
pip install -r requirements.txt
```

---

## 2. Cấu trúc dự án

```text
.
├── main.py
├── maze_generator.py
├── algorithms/
│   ├── ucs.py
│   ├── a_star.py
│   └── greedy.py
├── visual/
│   ├── window_agent.py
│   └── scoreboard.py
├── report/
│   └── plot_results.py
└── requirements.txt
```

---

## 3. Chạy ứng dụng chính

```bash
python main.py
```

Điều khiển trong cửa sổ:

- `R`: sinh mê cung ngẫu nhiên mới
- `F`: quay về mê cung cố định (`seed=42`)
- `UP`/`DOWN`: tăng/giảm level độ khó (5 level)

Sau khi cả 3 thuật toán hoàn tất, biểu đồ được lưu tại:

`report/comparison.png`

---

## 4. Chạy test độc lập từng thuật toán

Mỗi file thuật toán đều có khối `if __name__ == "__main__":` để chạy thử độc lập:

```bash
python algorithms/ucs.py
python algorithms/a_star.py
python algorithms/greedy.py
```

Kết quả in ra gồm:

- Đường đi
- Tổng chi phí
- Số ô đã duyệt
- Thời gian chạy

---

## 5. Giải thích thuật toán

### 5.1 Uniform Cost Search (UCS)

**Ý tưởng:** luôn mở rộng ô có **chi phí tích lũy nhỏ nhất từ start**.

- Ưu tiên theo `g(n)` (chi phí thực đã đi)
- Đảm bảo tối ưu chi phí (với trọng số không âm)
- Thường duyệt nhiều ô hơn A\*

### 5.2 A*

**Ý tưởng:** mở rộng ô có điểm `f(n) = g(n) + h(n)`.

- `g(n)`: chi phí thực từ start
- `h(n)`: heuristic Manhattan tới goal
- Thường ít duyệt hơn UCS vì được “dẫn hướng” tới đích
- Khi heuristic phù hợp, vẫn giữ chất lượng đường đi tốt

### 5.3 Greedy Best-First Search

**Ý tưởng:** chỉ xét `h(n)` để chọn ô gần đích nhất.

- Không tối ưu theo chi phí thực
- Trực quan thường “lao nhanh” về phía đích
- Có thể cho đường đi chi phí cao hơn UCS/A\*

---

## 6. Giải thích các hàm trong từng module thuật toán

Ba module (`ucs.py`, `a_star.py`, `greedy.py`) có cùng khung:

### 6.1 `SearchStep` (dataclass)

- `current`: ô hiện tại đang được xử lý
- `explored_count`: tổng số ô đã duyệt đến thời điểm hiện tại

Dùng để `yield` theo thời gian thực cho phần Pygame vẽ animation.

### 6.2 `SearchResult` (dataclass)

- `path`: danh sách tọa độ đường đi từ start đến goal
- `total_cost`: tổng chi phí đường đi
- `explored_nodes`: tổng số ô đã duyệt
- `runtime`: thời gian chạy (giây)

### 6.3 `_neighbors(maze, node)`

Sinh các ô kề hợp lệ theo 4 hướng (trên, dưới, trái, phải), loại bỏ:

- ô vượt biên
- ô tường (`-1`)

### 6.4 `_reconstruct(parent, start, goal)`

Khôi phục đường đi từ bảng `parent` bằng cách đi ngược từ `goal` về `start`.

### 6.5 Hàm chính dạng generator

- `ucs_steps(...)`
- `astar_steps(...)`
- `greedy_steps(...)`

Các hàm này:

1. đo thời gian bằng `time.perf_counter()`,
2. duyệt từng bước và `yield SearchStep`,
3. kết thúc thì `return SearchResult`.

### 6.6 Hàm chạy đầy đủ (không animation)

- `run_ucs(...)`
- `run_astar(...)`
- `run_greedy(...)`

Các hàm này tiêu thụ toàn bộ generator và trả về kết quả cuối.

---

## 7. Ghi chú trực quan khi quan sát

- **Uniform Cost Search (UCS)**: vùng tô màu thường lan rộng.
- **A\***: vùng tô tập trung hơn theo hướng đích.
- **Greedy**: thường tiến nhanh về đích nhưng có thể kém tối ưu chi phí.

---

## 8. Level độ khó (5 mức)

Ứng dụng có 5 level từ dễ đến khó:

1. Level 1: `20x20`, `wall_prob=0.14`
2. Level 2: `24x24`, `wall_prob=0.18`
3. Level 3: `28x28`, `wall_prob=0.22`
4. Level 4: `32x32`, `wall_prob=0.26`
5. Level 5: `36x36`, `wall_prob=0.30`

Màn hình chạy ở độ phân giải **Full HD (1920x1080)**.
# A*, GREEDY AND UCS-ALGORITHMS
