import os

# 定义干净的文件内容 (UTF-8 No-BOM)
files = {
    "dbt_shopify/models/staging/sources.yml": """version: 2
sources:
  - name: retailrocket
    database: shopify-mvp-2026
    schema: shopify_mvp
    tables:
      - name: raw_events
      - name: raw_item_properties
""",
    "dbt_shopify/models/staging/stg_events.sql": """SELECT
  TIMESTAMP_MILLIS(CAST(timestamp AS INT64)) AS event_time,
  visitorid,
  event,
  itemid,
  transactionid
FROM {{ source('retailrocket', 'raw_events') }}
WHERE itemid IS NOT NULL
""",
    "dbt_shopify/models/marts/fct_item_performance.sql": """SELECT
  itemid,
  COUNTIF(event = 'view') AS total_views,
  COUNTIF(event = 'addtocart') AS add_to_carts,
  COUNTIF(event = 'transaction') AS orders,
  MAX(event_time) AS last_seen
FROM {{ ref('stg_events') }}
GROUP BY itemid
ORDER BY total_views DESC
LIMIT 5000
"""
}

# 循环写入文件
for path, content in files.items():
    # 确保目录存在
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # 强制以 UTF-8 (无 BOM) 格式写入
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Fixed: {path}")