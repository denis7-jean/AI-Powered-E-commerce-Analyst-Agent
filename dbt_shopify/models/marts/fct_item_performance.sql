SELECT
  itemid,
  COUNTIF(event = 'view') AS total_views,
  COUNTIF(event = 'addtocart') AS add_to_carts,
  COUNTIF(event = 'transaction') AS orders,
  MAX(event_time) AS last_seen
FROM {{ ref('stg_events') }}
GROUP BY itemid
ORDER BY total_views DESC
LIMIT 5000
