GIT/HUB NOTICE

Mục tiêu: đảm bảo mọi thay đổi quan trọng được đẩy lên GitHub để không bị đứt đoạn giữa các phiên.

Repo chính: https://github.com/redsonvietnam/kim-mun-dict-hub

Quy tắc nhanh:
- Trước khi kết thúc phiên, nếu bạn sửa code, scripts, dữ liệu hoặc DB, hãy commit và push.
- Nếu thay đổi ảnh hưởng DB (schema, bulk updates), tạo backup: `kim_mun_dict_v2.db.bak` và đính kèm note.
- Nếu bạn không có quyền push, tạo branch patch và nói với maintainer (issue/PR).

Ví dụ lệnh (PowerShell):

```powershell
# Cấu hình user nếu cần
git config user.name "Your Name"
git config user.email "you@example.com"

# Add, commit, push
git add -A
git commit -m "[YOUR_SHORT_DESC] Update X: ..."
git push origin main
```

Ghi chú bảo mật: KHÔNG đẩy API keys hoặc file chứa secrets lên repo. Lưu keys trong biến môi trường hoặc secret manager.

Nếu cần tạo Pull Request: tạo branch `feature/your-thing`, push branch, mở PR trên GitHub và tag `redsonvietnam` (owner).