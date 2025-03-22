# Bài toán 16-Hậu sử dụng thuật toán di truyền

## Giới thiệu

Bài toán 16-Hậu yêu cầu đặt 16 quân hậu trên bàn cờ 16x16 sao cho không có hai quân hậu nào tấn công lẫn nhau.

Yêu cầu là hãy mô hình hóa bài toán dưới dạng local search và triển khai thuật toán Di truyền (Genetic Algorithm) để tìm lời giải.

**Ví dụ**: Một trạng thái hợp lệ có thể là:

`[0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]`

Trong đó quân hậu ở mỗi cột được đặt vào các hàng khác nhau để tránh xung đột theo hàng.

## Mô hình hóa bài toán

### Biểu diễn trạng thái

Mỗi trạng thái được biểu diễn dưới dạng một hoán vị của 16 số, trong đó chỉ số đại diện cho cột, và giá trị tại vị trí đó đại diện cho hàng của quân hậu trong cột tương ứng.

**Ví dụ**: Trạng thái:

`[3, 5, 7, 9, 11, 13, 15, 0, 2, 4, 6, 8, 10, 12, 14, 1]`

Nghĩa là:

- Quân hậu trong cột 0 được đặt ở hàng 3
- Quân hậu trong cột 1 được đặt ở hàng 5
- ...

**Lưu ý**: Mỗi khi nhắc đến cá thể trong bài toán này, ta có thể hiểu nó là 1 trạng thái

### Successor function

Các trạng thái mới được tạo ra thông qua các toán tử di truyền: chọn lọc (**selection**), lai ghép (**crossover**), và đột biến (**mutation**).

**Ví dụ**: Một cá thể ban đầu:

`[1, 3, 5, 7, 9, 11, 13, 15, 0, 2, 4, 6, 8, 10, 12, 14]`

Có thể biến đổi thành:

`[1, 3, 5, 7, 9, 11, 12, 15, 0, 2, 4, 6, 8, 10, 13, 14]`

Sau một bước đột biến.

### Fitness function

Fitness function trong bài toán này được định nghĩa hàm để tìm ra số cặp quân hậu không tấn công nhau.

Fitness value tối đa là 120 (**C(16,2)**).

**Ví dụ**: Nếu một trạng thái có 5 cặp quân hậu tấn công nhau, fitness value sẽ là 120 - 5 = 115.

## Triển khai Thuật toán Di truyền

### Chọn lọc (Selection)

Sử dụng phương pháp chọn lọc roulette wheel, trong đó các cá thể có fitness value cao hơn sẽ có xác suất được chọn cao hơn.

**Ví dụ**: Nếu một cá thể có fitness value là 100 và một cá thể khác có fitness value là 50, xác suất chọn cá thể đầu tiên sẽ cao gấp đôi so với cá thể thứ hai.

### Lai ghép (Crossover)

Hai cá thể cha mẹ thực hiện lai ghép hai điểm, trong đó hai điểm cắt ngẫu nhiên được chọn và các gene giữa hai điểm đó được hoán đổi để tạo ra cá thể con.

**Ví dụ**:

Cha: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]`

Mẹ: `[15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]`

Điểm cắt: **5**, **10**

Con: `[0, 1, 2, 3, 4, 10, 9, 8, 7, 6, 5, 11, 12, 13, 14, 15]`

### Đột biến (Mutation)

Một cột ngẫu nhiên được chọn và quân hậu trong cột đó sẽ được di chuyển đến một hàng ngẫu nhiên với xác suất được xác định bởi tỷ lệ đột biến (mutation rate), giá trị này do người dùng chỉ định.

**Ví dụ**: Nếu trạng thái hiện tại là:

`[0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]`

Và đột biến xảy ra tại cột **5**, hàng có thể thay đổi từ **10** thành **7**.

## Psuedo code

```
function GENETIC-ALGORITHM(population, FITNESS-FN)
    returns an individual

    inputs:
        population   ← a set of individuals
        FITNESS-FN   ← a function that measures the fitness of an individual

    repeat
        new_population ← empty set

        for i = 1 to SIZE(population) do
            x ← RANDOM-SELECTION(population, FITNESS-FN)
            y ← RANDOM-SELECTION(population, FITNESS-FN)
            child ← REPRODUCE(x, y)

            if (small random probability) then
                child ← MUTATE(child)

            add child to new_population

        population ← new_population

    until some individual is fit enough, or enough time has elapsed

    return the best individual in population, according to FITNESS-FN

function REPRODUCE(x, y)
    returns an individual
    inputs: x, y - parent individuals (list<int>)

    n ← LENGTH(x)
    c ← random number from 1 to n

    return CONCAT(SUBLIST(x, 1, c), SUBLIST(y, c + 1, n))
```

## Class design

### Problem

Chứa các thông tin của bài toán

1. **Thuộc tính**

   - `population_size`: Số lượng cá thể trong quần thể.
   - `mutation_rate`: Tỷ lệ đột biến khi tạo thế hệ mới.
   - `population`: Danh sách các cá thể trong quần thể.

2. **Phương thức**
   - `generate_random()`: Tạo bộ gene ngẫu nhiên cho cá thể.
   - `calculate_fitness()`: Tính toán độ thích nghi dựa trên số cặp quân hậu không tấn công nhau.
   - `mutate(mutation_rate=0.1)`: Thay đổi ngẫu nhiên một gene với xác suất nhất định.

### Individual

Cá thể trong quần thể (1 trạng thái của bài toán)

1. **Thuộc tính**

   - `size`: kích thước của bộ gene (số quân hậu trong bài toán N-Queens).
   - `genes`: Mảng chứa vị trí của các quân hậu trên bàn cờ.
   - `fitness`: Giá trị đánh giá mức độ thích nghi của cá thể.

2. **Phương thức**
   - `fitness_function(individual)`: Trả về độ thích nghi của cá thể.
   - `is_solution_found()`: Kiểm tra xem có cá thể nào đạt fitness tối đa hay chưa.

### GeneticAlgorithm

- Thực hiện quá trình tiến hóa của quần thể.
- Ghi lại quá trình chạy vào file CSV.

1. **Thuộc tính**

   - `problem`: Tham chiếu đến bài toán cần giải quyết để lấy thông tin.
   - `max_generations`: Số thế hệ tối đa để thuật toán chạy.
   - `elitism_k`: Số cá thể tốt nhất được giữ lại sau mỗi thế hệ.
   - `log_file`: File CSV ghi lại log quá trình chạy.
   - `csv_writer`: Đối tượng ghi dữ liệu vào file CSV.

2. **Phương thức**
   - `log(generation, best_individual)`: Ghi log thế hệ vào file CSV.
   - `selection()`: Chọn cá thể theo phương pháp roulette selection.
   - `crossover(parent1, parent2)`: Lai ghép hai cá thể để tạo cá thể con.
   - `run()`: Thực thi thuật toán di truyền và trả về cá thể tốt nhất.
