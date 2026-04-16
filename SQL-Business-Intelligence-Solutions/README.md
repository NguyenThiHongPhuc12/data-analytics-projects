# Truy vấn SQL cho Phân tích Kinh doanh (E-commerce Case Study)

## Tổng quan dự án
Dự án này tập trung vào việc sử dụng ngôn ngữ SQL để giải quyết các bài toán phân tích dữ liệu thực tế trong lĩnh vực Thương mại điện tử. Mục tiêu chính là trích xuất các insight về hiệu suất doanh thu, hành vi khách hàng và các chỉ số đo lường mức độ giữ chân người dùng.

## Các bài toán kinh doanh đã giải quyết
Tôi đã xây dựng các giải pháp SQL cho các tình huống sau:
1. **Hiệu suất Danh mục sản phẩm:** Xác định sản phẩm bán chạy nhất trong mỗi danh mục bằng **Window Functions**.
2. **Lòng trung thành khách hàng:** Tính toán **Tỷ lệ khách hàng quay lại (Repeat Purchase Rate)**.
3. **Hành vi mua hàng:** Đo lường **Số ngày trung bình giữa các đơn hàng** để hiểu chu kỳ mua sắm bằng hàm **LAG()**.
4. **Cảnh báo rời bỏ (Churn):** Nhận diện khách hàng có nguy cơ rời bỏ dựa trên thời gian tương tác cuối cùng.

## Kỹ năng kỹ thuật đã áp dụng
* **Advanced Joins:** Kết hợp các bảng Customers, Orders, Products để có cái nhìn toàn diện.
* **Window Functions:** Sử dụng `RANK() OVER()` và `PARTITION BY` để xếp hạng dữ liệu.
* **Time-Series Analysis:** Sử dụng `DATEDIFF` và `LAG()` để tính toán khoảng thời gian giữa các giao dịch.
* **Tư duy Logic:** Sử dụng `CASE WHEN`, `CTE (Common Table Expressions)` để xây dựng các KPI phức tạp.

*Dự án thực hiện bởi Nguyễn Thị Hồng Phúc
