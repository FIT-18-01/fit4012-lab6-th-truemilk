# Report 1 page - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: WinMilk0 - MSSV: 20230000
- Thành viên 2: TrueMilk - MSSV: 20230001

## Mục tiêu

Bài lab 6 nhằm xây dựng hệ thống gửi và nhận dữ liệu được mã hóa bằng AES-CBC qua TCP socket. Cụ thể: (1) triển khai AES-CBC với PKCS#7 padding; (2) tách biệt kênh khóa (KEY_PORT) và kênh dữ liệu (DATA_PORT); (3) thiết kế header độ dài cho gói tin; (4) viết test cho các trường hợp đúng, sai, tampering và wrong key; (5) nhận diện điểm yếu bảo mật khi gửi key/IV plaintext qua mạng.

## Phân công thực hiện

- **Thành viên 1 (WinMilk0) phụ trách chính**: Triển khai Sender, encrypt/build packet functions, demo kênh khóa
- **Thành viên 2 (TrueMilk) phụ trách chính**: Triển khai Receiver, decrypt/parse packet functions, demo kênh dữ liệu
- **Phần làm chung**: Thiết kế AES-CBC utils, viết test suite, threat model, debug và documentation

## Cách làm

Nhóm triển khai hệ thống theo kiến trúc 2 kênh:
1. **Sender**: Đọc plaintext từ biến môi trường MESSAGE hoặc INPUT_FILE, dùng AES-CBC (mode CBC, PKCS#7 padding) để mã hóa, tạo key packet ([key_len:4B][key][iv]) và data packet ([ciphertext_len:4B][ciphertext]), rồi gửi qua 2 TCP connection tách biệt.
2. **Receiver**: Lắng nghe trên 2 port, nhận key packet để parse key/IV, nhận data packet để parse ciphertext, rồi decrypt bằng AES-CBC mode với unpad PKCS#7.
3. **Utils**: Cung cấp các function pad/unpad, build/parse packets, encrypt/decrypt AES-CBC, validate key/IV, recv_exact để đảm bảo dữ liệu nhận đủ từ socket.

## Kết quả

- Chương trình build, run và pass 15/16 test (chỉ thiếu file peer-review-response.md)
- Test success: sender/receiver roundtrip encrypt/decrypt đúng, padding/unpading đúng
- Test failure: tamper ciphertext -> decrypt thất bại hoặc plaintext sai, wrong key -> plaintext không khôi phục được
- Log minh chứng: sender_success.log, receiver_success.log có key/IV/ciphertext hex, plaintext được khôi phục chính xác
- Tất cả test negative đều pass

## Kết luận

Bài lab giúp nhóm hiểu rõ: (1) AES-CBC cần IV để randomize encryption, PKCS#7 padding để handle arbitrary length; (2) socket programming cần protocol rõ ràng (header độ dài) để đảm bảo dữ liệu truyền đủ; (3) bảo mật: gửi key/IV plaintext qua mạng hoàn toàn không an toàn - cần dùng mã hóa bất đối xứng (RSA) hoặc trao đổi khóa (Diffie-Hellman) để bảo vệ key/IV.
