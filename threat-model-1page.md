# Threat Model - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: WinMilk0 - MSSV: 20230000
- Thành viên 2: TrueMilk - MSSV: 20230001

## Assets

Tài sản cần bảo vệ trong hệ thống:
1. **Plaintext**: Dữ liệu gốc cần mã hóa, được giữ trên máy Sender và Receiver
2. **AES Key**: 128 hoặc 256-bit khóa bí mật để encrypt/decrypt
3. **IV (Initialization Vector)**: 128-bit vector dùng cho CBC mode
4. **Ciphertext**: Dữ liệu đã mã hóa truyền qua mạng
5. **Log files**: Chứa key, IV, ciphertext, plaintext dưới dạng hex
6. **Network traffic**: Toàn bộ gói tin truyền qua KEY_PORT và DATA_PORT

## Attacker model

Mô tả đối tượng tấn công (Adversary):
- **Capability**: Có thể nghe lén (eavesdrop) toàn bộ traffic qua LAN hoặc WAN
- **Capability**: Có thể bắt và sửa (tamper) các gói tin giữa Sender/Receiver
- **Capability**: Có thể replay các gói tin cũ
- **Capability**: Có thể truy cập đến các log file trên hệ thống nếu chạy locally
- **Limitation**: Không thể thực hiện brute force AES key (AES-128 hoặc AES-256 đều chống brute force tốt)
- **Limitation**: Không thể hack vào Sender/Receiver để đọc plaintext trong RAM (giả định không có malware)

## Threats

Các mối đe dọa cụ thể:

**Threat 1: Key/IV Disclosure via Eavesdropping**
- **Mô tả**: Key và IV được gửi plaintext qua KEY_PORT. Kẻ tấn công nghe lén traffic có thể đọc trực tiếp key/IV từ packet
- **Impact**: Cao - Kẻ tấn công có thể decrypt toàn bộ ciphertext
- **Likelihood**: Cao - Không có encryption cho key channel

**Threat 2: Ciphertext Tampering without Detection**
- **Mô tả**: Ciphertext truyền qua DATA_PORT không có authentication tag (HMAC/MAC). Kẻ tấn công sửa một byte trong ciphertext, Receiver sẽ decrypt ra plaintext sai nhưng không biết đã bị tamper
- **Impact**: Cao - Dữ liệu bị hỏng, không phát hiện được
- **Likelihood**: Trung bình - Cần kẻ tấn công chủ động sửa gói tin

**Threat 3: Packet Replay Attack**
- **Mô tả**: Kẻ tấn công bắt được toàn bộ key packet hoặc data packet, rồi gửi lại. Receiver sẽ nhận lặp dữ liệu cũ
- **Impact**: Trung bình - Tạo confusion, có thể trigger side effect nếu message có ý nghĩa (ví dụ transfer money)
- **Likelihood**: Trung bình - Cần replay đúng thời điểm

**Threat 4: Log Leakage**
- **Mô tả**: Key, IV, plaintext được ghi vào log file có readable permission. Nếu log file accessible, key sẽ leak
- **Impact**: Cao - Toàn bộ key leak
- **Likelihood**: Cao nếu chạy locally, thấp nếu log được bảo vệ file permission

**Threat 5: No Sender/Receiver Authentication**
- **Mô tả**: Receiver không xác thực Sender - có thể tiếp nhận dữ liệu từ bất kỳ máy nào gửi đến
- **Impact**: Trung bình - Fake data hoặc data từ nguồn không tin cậy
- **Likelihood**: Trung bình - Cần kẻ tấn công biết port và địa chỉ

## Mitigations

Các biện pháp giảm thiểu rủi ro:

**Mitigation 1: Sử dụng TLS/SSL cho cả KEY_PORT và DATA_PORT**
- Thay vì gửi key plaintext, dùng TLS handshake để trao đổi key an toàn
- Tất cả traffic (key lẫn ciphertext) đều được encrypt bởi TLS

**Mitigation 2: Dùng AES-GCM thay vì AES-CBC**
- AES-GCM cung cấp Authenticated Encryption - Receiver có thể phát hiện tampering
- MAC/authentication tag được tính toán và verify

**Mitigation 3: Thêm HMAC cho Data Packet**
- Tính HMAC(key, ciphertext) rồi gửi cùng ciphertext
- Receiver tính lại HMAC để verify, phát hiện tampering ngay lập tức

**Mitigation 4: Thêm Nonce/Sequence Number**
- Mỗi packet được gán sequence number hoặc nonce
- Receiver kiểm tra sequence để phát hiện replay attack

**Mitigation 5: Chuyển key channel sang mã hóa bất đối xứng (RSA)**
- Receiver publish public key trước
- Sender encrypt key bằng receiver's public key
- Chỉ Receiver (có private key) mới decrypt được

**Mitigation 6: Không ghi plaintext/key vào log trong production**
- Ghi log có hash hoặc fingerprint thay vì plaintext
- Đảm bảo log files có restricted file permissions

**Mitigation 7: Thêm Sender Authentication (HMAC hoặc Digital Signature)**
- Sender sign message bằng private key, Receiver verify bằng public key
- Đảm bảo Receiver biết message từ Sender chứ không phải fake

## Residual risks

Các rủi ro còn lại sau khi áp dụng mitigations:

1. **Key Channel vẫn là mô phỏng**: Bài lab này chỉ mô phỏng key channel. Trong hệ thống thật, cần dùng TLS hoặc asymmetric crypto. Nếu không, key vẫn bị leak nếu bị MITM.

2. **Chưa có Perfect Forward Secrecy (PFS)**: Nếu long-term key bị compromise, toàn bộ session history có thể decrypt lại. Cần định kỳ rotate key hoặc dùng Ephemeral keys.

3. **Timing attacks**: Decrypt/unpad có thể dễ bị timing side-channel attack nếu không cẩn thận. Cần implement constant-time unpad.

4. **Crypto library vulnerabilities**: Có thể pycryptodome hoặc OS có lỗ hổng chưa được patch.

5. **Social engineering**: Người dùng có thể share log hoặc key một cách vô tình.

---

**Kết luận**: Hệ thống hiện tại hoàn toàn không an toàn cho production vì key channel gửi plaintext. Nhưng với mục đích học tập, các test case đã cover được các threat chính như tampering, wrong key, padding validation. Để làm hệ thống thật, bắt buộc phải implement Mitigation 1-3 tối thiểu.

