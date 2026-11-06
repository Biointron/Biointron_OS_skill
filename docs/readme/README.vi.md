<div align="center">

<p dir="ltr">
<a href="../../README.md" lang="en" dir="ltr">English</a> ·
<a href="README.zh-CN.md" lang="zh-CN" dir="ltr">简体中文</a> ·
<a href="README.zh-TW.md" lang="zh-TW" dir="ltr">繁體中文</a> ·
<a href="README.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="README.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="README.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="README.ru.md" lang="ru" dir="ltr">Русский</a> ·
<strong lang="vi" dir="ltr">Tiếng Việt</strong> ·
<a href="README.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="README.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="README.es.md" lang="es" dir="ltr">Español</a> ·
<a href="README.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="README.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="README.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="README.pt-BR.md" lang="pt-BR" dir="ltr">Português (Brasil)</a> ·
<a href="README.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="README.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="README.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="README.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="README.el.md" lang="el" dir="ltr">Ελληνικά</a> ·
<a href="README.ml.md" lang="ml" dir="ltr">മലയാളം</a> ·
<a href="README.ur-Latn.md" lang="ur-Latn" dir="ltr">Roman Urdu</a> ·
<a href="README.ro.md" lang="ro" dir="ltr">Română</a>
</p>

# Biointron OS

### Kết nối tác nhân AI của bạn với các dịch vụ Biointron.

Từ yêu cầu đặt hàng đến kết quả báo cáo, đưa quy trình Biointron vào những công cụ bạn đang sử dụng.<br />
MCP cung cấp kết nối. Skills hướng dẫn quy trình. Bạn luôn nắm quyền kiểm soát.

[![Danh mục công cụ MCP](https://img.shields.io/badge/MCP-tool_catalog-087F8C?style=flat-square)](../../docs/tool-catalog.md)
[![Skills](https://img.shields.io/badge/Agent-Skills-234E70?style=flat-square)](../../skills/README.md)
[![Giấy phép phi thương mại](https://img.shields.io/badge/License-Noncommercial-6B7280?style=flat-square)](../../LICENSE)
[![Beta Playground](https://img.shields.io/badge/Release-Beta_Playground-D7A345?style=flat-square)](#beta)

<br />

<!-- HERO: Keep the artwork path in sync across all language versions. -->
<img src="../../assets/biointron-os-hero.png" alt="Biointron OS" width="1000" />

<br />

**[Bắt đầu](#get-started) · [Công cụ MCP](../../docs/tool-catalog.md) · [Skills](../../skills/README.md) · [API và ví dụ](../../docs/api.md) · [Nền tảng trực tuyến](#online-platform) · [Câu hỏi thường gặp](#faq)**

</div>

---

## Một nền tảng. Ba cách kết nối.

Biointron OS là giao diện truy cập dịch vụ Biointron dành cho tác nhân AI, mô hình và con người. Nền tảng kết hợp quyền truy cập dịch vụ với hướng dẫn quy trình, theo lộ trình bao gồm đặt hàng, gửi dữ liệu thiết kế, theo dõi tiến độ và nhận kết quả.

| Dành cho tác nhân | Dành cho mô hình | Dành cho người dùng |
| :--- | :--- | :--- |
| Khám phá và gọi dịch vụ qua **MCP**. | Làm việc với **dữ liệu có cấu trúc** và các giao diện có tài liệu mô tả. | Truy cập quy trình qua **giao diện tương tác**. |
| Kết hợp việc gọi công cụ với Skills dành riêng cho từng tác vụ. | Các quy ước dữ liệu đang được thống nhất trong giai đoạn Beta. | Trải nghiệm web được cung cấp riêng, không nằm trong kho lưu trữ này. |

Kho lưu trữ này là nơi công khai Skills, hướng dẫn kết nối, danh mục công cụ và ví dụ. Các dịch vụ nghiệp vụ của Biointron vận hành riêng biệt.

<a id="get-started"></a>

## Bắt đầu

### 1 · Kết nối MCP

Liên hệ đầu mối Biointron của bạn để nhận mã thông báo truy cập dịch vụ và quyền sử dụng. Trong ứng dụng khách MCP hỗ trợ **Streamable HTTP** và **xác thực Bearer**, hãy thêm:

| Thiết lập | Giá trị |
| :--- | :--- |
| Tên | `BiointronOS_MCP` |
| Phương thức truyền | Streamable HTTP |
| URL | `https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp` |
| Xác thực | `Authorization: Bearer <MCP_ACCESS_TOKEN>` |

Với ứng dụng khách hỗ trợ định dạng `mcpServers`, bạn có thể hợp nhất cấu hình dưới đây vào thiết lập hiện có và thay phần giữ chỗ bằng mã thông báo của mình.

```json
{
  "mcpServers": {
    "BiointronOS_MCP": {
      "url": "https://mcp-rusta-order-blgdfvompw.cn-shanghai.fcapp.run/mcp",
      "headers": {
        "Authorization": "Bearer <MCP_ACCESS_TOKEN>",
        "START_MCP_TIMEOUT_MS": "60000",
        "RUN_MCP_TIMEOUT_MS": "660000"
      }
    }
  }
}
```

Hai tiêu đề thời gian chờ là các mục tùy chỉnh trong cấu hình tham khảo: 60000 mili giây tương đương 60 giây, còn 660000 mili giây tương đương 11 phút. Chúng chỉ có tác dụng tương ứng khi ứng dụng khách hoặc dịch vụ hỗ trợ các tiêu đề này. Chỉ thêm chúng vào `headers` không bảo đảm thay đổi thời gian chờ của ứng dụng khách; hãy thiết lập cụ thể theo tài liệu của ứng dụng khách.

Xem [hướng dẫn cài đặt](../../docs/installation.md#mcp) để biết thêm chi tiết cấu hình.

### 2 · Thêm Skills

Chọn một Skill đã phát hành từ [danh mục Skills](../../skills/README.md). Tải toàn bộ thư mục, bao gồm `references/`, các tập lệnh đi kèm và những tệp được tham chiếu khác, rồi đặt vào thư mục Skill của tác nhân. Xem [cách cài đặt Skill](../../docs/installation.md#skills) cho Codex và Claude Code.

Cả hai gói Skill đã có trong kho lưu trữ và có thể tải xuống. `auto-html-report` tạo báo cáo cục bộ từ JSON kết quả đã được cung cấp, không cần thông tin xác thực hay kết nối MCP. Nếu chưa có JSON, trong phạm vi được cho phép, có thể dùng mã đơn hàng đã xác nhận và JWT hợp lệ của khách hàng hiện tại để lấy kết quả qua `get_report_results` trước, rồi tạo báo cáo. Chỉ có mã đơn hàng là chưa đủ. Biointron Account và App Key chỉ được dùng khi chưa có JWT hợp lệ; tái sử dụng thông tin đã cung cấp và chỉ hỏi phần còn thiếu. Hướng dẫn Skill bằng tiếng Anh nhưng báo cáo vẫn có thể được tạo bằng nhiều ngôn ngữ.

### 3 · Bắt đầu bằng trải nghiệm chỉ đọc

```text
Liệt kê các công cụ Biointron MCP có trong phiên này và giải thích chức năng của từng công cụ.
Cho tôi biết những khả năng nào đã sẵn sàng và những khả năng nào vẫn ở giai đoạn Beta.
Không tạo hoặc gửi đơn hàng.
```

Khám phá công cụ là bước kiểm tra kết nối đầu tiên. Một thao tác nghiệp vụ thành công đòi hỏi kết nối đến hệ thống xử lý phía sau tương ứng cũng phải được xác minh.

## Danh mục công cụ MCP

| Công cụ | Mục đích | Tác động |
| :--- | :--- | :--- |
| `get_order_input_requirements` | Mặc định thu thập các câu hỏi độc lập theo từng nhóm; trước khi ghi, kiểm tra toàn bộ dữ liệu của bước bằng `mode="validate"`. Không cần JWT nghiệp vụ. | Chỉ đọc |
| `search_order_antigens` | Tìm trong danh mục theo từ khóa, trả về sản phẩm và quy cách thực tế cùng thông tin để tải các trang tiếp theo. | Chỉ đọc |
| `order_design_preflight` | Kiểm tra điều kiện của công ty và các phép thử hiện có. | Chỉ đọc |
| `start_order_design` | Gửi tệp XLSX được cung cấp và chờ xác nhận lưu thiết kế. | Ghi dữ liệu nghiệp vụ |
| `get_order_design_result` | Khi khách hàng chọn xem, lấy và cung cấp HTML thực tế của thiết kế đã lưu bằng thao tác chỉ đọc. | Chỉ đọc |
| `add_order_to_cart` | Thêm thiết kế đã được xác nhận lưu vào giỏ hàng. | Ghi dữ liệu nghiệp vụ |
| `end_order_workflow` | Yêu cầu ứng dụng khách bỏ ngữ cảnh cục bộ, không thu hồi chữ ký hay hủy đơn hàng. | Chỉ hướng dẫn ứng dụng khách |
| `get_order_cart` | Đọc giỏ hàng đơn hàng. | Chỉ đọc |
| `calculate_order_price` | Lấy báo giá cho các đơn hàng đã chọn. | Chỉ đọc |
| `submit_verified_order` | Kiểm tra lại báo giá và gửi các đơn hàng đã chọn để được người phụ trách xác nhận. | Ghi dữ liệu nghiệp vụ |
| `get_report_results` | Lấy kết quả báo cáo đã có dưới dạng JSON. | Chỉ đọc |

Bản triển khai MCP hiện tại đăng ký 11 công cụ: 10 công cụ cần JWT nghiệp vụ của khách hàng hiện tại; `get_order_input_requirements` chạy cục bộ mà không cần JWT này. Việc triển khai và khả năng hoạt động của toàn bộ quy trình nghiệp vụ vẫn cần được xác minh. Xem [chữ ký hàm, trạng thái và giới hạn](../../docs/tool-catalog.md).

## Skills

| Skill | Mục đích | Trạng thái phát hành |
| :--- | :--- | :--- |
| [Thiết kế đơn hàng · `order-design`](../../skills/order_design/SKILL.md) | Giải thích gói dịch vụ, thu thập thông tin theo nhóm, hướng dẫn chọn sản phẩm trong danh mục, cho phép xem HTML sau khi lưu thiết kế và xử lý giỏ hàng, báo giá, gửi đơn để người phụ trách xác nhận. | Đã có · Có thể tải xuống |
| [Báo cáo kết quả · `auto-html-report`](../../skills/auto_html_report/SKILL.md) | Tạo báo cáo HTML độc lập, đa ngôn ngữ với bảng tổng hợp, biểu đồ và hình ảnh sẵn có từ JSON kết quả được cung cấp hoặc được lấy bằng truy vấn đã được cho phép. | Đã có · Có thể tải xuống |

Gửi đơn không có nghĩa là đã bắt đầu sản xuất hoặc hoàn thành thí nghiệm. Việc sản xuất chỉ bắt đầu sau khi Biointron xác nhận.

MCP cung cấp các thao tác; Skills mô tả cách tác nhân sử dụng chúng trong một tác vụ. Cài đặt Skill không cấp quyền truy cập dịch vụ và không tự động đăng ký MCP. [Xem danh mục →](../../skills/README.md)

<a id="beta"></a>

## Beta Playground

Biointron OS đang được giới thiệu dưới dạng Beta Playground. Một số kết nối có thể vẫn chưa khả dụng. Hãy báo cáo kết quả thực tế của từng bước; phản hồi HTTP thành công hoặc tên công cụ xuất hiện không chứng minh rằng thao tác nghiệp vụ đã hoàn tất.

Việc tạo và gửi đơn hàng cần được người dùng cho phép. Nếu thao tác ghi hết thời gian chờ, hãy kiểm tra trạng thái đơn hàng hiện có trước khi thử lại. Với vấn đề truy cập hoặc khả năng chưa được cung cấp, hãy liên hệ đại diện Biointron đã cấp tài khoản cho bạn.

<a id="online-platform"></a>

## Nền tảng trực tuyến Biointron

Nền tảng trực tuyến của Biointron đưa quy trình dự án RushDATA lên trình duyệt, với các mục truy cập bản nháp dự án, giỏ hàng, đơn hàng và trợ lý AI. Mở nền tảng để khám phá các dịch vụ hiện có và xem thông tin dự án.

[Truy cập nền tảng trực tuyến Biointron →](https://ai.biointron.com/#/landing)

<a href="https://ai.biointron.com/#/landing"><img src="../../assets/Biointron_Rushdata.png" alt="Giao diện dự án RushDATA trên nền tảng trực tuyến Biointron" width="1000" /></a>

<a id="faq"></a>

## Câu hỏi thường gặp

<details>
<summary><strong>Tôi có cần cả MCP và Skills không?</strong></summary>

MCP cung cấp các công cụ có thể gọi. Skills bổ sung hướng dẫn quy trình và có thể có các thành phần phụ thuộc riêng. Hãy tuân theo yêu cầu của từng Skill đã phát hành; chỉ tải Skill xuống sẽ không kết nối được dịch vụ.

</details>

<details>
<summary><strong>Công cụ xuất hiện trong danh sách có nghĩa là đã sẵn sàng sử dụng cho nghiệp vụ không?</strong></summary>

Không. Việc khám phá chỉ xác nhận công cụ đã được đăng ký. Cấu hình hệ thống phía sau, quyền truy cập tài khoản và thao tác được yêu cầu cũng cần được xác minh. Danh mục thể hiện rõ sự khác biệt này.

</details>

<details>
<summary><strong>Máy chủ và phần triển khai nghiệp vụ nằm ở đâu?</strong></summary>

Kho lưu trữ này phân phối tài liệu tích hợp công khai và Skills. Dịch vụ được lưu trữ và phần triển khai nghiệp vụ nội bộ được duy trì riêng biệt.

</details>

## Tài liệu

| Bắt đầu tại đây | Tham khảo |
| :--- | :--- |
| [Cài đặt MCP và Skills](../../docs/installation.md) | [Danh mục công cụ MCP](../../docs/tool-catalog.md) |
| [Danh mục Skills](../../skills/README.md) | [API và ví dụ JSON](../../docs/api.md) |
| [Đóng góp](../../CONTRIBUTING.md) | [Thông tin giấy phép](../../docs/license.md) |

Hướng dẫn chi tiết được cung cấp bằng tiếng Trung và tiếng Anh.

## Giấy phép

Được cấp phép theo [PolyForm Noncommercial 1.0.0](../../LICENSE). **Giấy phép này không cho phép sử dụng cho mục đích thương mại.** Mã nguồn của kho lưu trữ được cung cấp để sử dụng phi thương mại. Xem [phạm vi và điều khoản](../../docs/license.md).

---

<div align="center">
<sub>Biointron OS · Dành cho tác nhân. Dành cho mô hình. Dành cho con người.</sub>
</div>
