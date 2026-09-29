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

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Traces được kết nối và gửi trực tiếp về project Langfuse cá nhân `day13-k4-l3a-2A202602625` (Project ID: `cmumcljev12xkad0c44gkvpfr`) thông qua cặp API keys cá nhân `LANGFUSE_PUBLIC_KEY` và `LANGFUSE_SECRET_KEY`. Mỗi trace chứa user_id băm (`user_id_hash`), `session_id`, `environment: dev`, tags `["lab", feature, model]` và metadata mang mã `correlation_id` tương ứng với request chạy trên máy cục bộ.
- **Cấu trúc root/retrieval/generation observations:**
  - **Root observation (`lab-agent-run`, type: `agent`):** Đại diện cho toàn bộ luồng xử lý `LabAgent.run`, chứa thông tin user hash, correlation_id, model, feature, tags và kết quả tổng thể.
  - **Child observation 1 (`retrieval`, type: `retriever`):** Gắn với bước tra cứu ngữ cảnh `retrieve(message)`, đo thời gian tra cứu vector store và ghi metadata số tài liệu tìm thấy (`doc_count`).
  - **Child observation 2 (`generation`, type: `generation`):** Gắn với bước sinh token của `FakeLLM.generate(prompt)`, ghi nhận model (`claude-sonnet-4-5`), prompt template từ Langfuse, chi tiết số token (`usage_details`: `input`, `output`, `total`) và chi phí ước tính (`cost_details`: `total_cost`).
  Cấu trúc phân cấp cha–con này cho phép biểu đồ waterfall phân tách rõ ràng thời gian của bước retrieval và generation, dễ dàng khoanh vùng bước nào bị chậm khi có sự cố.
- **Cách nối trace với log:** Thông qua `correlation_id` (ví dụ `req-79cccbe5`). Trong log file `data/logs.jsonl`, mỗi request/response đều có `correlation_id`. Trên Langfuse, metadata của trace root và các span đều được inject `correlation_id: correlation_id`. Từ log entry bất thường có thể tra cứu ngay trace trên Langfuse, và ngược lại.
- **Prompt name:** `day13-chat`
- **Version/label baseline:** Version 1, mang labels `baseline` và `production` (template: `Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}`).
- **Version/label candidate:** Version 2, mang label `candidate` (bổ sung chỉ dẫn: `\nAnswer concisely in 1-2 sentences.`).
- **Trace ID của mỗi version:**
  - Baseline (v1, label `baseline`): `e4d5d49b2b1074565b9b559bd5c984c0` (hoặc các trace load test v1: `519f596ca5a1ed6dfaef8ad6fa627812`, `9b0a8cfd5ef88fcb79d700ef36ef9fb5`)
  - Candidate (v2, label `candidate`): `a4b72a5b8164e0b1474d6a6ca6fc67b6`
  - Promoted v2 trên production: `8b2b34c7661429a534edf5608c8ec95a`
  - Rollback v1 trên production: `294226830699b9f602cd4fe95258928d`
- **Cách promote và rollback `production`:** Sử dụng API / SDK Langfuse `client.update_prompt(name="day13-chat", version=2, new_labels=["candidate", "production"])` để gắn nhãn `production` cho version 2; và khi cần rollback thì thực thi `client.update_prompt(name="day13-chat", version=1, new_labels=["baseline", "production"])` đưa nhãn `production` quay về version 1 một cách an toàn mà không cần thay đổi source code hay rebuild ứng dụng.

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** Dựng đúng theo đặc tả contract `config/dashboard.yaml` với nguồn dữ liệu từ `data/logs.jsonl`, time range 60 phút, tự động làm mới mỗi 30 giây:
  1. `Latency percentiles and TTFT` (P50, P95, P99 và TTFT P95, đơn vị ms; Threshold: P95 &le; 3000 ms).
  2. `Request traffic` (Tổng số request và tốc độ request/phút; Threshold: &ge; 1 req/min).
  3. `Error rate and retrieval success` (Tỷ lệ lỗi %, phân loại theo error_type và tỷ lệ retrieval thành công %; Threshold: Error &le; 2%, Success &ge; 90%).
  4. `Cost over time` (Tổng chi phí tích lũy và theo phút, đơn vị USD; Threshold: &le; $2.50 USD).
  5. `Input and output tokens` (Tổng tokens in và tokens out, đơn vị tokens; Threshold: &le; 50,000 tokens).
  6. `Quality proxy` (Điểm chất lượng trung bình từ 0.00 đến 1.00; Threshold: Mean &ge; 0.75).
- **SLO và lý do chọn:** Chọn Primary SLO `fast_successful_requests` với mục tiêu **99.5%** trong chu kỳ đánh giá **28 ngày**.
  - SLI: `Tỷ lệ request có event == "response_sent" và latency_ms <= 3000ms / Tổng request_received`.
  - Lý do chọn: Trong điều kiện bình thường (baseline), độ trễ P95 đạt ~400–500ms. Ngưỡng 3000ms được chọn làm ranh giới chấp nhận của người dùng đối với một ứng dụng chatbot tương tác (nếu quá 3s người dùng thường sẽ refresh hoặc bỏ phiên). Mức 99.5% phản ánh chất lượng dịch vụ cao, chỉ cho phép 0.5% lỗi hoặc phản hồi chậm.
- **Cách tính error budget:**
  - Tỷ lệ Error Budget = $100\% - 99.5\% = 0.5\%$.
  - Nếu hệ thống nhận 100,000 requests trong cửa sổ 28 ngày:
    $\text{Error Budget} = 100,000 \times 0.5\% = 500 \text{ requests được phép lỗi hoặc trễ > 3000ms}$.
  - Tốc độ tiêu hao (Burn Rate) = $\frac{\text{Tỷ lệ lỗi thực tế}}{0.5\%}$. Khi Burn Rate > 1, ngân sách lỗi sẽ cạn trước chu kỳ 28 ngày, kích hoạt việc đóng băng release tính năng mới để tập trung cải thiện hiệu năng.
- **Ba alert và runbook tương ứng:**
  1. `HighTailLatencyBreach` (Warning | 5m | `#llmops-alerts` | `@oncall-sre`): Kích hoạt khi `p95(latency_ms) > 3000` liên tục trong 5 phút. Runbook: [docs/alerts.md#alert-1](file:///c:/Users/nguye/K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps/docs/alerts.md#alert-1).
  2. `HighErrorRateAndRetrievalFailure` (Critical | 3m | `#llmops-incident` | `@oncall-backend`): Kích hoạt khi `error_rate_pct > 2.0%` hoặc `retrieval_success_rate_pct < 90.0%` duy trì trong 3 phút. Runbook: [docs/alerts.md#alert-2](file:///c:/Users/nguye/K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps/docs/alerts.md#alert-2).
  3. `TokenCostSpikeAnomaly` (Warning | 10m | `#llmops-finops` | `@llmops-finops`): Kích hoạt khi tổng chi phí vượt $2.50 USD hoặc trung bình output token vượt 400 token/request kéo dài 10 phút. Runbook: [docs/alerts.md#alert-3](file:///c:/Users/nguye/K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps/docs/alerts.md#alert-3).

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
