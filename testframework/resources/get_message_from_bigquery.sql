SELECT *
FROM `{gcp_project_id}.{dataset_name}.{table_name}`
WHERE
  ({partition_filter})
  AND ({filter})
  AND ({where})
