# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Nguyễn Đức Anh
- **MSSV:** 2A202602625
- **Lớp:** K4-L3A
- **Repository URL:** https://github.com/Munfond/K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps
- **Commit SHA cuối:**
- **Challenge ID:**
- **Tên project Langfuse cá nhân:** `day13-k4-l3a-2A202602625`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | `evidence/01-pytest.png` |
| Log validator | `evidence/02-log-validator.png` |
| Dashboard validator | `evidence/03-dashboard-validator.png` |
| Structured log | `evidence/04-structured-log.png` |
| PII redaction | `evidence/05-pii-redaction.png` |
| Trace list | `evidence/06-trace-list.png` |
| Trace waterfall | `evidence/07-trace-waterfall.png` |
| Trace metadata | `evidence/08-trace-metadata.png` |
| Prompt versions | `evidence/09-prompt-versions.png` |
| Prompt rollback | `evidence/10-prompt-rollback.png` |
| Dashboard runtime | `evidence/11-dashboard-overview.png` |
| Incident metric | `evidence/12-incident-metric.png` |
| Incident log | `evidence/13-incident-log.png` |
| Incident trace | `evidence/14-incident-trace.png` |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | 30/100 (PII passed, missing schema/enrichment) | | Chưa inject correlation_id và enrichment context fields vào request/response log (bình thường ở CP0). PII scrubbing đạt chuẩn (0 leak). |
| `validate_dashboard.py` | Hợp lệ (6/6 panels) | | Đạt chuẩn dashboard contract 6 panels (latency, traffic, errors, cost, tokens, quality). |
| `pytest` | 22 passed / 22 tests (3.68s) | | Toàn bộ 22 test cases cơ sở ban đầu pass 100%. |
| Số traces hợp lệ | 10/10 traces | | Đã gửi thành công 10 query mẫu qua load_test.py và đẩy trace lên Langfuse. |
| Số PII leak | 0 leak | | Email, SĐT VN, Credit Card đã được redact thành công trong preview log. |
| Latency P95 / TTFT P95 | ~1176 ms / ~51 ms | | Request đầu cold-start 1732 ms, các request tiếp theo ~400-500 ms. TTFT ổn định ~50 ms. |
| Retrieval success rate | 100% (10/10) | | 10/10 request đều gọi retrieval tool thành công. |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** Trong `CorrelationIdMiddleware` (`app/middleware.py`), mỗi request bắt đầu bằng việc xóa context cũ qua `clear_contextvars()`. Sau đó nhận `x-request-id` từ request headers hoặc sinh ID mới theo định dạng `req-<8-hex>` (`f"req-{uuid.uuid4().hex[:8]}"`). ID được gán vào `request.state.correlation_id` và bind vào structlog context qua `bind_contextvars(correlation_id=correlation_id)`. Cuối middleware, trả lại headers `x-request-id` và `x-response-time-ms` trong HTTP response.
- **Các metadata được ghi vào structured log:** Gồm các trường schema bắt buộc và enrichment context: `ts` (ISO UTC timestamp), `level`, `service` ("api"), `event`, `correlation_id`, `user_id_hash` (hash SHA256 12 ký tự), `session_id`, `feature`, `model`, `env` ("dev"), cùng các runtime metrics (`latency_ms`, `ttft_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`, `tool_name`, `tool_success`, và `message_preview`/`answer_preview`).
- **Cách bảo đảm PII được scrub trước khi ghi:** Đăng ký processor `scrub_event` trong structlog pipeline (`app/logging_config.py`) nằm ngay trước `JsonlFileProcessor` và `JSONRenderer`. Hàm `scrub_event` duyệt và thay thế các chuỗi nhạy cảm khớp với regex trong `PII_PATTERNS` (`app/pii.py`) cho email, số điện thoại Việt Nam, CCCD 12 số, thẻ thanh toán thành các token `[REDACTED_*]` trước khi ghi xuống file `data/logs.jsonl` hoặc console.
- **Cách kiểm chứng kết quả:** Chạy script `python scripts/validate_logs.py` đạt 100/100 điểm (0 thiếu schema, 0 thiếu context, 10 correlation IDs duy nhất, 0 PII leak). Kiểm tra response headers trả về đủ `x-request-id` và `x-response-time-ms`. Chạy `pytest` đạt 24/24 tests pass bao gồm các test case cho email, SĐT VN, CCCD và thẻ tín dụng.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:**
- **Cấu trúc root/retrieval/generation observations:**
- **Cách nối trace với log:**
- **Prompt name:**
- **Version/label baseline:**
- **Version/label candidate:**
- **Trace ID của mỗi version:**
- **Cách promote và rollback `production`:**

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:**
- **SLO và lý do chọn:**
- **Cách tính error budget:**
- **Ba alert và runbook tương ứng:**

## 7. Điều tra challenge

- **Challenge ID:**
- **Khoảng thời gian điều tra:**
- **Triệu chứng từ metrics:**
- **Log line và correlation ID liên quan:**
- **Trace ID và span gây ảnh hưởng:**
- **Root cause:**
- **Fix action:**
- **Preventive measure:**

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:**
- **Một lỗi/blocker đã gặp:**
- **Cách tìm nguyên nhân và xử lý:**
- **Cách hiểu luồng Metrics → Logs → Traces:**
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**
- **Điều quan trọng nhất đã học:**
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:**

## 9. Checklist trước khi nộp

- [ ] Kết quả và evidence thuộc commit SHA cuối.
- [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ ] Repository chạy lại được theo README.
- [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
