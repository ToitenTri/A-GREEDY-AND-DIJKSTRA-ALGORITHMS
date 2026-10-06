# Các hàm trong dự án

Ứng dụng đọc 5 bản đồ cố định từ `maze_generator.json`. Code dùng Python 3.14.

## Quy ước

- `(row, col)`, đi 4 hướng; `-1` là tường, trọng số ít nhất 1.
- `c(u,v) = maze[v]`; `g(start) = 0`; Cost cộng `path[1:]`, gồm ô đích.
- Không có đường: `path=[]`, cost `inf`; giao diện hiện `no path` và `N/A`.
- Đầu = đích hợp lệ: `path=[start]`, cost 0. Độ dài đường tính số ô;
  khi có đường, số bước bằng số ô trừ 1.
- Phím H đổi trọng số/Manhattan; số 0 ở điểm đầu trong chế độ trọng số chỉ là hiển thị.

## `algorithms/common.py`

| Hàm / kiểu | Chức năng |
|---|---|
| `Coordinate` | Alias `tuple[int, int]` |
| `SearchStep` | Dataclass: `current`, `explored_count` |
| `SearchResult` | Dataclass: `path`, `total_cost`, `explored_nodes`, `runtime` (giây, mặc định 0) |
| `SearchGenerator` | `Generator[SearchStep, None, SearchResult]` |
| `validate_maze(maze, start, goal)` | Nhận NumPy ndarray; yêu cầu lưới 2D không rỗng, số thực hữu hạn, ô -1 hoặc >=1, đầu/cuối nguyên trong biên và không phải tường; lỗi kiểm tra ném `ValueError`, hợp lệ trả `None` |
| `neighbors(maze, node)` | Yield các ô mở kề trong biên |
| `manhattan(a, b)` | Khoảng cách Manhattan |
| `reconstruct(parent, start, goal)` | Trả list tọa độ từ đầu tới đích; không có cha của đích thì trả `[]`, trừ đầu = đích |
| `search_result(parent, maze, start, goal, explored)` | Trả `SearchResult`: dựng đường, cộng cost bỏ ô đầu; không có đường dùng `inf`; runtime ban đầu 0 |
| `timed_search(search)` | Decorator đo thời gian thực thi generator, không tính thời gian giữa các lần next |
| `finish_search(generator)` | Chạy hết generator và lấy `StopIteration.value` |
| `demo(name, run)` | Chạy ví dụ 5×5 với cùng đầu/đích cho các thuật toán |

`timed_search()` trả hàm generator nội bộ `steps(maze, start, goal, *args, **kwargs)`.
Hàm này kiểm tra đầu vào ở lần `next()` đầu tiên, chuyển tiếp các bước yield,
gán runtime vào kết quả cuối rồi return. Vì vậy lỗi đầu vào xảy ra khi bắt
đầu chạy generator, không phải lúc tạo generator.

`finish_search()` trả `SearchResult`; `demo()` in đường, cost, số ô duyệt,
runtime và trả `None`. `neighbors()` giữ thứ tự xuống, lên, phải, trái.

## Thuật toán

| File | Hàm | Chức năng |
|---|---|---|
| `dijkstra.py` | `dijkstra_steps(maze, start, goal)` | Ưu tiên g nhỏ nhất; yield bước và return kết quả |
| `dijkstra.py` | `run_dijkstra(...)` | Chạy hết Dijkstra |
| `a_star.py` | `astar_steps(..., heuristic_weight=1.0)` | Ưu tiên `g+w*h`; mở lại nút khi tìm thấy g tốt hơn |
| `a_star.py` | `run_astar(...)` | Chạy hết A* |
| `greedy.py` | `greedy_steps(maze, start, goal)` | Ưu tiên h; đánh dấu khi phát hiện để tránh thêm heap trùng |
| `greedy.py` | `run_greedy(...)` | Chạy hết Greedy |

Dijkstra và A* mặc định tối ưu trên trọng số hợp lệ. Weighted A* (w > 1)
và Greedy không bảo đảm cost tối ưu. Tham số w hữu hạn nhỏ hơn 1 được đưa về 1.
Runtime gồm kiểm tra đầu vào và tính đường, không gồm vẽ hay chờ animation.
`explored_nodes` đếm số lần mở rộng; Weighted A* có thể mở lại cùng một ô,
nên con số này có thể lớn hơn số tọa độ duy nhất được tô màu.

## Dữ liệu và giao diện

| File | Hàm / cấu trúc | Chức năng |
|---|---|---|
| `maze_generator.py` | `MazeData` | Ma trận, đầu, đích; không còn seed |
| `maze_generator.py` | `load_fixed_mazes()` | Đọc đúng 5 bản đồ, kiểm tra trọng số nguyên, đầu/cuối và mọi ô mở liên thông; trả danh sách `(name, MazeData)` |
| `main.py` | `build_panels(screen_w, screen_h, maze_data, font, show_heuristic=False)` | Tạo và trả list 3 bảng cùng generator, dùng chung ma trận chỉ đọc |
| `main.py` | `main()` | Xử lý sự kiện, chạy/vẽ từng bước, xuất biểu đồ khi hoàn tất |
| `window_agent.py` | `AgentPanel` | Trạng thái animation, đường, cache chữ, bảng điểm |
| `window_agent.py` | `__post_init__()` | Tạo chữ trọng số và heuristic vừa ô |
| `window_agent.py` | `displayed_value(row, col)` | Trọng số (đầu = 0) hoặc h |
| `window_agent.py` | `cell_at(position)` | Đổi `(x,y)` pixel sang `(row,col)`; ngoài lưới trả `None`, chưa loại ô tường |
| `window_agent.py` | `tick()` | Chạy một bước hoặc lưu kết quả cuối; hoàn tất thì không chạy tiếp |
| `window_agent.py` | `draw(screen)` | Vẽ lưới và bảng điểm; dùng set để tra ô trên đường |
| `scoreboard.py` | `Scoreboard.__init__(font, title)` | Lưu font/tên |
| `scoreboard.py` | `Scoreboard.draw(surface, x, y, metrics)` | Hiện chỉ số; đang chạy chưa có cost/time cuối thì hiện N/A và ... |
| `plot_results.py` | `plot_results(results, output_path="comparison.png")` | Lưu 4 biểu đồ PNG 150 DPI; giá trị không hữu hạn thành khoảng trống ghi N/A |

`MazeData` cố định thuộc tính nhưng nội dung NumPy vẫn sửa được; các thuật toán
và bảng vẽ hiện chỉ đọc. Chọn đầu/cuối dùng `dataclasses.replace()`.
File JSON thiếu khóa, sai cấu trúc hoặc không hợp lệ sẽ báo lỗi khi đọc.

Các hàm `main()`, `tick()`, `draw()` và `plot_results()` trả `None`.
`metrics` của bảng điểm dùng `status`, `runtime`, `cost`, `explored`, `path_len`;
`results` của biểu đồ là dict tên thuật toán → 4 chỉ số sau (không có status).
Khi không có đường, `tick()` giữ cost `inf`; bảng hiện `no path` và `N/A`.

Điều khiển: `1–5` / `↑↓` chuyển bản đồ, chuột trái/phải chọn đầu/đích,
`H` đổi số, `R` chạy lại, `ESC` thoát. Điểm được giữ trong phiên, không ghi JSON.

Xem [tài liệu các file](files.md) để biết vai trò và quan hệ giữa các module.
