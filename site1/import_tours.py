import os
import sys
import django
import pandas as pd
from urllib.request import urlretrieve

# Cấu hình Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site1.settings')
django.setup()

from home.models import Tour, Destination

# File Excel
excel_path = r"D:\webpython\site1\data\tour_data.xlsx"

if not os.path.exists(excel_path):
    print(f"❌ Không tìm thấy file Excel tại: {excel_path}")
    sys.exit(1)

df = pd.read_excel(excel_path)

print("🧾 CÁC CỘT CÓ TRONG FILE EXCEL:")
print(df.columns.tolist())

# Thư mục lưu ảnh
media_root = os.path.join(os.path.dirname(__file__), 'media', 'tours')
os.makedirs(media_root, exist_ok=True)

count = 0
for _, row in df.iterrows():
    try:
        dest_name = str(row['destination']).strip()
        destination, _ = Destination.objects.get_or_create(name=dest_name)

        image_url = None
        if 'image' in df.columns and pd.notna(row['image']):
            link = str(row['image']).strip()
            if link.startswith("http"):
                filename = os.path.basename(link).split("?")[0]
                local_path = os.path.join(media_root, filename)
                if not os.path.exists(local_path):
                    urlretrieve(link, local_path)
                image_url = f"tours/{filename}"

        Tour.objects.create(
            destination=destination,
            title=row.get('title', ''),
            price=row.get('price', 0),
            duration=row.get('duration', ''),
            schedule=row.get('schedule', ''),
            featured=row.get('featured', False),
            image=image_url
        )
        count += 1
    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý dòng: {row.to_dict()}")
        print(f"   ➜ {e}")

print(f"✅ Đã nhập thành công {count} tour!")
