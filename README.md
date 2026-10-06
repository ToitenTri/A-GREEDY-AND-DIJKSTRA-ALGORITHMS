













# Ứng dụng so sánh thuật toán giải mê cung

Ứng dụng trực quan hóa và so sánh 3 thuật toán tìm đường trên **cùng một mê cung có trọng số**:

- **Dijkstra**
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
├── maze_generator.json
├── maze_generator.py
├── algorithms/
│   ├── dijkstra.py
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

- `1`–`5`: chọn một trong 5 bản đồ cố định
- `UP`/`DOWN`: chuyển bản đồ
- Chuột trái: chọn điểm bắt đầu trên ô mở ở bất kỳ bảng thuật toán nào
- Chuột phải: chọn điểm kết thúc trên ô mở ở bất kỳ bảng thuật toán nào
- `R`: chạy lại trên bản đồ và các điểm đang chọn
- `H`: đổi số trong ô giữa trọng số và heuristic Manhattan tới đích (đích có h = 0).
  Đây chỉ là chế độ hiển thị, không thay đổi cost hoặc khởi động lại thuật toán.
  Trong chế độ trọng số, ô bắt đầu hiển thị 0 vì chưa di chuyển; các ô khác
  hiển thị chi phí đi vào ô. Tổng Cost bỏ ô bắt đầu và tính cả ô đích.
  Trong chế độ heuristic, mọi ô hiển thị khoảng cách Manhattan tới đích.
- `ESC`: thoát

Khi đổi điểm bắt đầu hoặc kết thúc, cả 3 thuật toán chạy lại. Các điểm
được giữ khi chuyển qua lại giữa bản đồ trong phiên hiện tại. Ô tường
không thể được chọn. Bản đồ không thay đổi giữa các lần chạy ứng dụng.

Sau khi cả 3 thuật toán hoàn tất, biểu đồ được lưu tại:

`report/comparison.png`

---

## 4. Chạy test độc lập từng thuật toán

Mỗi file thuật toán đều có khối `if __name__ == "__main__":` để chạy thử độc lập:

```bash
python algorithms/dijkstra.py
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

### 5.1 Dijkstra

**Ý tưởng:** luôn mở rộng ô có **chi phí tích lũy nhỏ nhất từ start**.

- Ưu tiên theo `g(n)` (chi phí thực đã đi)
- Đảm bảo tối ưu chi phí (với trọng số không âm)
- Thường duyệt nhiều ô hơn A\*

### 5.2 A*

**Ý tưởng:** mở rộng ô có điểm `f(n) = g(n) + h(n)`.

- `g(n)`: chi phí thực từ start
- `h(n)`: heuristic Manhattan tới goal
- Thường ít duyệt hơn Dijkstra vì được “dẫn hướng” tới đích
- Khi heuristic phù hợp, vẫn giữ chất lượng đường đi tốt

### 5.3 Greedy Best-First Search

**Ý tưởng:** chỉ xét `h(n)` để chọn ô gần đích nhất.

- Không tối ưu theo chi phí thực
- Trực quan thường “lao nhanh” về phía đích
- Có thể cho đường đi chi phí cao hơn Dijkstra/A\*

---

## 6. Giải thích các hàm trong từng module thuật toán

Ba module (`dijkstra.py`, `a_star.py`, `greedy.py`) có cùng khung:

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

- `dijkstra_steps(...)`
- `astar_steps(...)`
- `greedy_steps(...)`

Các hàm này:

1. đo thời gian bằng `time.perf_counter()`,
2. duyệt từng bước và `yield SearchStep`,
3. kết thúc thì `return SearchResult`.

### 6.6 Hàm chạy đầy đủ (không animation)

- `run_dijkstra(...)`
- `run_astar(...)`
- `run_greedy(...)`

Các hàm này tiêu thụ toàn bộ generator và trả về kết quả cuối.

---

## 7. Ghi chú trực quan khi quan sát

- **Dijkstra**: vùng tô màu thường lan rộng.
- **A\***: vùng tô tập trung hơn theo hướng đích.
- **Greedy**: thường tiến nhanh về đích nhưng có thể kém tối ưu chi phí.

---

## 8. Năm bản đồ cố định

Ứng dụng đọc 5 bản đồ có trọng số từ `maze_generator.json`, không sinh ngẫu nhiên khi chạy:

1. Map 1: `20x20`
2. Map 2: `24x24`
3. Map 3: `28x28`
4. Map 4: `32x32`
5. Map 5: `36x36`

Tất cả ô mở của mỗi bản đồ thuộc cùng một vùng liên thông, nên có thể
chọn bất kỳ hai ô mở làm điểm bắt đầu và kết thúc.

Kích thước cửa sổ lấy theo độ phân giải màn hình hiện tại.
# A*, GREEDY AND Dijkstra-ALGORITHMS
