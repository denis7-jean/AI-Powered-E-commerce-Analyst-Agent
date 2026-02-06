SELECT
  TIMESTAMP_MILLIS(CAST(timestamp AS INT64)) AS event_time,
  visitorid,
  event,
  itemid,
  transactionid
FROM {{ source('retailrocket', 'raw_events') }}
WHERE itemid IS NOT NULL
