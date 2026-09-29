# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: HighTailLatencyBreach
- Severity: Warning
- Duration: 5m
- Kênh thông báo: Slack (`#llmops-alerts`)
- SLI/SLO liên quan: Primary SLO `fast_successful_requests` (Latency P95 <= 3000ms trong 28 ngày)
- Điều kiện và thời gian duy trì: `p95(latency_ms) > 3000ms` liên tục trong 5 phút
- Ảnh hưởng tới người dùng: Người dùng chờ phản hồi chatbot lâu hơn 3 giây, tăng tỷ lệ người dùng thoát và giảm trải nghiệm hội thoại.
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard kiểm tra panel **Latency percentiles and TTFT** để xác định độ trễ tăng ở bước TTFT (LLM) hay tổng độ trễ.
  2. Lọc log `data/logs.jsonl` tìm các event `response_sent` có `latency_ms > 3000` trong 15 phút gần nhất, trích xuất `correlation_id` tương ứng.
  3. Mở trace trên Langfuse theo `correlation_id` đã tìm để xem waterfall: kiểm tra span `retrieval` (có bị incident `rag_slow` hoặc vector store nghẽn) hay observation `generation` (LLM token generation bị nghẽn).
- Mitigation tạm thời:
  - Nếu span `retrieval` bị nghẽn: kiểm tra và tắt incident `rag_slow` (hoặc bật fallback cache cho vector search).
  - Tăng timeout cho upstream service hoặc degrade sang chế độ general QA fallback.
- Owner: `@oncall-sre`

## Alert 2

- Tên: HighErrorRateAndRetrievalFailure
- Severity: Critical
- Duration: 3m
- Kênh thông báo: Slack (`#llmops-incident`)
- SLI/SLO liên quan: Guardrails `error_rate_pct_max: 2%` và `retrieval_success_rate_pct_min: 90%`
- Điều kiện và thời gian duy trì: `error_rate_pct > 2.0%` hoặc `retrieval_success_rate_pct < 90.0%` duy trì trong 3 phút
- Ảnh hưởng tới người dùng: Người dùng nhận thông báo lỗi HTTP 500 hoặc câu trả lời không có ngữ cảnh tra cứu, dịch vụ gián đoạn diện rộng.
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard panel **Error rate and retrieval success** để xem biểu đồ lỗi và breakdown theo `error_type` (`RuntimeError`, `Timeout`, v.v.).
  2. Tìm trong log các event `request_failed`, ghi nhận `error_type`, correlation ID và payload `detail`.
  3. Vào Langfuse tìm các trace có gắn cờ ERROR hoặc observation `retrieval` bị fail, kiểm tra xem có incident `tool_fail` hay vector store ngừng hoạt động.
- Mitigation tạm thời:
  - Tắt incident lỗi nếu đang diễn ra (`/incidents/tool_fail/disable`).
  - Kích hoạt cơ chế Fallback Document/Rule-based answering để bot không trả lỗi 500 về phía client.
  - Khởi động lại service hoặc chuyển traffic sang cluster dự phòng.
- Owner: `@oncall-backend`

## Alert 3

- Tên: TokenCostSpikeAnomaly
- Severity: Warning
- Duration: 10m
- Kênh thông báo: Slack (`#llmops-finops`)
- SLI/SLO liên quan: Guardrail `daily_cost_usd_max: 2.50 USD` và token panel threshold
- Điều kiện và thời gian duy trì: Tổng `cost_usd` vượt 2.50 USD trong cửa sổ theo dõi hoặc `avg(tokens_out) > 400` trong 10 phút
- Ảnh hưởng tới người dùng: Không ảnh hưởng trực tiếp tới UI nhưng tiêu hao ngân sách API của dự án với tốc độ bất thường, có nguy cơ cạn quota API key dẫn tới ngắt dịch vụ.
- Ba bước kiểm tra đầu tiên:
  1. Mở panel **Cost over time** và **Input and output tokens** để xác định chi phí tăng do số lượng request (traffic) hay do số output token mỗi request tăng đột biến.
  2. Lọc log `response_sent` có `tokens_out > 300` hoặc `cost_usd` cao bất thường, lấy `user_id_hash`, `prompt_version`, và `correlation_id`.
  3. Mở trace trên Langfuse để xem prompt template đang dùng có bị prompt injection/loop sinh text vô tận hoặc có incident `cost_spike` được kích hoạt.
- Mitigation tạm thời:
  - Nếu do prompt candidate mới bị verbose: thực hiện rollback label `production` về version prompt trước đó trên Langfuse.
  - Tắt incident `cost_spike` nếu đang test (`/incidents/cost_spike/disable`).
  - Áp dụng max_tokens limit chặt hơn trong tham số gọi LLM.
- Owner: `@llmops-finops`

