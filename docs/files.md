# Tài liệu các file dự án

Mô tả theo mã nguồn hiện tại, ngày 07/10/2026. Không bao gồm môi trường
ảo, cache, Git và cấu hình IDE.

## Luồng chương trình

```text
maze_generator.json → maze_generator.py → main.py
                                           ├─ algorithms/: tìm đường
                                           ├─ visual/: hiển thị
                                           └─ report/: xuất biểu đồ
```

Tọa độ dùng `(row, col)`, đi 4 hướng. `-1` là tường; số dương là chi phí
đi vào ô. Tổng Cost bỏ ô bắt đầu và tính ô đích. Heuristic dùng Manhattan.

## `main.py` — Điều phối ứng dụng

- **Thành phần:** `build_panels()` và `main()`.
- **Đầu vào:** 5 bản đồ từ bộ đọc, thao tác bàn phím và chuột.
- **Xử lý:** tạo 3 bảng dùng cùng ma trận; chạy một bước mỗi thuật toán
  trong mỗi frame, vẽ kết quả và đổi điểm đầu/cuối khi chọn ô mở.
- **Đầu ra:** cửa sổ Pygame; gọi xuất `report/comparison.png` sau khi cả 3 xong.
- **Phụ thuộc:** các thuật toán, bộ đọc bản đồ, `AgentPanel`, `Scoreboard`, `plot_results`.

Phím `1–5` hoặc `↑↓` chuyển bản đồ; chuột trái chọn đầu, chuột phải chọn
đích; `H` đổi trọng số/heuristic; `R` chạy lại; `ESC` thoát. Chọn điểm
được giữ trong phiên hiện tại, không ghi vào JSON. H không chạy lại thuật toán.

## `maze_generator.py` — Đọc bản đồ cố định

- **Thành phần:** dataclass `MazeData(maze, start, goal)`, `load_fixed_mazes()`.
- **Đầu vào:** file JSON nằm cạnh module.
- **Xử lý:** yêu cầu đúng 5 bản đồ, chuyển dữ liệu thành mảng NumPy,
  kiểm tra trọng số nguyên, đầu/cuối hợp lệ và mọi ô mở nối với điểm đầu.
- **Đầu ra:** danh sách `(tên bản đồ, MazeData)`.
- **Phụ thuộc:** `json`, NumPy và các hàm kiểm tra/láng giềng trong `common.py`.

Tên file được giữ từ phiên bản cũ; hiện không còn sinh ngẫu nhiên.
Dữ liệu không hợp lệ báo lỗi khi đọc. `MazeData` cố định thuộc tính,
nhưng nội dung mảng vẫn có thể sửa; code ứng dụng hiện chỉ đọc ma trận.

## `maze_generator.json` — Dữ liệu bản đồ

Chứa danh sách 5 bản đồ: `20×20`, `24×24`, `28×28`, `32×32`, `36×36`.
Mỗi bản đồ có 4 trường:

| Trường | Nội dung |
|---|---|
| `name` | Tên hiển thị, ví dụ `Map 1` |
| `maze` | Ma trận trọng số nguyên; dữ liệu hiện tại dùng 1–9 và tường -1 |
| `start` | Tọa độ đầu mặc định `[row, col]` |
| `goal` | Tọa độ đích mặc định `[row, col]` |

Đầu mặc định là `[0,0]`, đích ở góc đối diện. File này được đọc khi mở
ứng dụng, không bị cập nhật khi bấm chuột.

## `algorithms/common.py` — Thành phần dùng chung

- **Kiểu dữ liệu:** `Coordinate`, `SearchGenerator`, `SearchStep`, `SearchResult`.
- **Hàm lưới:** `validate_maze()`, `neighbors()`, `manhattan()`.
- **Hàm kết quả:** `reconstruct()`, `search_result()`.
- **Hàm thực thi:** `timed_search()`, `finish_search()`, `demo()`.
- **Đầu vào:** ma trận, tọa độ, bảng cha hoặc generator tùy hàm.
- **Đầu ra:** bước tìm kiếm, đường đi, cost và thời gian thực thi.

`timed_search` chỉ cộng thời gian thực thi, gồm kiểm tra đầu vào;
không cộng thời gian chờ animation hay vẽ. `finish_search` lấy kết quả
return qua `StopIteration.value`. `demo` dùng chung ví dụ 5×5.

Các thuật toán yield `SearchStep(current, explored_count)` và return
`SearchResult(path, total_cost, explored_nodes, runtime)`.

## `algorithms/dijkstra.py` — Dijkstra

- **Hàm:** `dijkstra_steps()` chạy từng bước; `run_dijkstra()` chạy đến cuối.
- **Đầu vào:** ma trận, điểm đầu và đích.
- **Xử lý:** min-heap ưu tiên tổng chi phí đã đi `g`; cập nhật chi phí
  và cha khi tìm được đường rẻ hơn. Dừng khi lấy đích ra khỏi heap.
- **Đầu ra:** bước duyệt hoặc kết quả đường đi có chi phí tối ưu.
- **Phụ thuộc:** `heapq`, NumPy, `common.py`.

## `algorithms/a_star.py` — A* và Weighted A*

- **Hàm:** `astar_steps()`, `run_astar()`.
- **Đầu vào:** ma trận, đầu/đích, `heuristic_weight=1.0`.
- **Xử lý:** ưu tiên `f = g + w*h`, h là Manhattan; loại mục heap cũ
  và mở lại nút nếu có g tốt hơn. w hữu hạn nhỏ hơn 1 được đưa về 1.
- **Đầu ra:** bước duyệt hoặc kết quả tìm đường.
- **Phụ thuộc:** `heapq`, `math`, NumPy, `common.py`.

A* mặc định tối ưu với trọng số hợp lệ ít nhất 1. w > 1 là Weighted A*,
không bảo đảm cost tối ưu. Giao diện dùng w = 1.

## `algorithms/greedy.py` — Greedy Best-First Search

- **Hàm:** `greedy_steps()`, `run_greedy()`.
- **Đầu vào:** ma trận, đầu và đích.
- **Xử lý:** ưu tiên h nhỏ nhất, giữ cha khi phát hiện lần đầu;
  tập `discovered` tránh thêm cùng ô vào heap nhiều lần.
- **Đầu ra:** bước duyệt hoặc đường tìm được và cost thực của đường đó.
- **Phụ thuộc:** `heapq`, NumPy, `common.py`.

Greedy không dùng g để chọn nút, nên không bảo đảm chi phí tối ưu.
Ba file thuật toán đều có khối chạy ví dụ độc lập với cùng đầu/đích.

## `visual/window_agent.py` — Vẽ bảng mê cung

- **Thành phần:** dataclass `AgentPanel`.
- **Hàm:** `__post_init__()` tạo cache chữ; `displayed_value()` chọn số;
  `cell_at()` đổi pixel thành ô; `tick()` chạy một bước; `draw()` vẽ bảng.
- **Đầu vào:** mê cung, tọa độ, generator, bảng điểm, vùng vẽ và kích thước ô.
- **Đầu ra:** hình vẽ và trạng thái kết quả dùng để xuất biểu đồ.
- **Phụ thuộc:** Pygame, NumPy, kiểu dữ liệu/Manhattan chung, `Scoreboard`.

Màu: tường tối, ô mở xám, đã duyệt cam, đường đi xanh lá, đầu xanh dương,
đích đỏ. Chế độ trọng số hiện 0 trên ô đầu, các ô khác hiện chi phí đi vào;
chế độ H hiện Manhattan tới đích. Không thay đổi dữ liệu trọng số.

`final_path` giữ thứ tự đường; `path_cells` là set để tra cứu khi vẽ.
Không có đường giữ cost vô hạn và trạng thái `no path`.

## `visual/scoreboard.py` — Bảng chỉ số

- **Thành phần:** lớp `Scoreboard`, hàm khởi tạo và `draw()`.
- **Đầu vào:** font, tên thuật toán và dict chỉ số.
- **Đầu ra:** tên, trạng thái, thời gian, cost, số lần mở rộng và độ dài đường.
- **Phụ thuộc:** Pygame, `math.isfinite`.

Chưa hoàn tất thì thời gian hiện `...`, cost hiện `N/A`. Không có đường
cũng hiện cost `N/A`. File này hiển thị kết quả, không tự tính lại chi phí.

## `report/plot_results.py` — Xuất biểu đồ

- **Hàm:** `plot_results(results, output_path="comparison.png")`.
- **Đầu vào:** dict tên thuật toán → `runtime`, `cost`, `explored`, `path_len`.
- **Xử lý:** tạo 4 biểu đồ cột trong bố cục 2×2; giá trị vô hạn được
  thể hiện bằng khoảng trống ghi `N/A`.
- **Đầu ra:** PNG 150 DPI; tự tạo thư mục nếu cần, đóng figure sau lưu.
- **Phụ thuộc:** Matplotlib, `pathlib`, `math`.

Trong ứng dụng, ảnh lưu ở `report/comparison.png` và được ghi đè sau lần
so sánh hoàn tất tiếp theo. Không cần ảnh này để khởi động ứng dụng.

## `requirements.txt` — Thư viện

| Gói | Vai trò |
|---|---|
| `pygame-ce>=2.5.0` | Cửa sổ, bàn phím/chuột, vẽ ô và chữ; import bằng tên `pygame` |
| `numpy>=1.24.0` | Ma trận mê cung và kiểm tra trọng số |
| `matplotlib>=3.7.0` | Xuất biểu đồ so sánh |

Các dấu `>=` là giới hạn dưới, không khóa phiên bản. Code hiện dùng Python 3.14.

## Các file tài liệu

- `README.md`: cách cài, chạy, điều khiển và giới thiệu thuật toán.
- `docs/functions.md`: bảng tra các hàm, cấu trúc dữ liệu và quy ước chi phí.
- `docs/files.md`: tài liệu này, mô tả vai trò và quan hệ của từng file.

Chạy ứng dụng bằng `python main.py`; chạy ví dụ bằng
`python algorithms/dijkstra.py`, `python algorithms/a_star.py` hoặc
`python algorithms/greedy.py` trong môi trường đã cài thư viện.
