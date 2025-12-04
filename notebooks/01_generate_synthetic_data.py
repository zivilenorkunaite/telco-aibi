# Databricks notebook source
# MAGIC %md
# MAGIC # 🔧 SouthernLink Networks - Synthetic Data Generator
# MAGIC
# MAGIC This notebook generates synthetic data for the Databricks AI/BI demo showcasing network intelligence capabilities.
# MAGIC
# MAGIC **Catalog:** `zivile`  
# MAGIC **Schema:** `telco`
# MAGIC
# MAGIC ### Tables Created:
# MAGIC 1. `poi_infrastructure` - Points of Interconnect (network nodes)
# MAGIC 2. `premises` - Customer premises/locations
# MAGIC 3. `customers` - Customer accounts and plans
# MAGIC 4. `network_telemetry` - Real-time network performance metrics
# MAGIC 5. `incidents` - Network incidents and outages
# MAGIC 6. `customer_usage` - Daily customer usage patterns
# MAGIC 7. `capacity_forecasts` - ML-generated capacity predictions

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup & Configuration

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lit, rand, randn, expr, when, concat, lpad,
    date_add, date_sub, current_date, current_timestamp,
    hour, dayofweek, month, year, floor, ceil, abs as spark_abs,
    array, explode, sequence, to_date, to_timestamp,
    monotonically_increasing_id, sha2, substring, upper,
    round as spark_round, greatest, least
)
from pyspark.sql.types import *
import random

# Configuration
CATALOG = "zivile"
SCHEMA = "telco"

# Set the catalog and schema
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print(f"✅ Using catalog: {CATALOG}, schema: {SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1️⃣ POI Infrastructure (Points of Interconnect)
# MAGIC
# MAGIC Network nodes that serve as aggregation points for customer connections.

# COMMAND ----------

# Australian states and major cities/suburbs
locations_data = [
    # NSW
    ("NSW", "Sydney", "Sydney CBD", -33.8688, 151.2093, "FTTP", 45000),
    ("NSW", "Sydney", "Parramatta", -33.8151, 151.0011, "FTTN", 38000),
    ("NSW", "Sydney", "Western Sydney", -33.8330, 150.8500, "FTTN", 52000),
    ("NSW", "Sydney", "North Sydney", -33.8397, 151.2065, "FTTP", 28000),
    ("NSW", "Sydney", "Blacktown", -33.7690, 150.9063, "FTTN", 48000),
    ("NSW", "Sydney", "Liverpool", -33.9200, 150.9256, "HFC", 35000),
    ("NSW", "Sydney", "Penrith", -33.7507, 150.6876, "FTTN", 32000),
    ("NSW", "Newcastle", "Newcastle", -32.9283, 151.7817, "FTTP", 29000),
    ("NSW", "Wollongong", "Wollongong", -34.4250, 150.8931, "HFC", 24000),
    
    # VIC
    ("VIC", "Melbourne", "Melbourne CBD", -37.8136, 144.9631, "FTTP", 42000),
    ("VIC", "Melbourne", "Werribee", -37.9000, 144.6667, "FTTN", 55000),
    ("VIC", "Melbourne", "Cranbourne", -38.0996, 145.2834, "FTTN", 49000),
    ("VIC", "Melbourne", "Point Cook", -37.9167, 144.7500, "FTTN", 44000),
    ("VIC", "Melbourne", "Tarneit", -37.8333, 144.6500, "FTTP", 51000),
    ("VIC", "Melbourne", "Epping", -37.6500, 145.0333, "HFC", 38000),
    ("VIC", "Melbourne", "Dandenong", -37.9875, 145.2153, "FTTN", 36000),
    ("VIC", "Melbourne", "Frankston", -38.1433, 145.1228, "HFC", 31000),
    ("VIC", "Geelong", "Geelong", -38.1499, 144.3617, "FTTP", 27000),
    
    # QLD
    ("QLD", "Brisbane", "Brisbane CBD", -27.4705, 153.0260, "FTTP", 39000),
    ("QLD", "Brisbane", "Gold Coast", -28.0167, 153.4000, "HFC", 46000),
    ("QLD", "Brisbane", "Ipswich", -27.6167, 152.7667, "FTTN", 33000),
    ("QLD", "Brisbane", "Logan", -27.6394, 153.1094, "FTTN", 41000),
    ("QLD", "Brisbane", "Sunshine Coast", -26.6500, 153.0667, "HFC", 35000),
    ("QLD", "Cairns", "Cairns", -16.9186, 145.7781, "FTTN", 22000),
    ("QLD", "Townsville", "Townsville", -19.2590, 146.8169, "FTTN", 19000),
    
    # WA
    ("WA", "Perth", "Perth CBD", -31.9505, 115.8605, "FTTP", 36000),
    ("WA", "Perth", "Joondalup", -31.7453, 115.7663, "FTTN", 34000),
    ("WA", "Perth", "Rockingham", -32.2833, 115.7333, "HFC", 29000),
    ("WA", "Perth", "Mandurah", -32.5269, 115.7217, "FTTN", 26000),
    
    # SA
    ("SA", "Adelaide", "Adelaide CBD", -34.9285, 138.6007, "FTTP", 31000),
    ("SA", "Adelaide", "Elizabeth", -34.7167, 138.6667, "FTTN", 28000),
    ("SA", "Adelaide", "Salisbury", -34.7667, 138.6333, "FTTN", 25000),
    
    # TAS
    ("TAS", "Hobart", "Hobart", -42.8821, 147.3272, "FTTP", 18000),
    ("TAS", "Launceston", "Launceston", -41.4332, 147.1441, "FTTN", 14000),
    
    # NT
    ("NT", "Darwin", "Darwin", -12.4634, 130.8456, "Fixed Wireless", 12000),
    ("NT", "Alice Springs", "Alice Springs", -23.6980, 133.8807, "Fixed Wireless", 6000),
    
    # ACT
    ("ACT", "Canberra", "Canberra", -35.2809, 149.1300, "FTTP", 28000),
    ("ACT", "Canberra", "Belconnen", -35.2388, 149.0667, "FTTP", 24000),
]

# Create POI DataFrame
poi_schema = StructType([
    StructField("state", StringType(), False),
    StructField("city", StringType(), False),
    StructField("suburb", StringType(), False),
    StructField("latitude", DoubleType(), False),
    StructField("longitude", DoubleType(), False),
    StructField("technology_type", StringType(), False),
    StructField("premises_served", IntegerType(), False),
])

poi_df = spark.createDataFrame(locations_data, poi_schema)

# Add additional columns
poi_df = poi_df.withColumn("poi_id", concat(
    upper(col("state")),
    lit("-"),
    lpad(monotonically_increasing_id().cast("string"), 4, "0")
)) \
.withColumn("max_capacity_gbps", 
    when(col("technology_type") == "FTTP", lit(100))
    .when(col("technology_type") == "HFC", lit(50))
    .when(col("technology_type") == "FTTN", lit(25))
    .otherwise(lit(10))
) \
.withColumn("install_date", 
    date_sub(current_date(), (rand() * 2000 + 500).cast("int"))
) \
.withColumn("last_upgrade_date",
    date_sub(current_date(), (rand() * 365).cast("int"))
)

# Reorder columns
poi_df = poi_df.select(
    "poi_id", "state", "city", "suburb", "latitude", "longitude",
    "technology_type", "premises_served", "max_capacity_gbps",
    "install_date", "last_upgrade_date"
)

# Save to table
poi_df.write.mode("overwrite").saveAsTable("poi_infrastructure")
print(f"✅ Created poi_infrastructure table with {poi_df.count()} POIs")
display(poi_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2️⃣ Premises (Customer Locations)
# MAGIC
# MAGIC Physical addresses that can be connected to the network.

# COMMAND ----------

# Read POI data to distribute premises
poi_data = spark.table("poi_infrastructure")

# Generate premises for each POI
premises_df = poi_data.select(
    col("poi_id"),
    col("suburb"),
    col("state"),
    col("technology_type"),
    col("premises_served"),
    col("latitude").alias("poi_lat"),
    col("longitude").alias("poi_lon")
) \
.withColumn("premise_count", col("premises_served")) \
.withColumn("premise_idx", explode(sequence(lit(1), (col("premise_count") / 100).cast("int")))) \
.withColumn("premise_id", concat(
    col("poi_id"),
    lit("-P"),
    lpad(col("premise_idx").cast("string"), 5, "0")
)) \
.withColumn("latitude", col("poi_lat") + (rand() - 0.5) * 0.05) \
.withColumn("longitude", col("poi_lon") + (rand() - 0.5) * 0.05) \
.withColumn("address_number", (rand() * 500 + 1).cast("int")) \
.withColumn("street_name", concat(
    when(rand() < 0.2, lit("Main"))
    .when(rand() < 0.4, lit("High"))
    .when(rand() < 0.6, lit("Station"))
    .when(rand() < 0.8, lit("Park"))
    .otherwise(lit("Victoria")),
    when(rand() < 0.5, lit(" Street")).otherwise(lit(" Road"))
)) \
.withColumn("address", concat(
    col("address_number").cast("string"),
    lit(" "),
    col("street_name"),
    lit(", "),
    col("suburb"),
    lit(" "),
    col("state")
)) \
.withColumn("premise_type",
    when(rand() < 0.7, lit("Residential"))
    .when(rand() < 0.9, lit("Business"))
    .otherwise(lit("Enterprise"))
) \
.withColumn("is_connected", rand() < 0.85) \
.withColumn("connection_date",
    when(col("is_connected"), date_sub(current_date(), (rand() * 1500 + 30).cast("int")))
)

premises_df = premises_df.select(
    "premise_id", "poi_id", "address", "suburb", "state",
    "latitude", "longitude", "technology_type", "premise_type",
    "is_connected", "connection_date"
)

premises_df.write.mode("overwrite").saveAsTable("premises")
print(f"✅ Created premises table with {premises_df.count()} premises")
display(premises_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3️⃣ Customers (Account & Plan Information)
# MAGIC
# MAGIC Customer accounts with their selected plans and service details.

# COMMAND ----------

# Get connected premises
connected_premises = spark.table("premises").filter(col("is_connected") == True)

# Define plans based on technology
plans = [
    ("Basic 25", 25, 5, 49.99),
    ("Standard 50", 50, 20, 69.99),
    ("Standard Plus 100", 100, 20, 89.99),
    ("Premium 250", 250, 25, 109.99),
    ("Ultrafast 500", 500, 50, 129.99),
    ("Ultrafast 1000", 1000, 50, 149.99),
    ("Business 100", 100, 40, 119.99),
    ("Business 250", 250, 100, 179.99),
    ("Enterprise 1000", 1000, 400, 299.99),
]

customers_df = connected_premises.select(
    col("premise_id"),
    col("poi_id"),
    col("technology_type"),
    col("premise_type"),
    col("connection_date").alias("account_created_date")
) \
.withColumn("customer_id", concat(lit("CUST-"), substring(sha2(col("premise_id"), 256), 1, 10))) \
.withColumn("plan_tier",
    when(col("premise_type") == "Enterprise", 
         when(rand() < 0.5, lit("Enterprise 1000")).otherwise(lit("Business 250")))
    .when(col("premise_type") == "Business",
         when(rand() < 0.3, lit("Business 100"))
         .when(rand() < 0.6, lit("Business 250"))
         .otherwise(lit("Premium 250")))
    .otherwise(
        when(rand() < 0.15, lit("Basic 25"))
        .when(rand() < 0.35, lit("Standard 50"))
        .when(rand() < 0.60, lit("Standard Plus 100"))
        .when(rand() < 0.80, lit("Premium 250"))
        .when(rand() < 0.95, lit("Ultrafast 500"))
        .otherwise(lit("Ultrafast 1000"))
    )
) \
.withColumn("download_speed_mbps",
    when(col("plan_tier") == "Basic 25", lit(25))
    .when(col("plan_tier") == "Standard 50", lit(50))
    .when(col("plan_tier") == "Standard Plus 100", lit(100))
    .when(col("plan_tier") == "Premium 250", lit(250))
    .when(col("plan_tier") == "Ultrafast 500", lit(500))
    .when(col("plan_tier") == "Ultrafast 1000", lit(1000))
    .when(col("plan_tier") == "Business 100", lit(100))
    .when(col("plan_tier") == "Business 250", lit(250))
    .when(col("plan_tier") == "Enterprise 1000", lit(1000))
) \
.withColumn("upload_speed_mbps",
    when(col("plan_tier") == "Basic 25", lit(5))
    .when(col("plan_tier") == "Standard 50", lit(20))
    .when(col("plan_tier") == "Standard Plus 100", lit(20))
    .when(col("plan_tier") == "Premium 250", lit(25))
    .when(col("plan_tier") == "Ultrafast 500", lit(50))
    .when(col("plan_tier") == "Ultrafast 1000", lit(50))
    .when(col("plan_tier") == "Business 100", lit(40))
    .when(col("plan_tier") == "Business 250", lit(100))
    .when(col("plan_tier") == "Enterprise 1000", lit(400))
) \
.withColumn("monthly_price",
    when(col("plan_tier") == "Basic 25", lit(49.99))
    .when(col("plan_tier") == "Standard 50", lit(69.99))
    .when(col("plan_tier") == "Standard Plus 100", lit(89.99))
    .when(col("plan_tier") == "Premium 250", lit(109.99))
    .when(col("plan_tier") == "Ultrafast 500", lit(129.99))
    .when(col("plan_tier") == "Ultrafast 1000", lit(149.99))
    .when(col("plan_tier") == "Business 100", lit(119.99))
    .when(col("plan_tier") == "Business 250", lit(179.99))
    .when(col("plan_tier") == "Enterprise 1000", lit(299.99))
) \
.withColumn("contract_end_date", 
    date_add(col("account_created_date"), (rand() * 365 + 365).cast("int"))
) \
.withColumn("is_active", rand() < 0.95) \
.withColumn("churn_risk_score", 
    when(col("is_active") == False, lit(1.0))
    .otherwise(spark_round(rand() * 0.6, 2))
)

customers_df = customers_df.select(
    "customer_id", "premise_id", "poi_id", "technology_type", "premise_type",
    "plan_tier", "download_speed_mbps", "upload_speed_mbps", "monthly_price",
    "account_created_date", "contract_end_date", "is_active", "churn_risk_score"
)

customers_df.write.mode("overwrite").saveAsTable("customers")
print(f"✅ Created customers table with {customers_df.count()} customers")
display(customers_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4️⃣ Network Telemetry (Real-time Performance Data)
# MAGIC
# MAGIC Network performance metrics collected from POIs - last 30 days of hourly data.

# COMMAND ----------

# Generate 30 days of hourly telemetry data for each POI
poi_data = spark.table("poi_infrastructure")

# Create date range - last 30 days, hourly
telemetry_base = poi_data.select(
    "poi_id", "technology_type", "max_capacity_gbps", "premises_served", "suburb", "state"
) \
.crossJoin(
    spark.range(0, 30 * 24).toDF("hour_offset")
) \
.withColumn("timestamp", 
    expr("current_timestamp() - interval '1' hour * hour_offset")
) \
.withColumn("date", to_date(col("timestamp"))) \
.withColumn("hour", hour(col("timestamp"))) \
.withColumn("day_of_week", dayofweek(col("timestamp")))

# Calculate realistic utilization patterns
# Peak hours: 6-9 PM (18-21), higher on weekdays
# Technology affects baseline utilization
telemetry_df = telemetry_base \
.withColumn("base_utilization",
    when(col("technology_type") == "FTTN", 0.55 + rand() * 0.15)
    .when(col("technology_type") == "HFC", 0.45 + rand() * 0.15)
    .when(col("technology_type") == "FTTP", 0.35 + rand() * 0.15)
    .otherwise(0.40 + rand() * 0.15)
) \
.withColumn("peak_multiplier",
    when((col("hour") >= 18) & (col("hour") <= 21), 1.4 + rand() * 0.2)
    .when((col("hour") >= 12) & (col("hour") <= 14), 1.15 + rand() * 0.1)
    .when((col("hour") >= 9) & (col("hour") <= 17), 1.1 + rand() * 0.1)
    .when((col("hour") >= 6) & (col("hour") <= 8), 1.2 + rand() * 0.1)
    .otherwise(0.6 + rand() * 0.2)
) \
.withColumn("weekend_factor",
    when(col("day_of_week").isin([1, 7]), 0.85 + rand() * 0.1)
    .otherwise(1.0)
) \
.withColumn("utilization_pct", 
    least(
        lit(0.98),
        greatest(
            lit(0.15),
            col("base_utilization") * col("peak_multiplier") * col("weekend_factor") + (rand() - 0.5) * 0.1
        )
    )
) \
.withColumn("current_throughput_gbps", 
    spark_round(col("max_capacity_gbps") * col("utilization_pct"), 2)
) \
.withColumn("active_connections", 
    (col("premises_served") * col("utilization_pct") * (0.3 + rand() * 0.2)).cast("int")
) \
.withColumn("avg_latency_ms",
    when(col("utilization_pct") > 0.85, 25 + rand() * 30)
    .when(col("utilization_pct") > 0.7, 15 + rand() * 15)
    .otherwise(8 + rand() * 10)
) \
.withColumn("packet_loss_pct",
    when(col("utilization_pct") > 0.9, 0.5 + rand() * 1.5)
    .when(col("utilization_pct") > 0.8, 0.1 + rand() * 0.4)
    .otherwise(rand() * 0.1)
) \
.withColumn("congestion_status",
    when(col("utilization_pct") > 0.85, lit("Critical"))
    .when(col("utilization_pct") > 0.70, lit("Warning"))
    .otherwise(lit("Normal"))
) \
.withColumn("avg_download_speed_pct",
    when(col("utilization_pct") > 0.9, 0.5 + rand() * 0.2)
    .when(col("utilization_pct") > 0.8, 0.65 + rand() * 0.15)
    .when(col("utilization_pct") > 0.7, 0.75 + rand() * 0.15)
    .otherwise(0.85 + rand() * 0.15)
)

telemetry_df = telemetry_df.select(
    "poi_id", "suburb", "state", "technology_type", "timestamp", "date", "hour", "day_of_week",
    spark_round(col("utilization_pct") * 100, 1).alias("utilization_pct"),
    "current_throughput_gbps", "max_capacity_gbps", "active_connections",
    spark_round(col("avg_latency_ms"), 1).alias("avg_latency_ms"),
    spark_round(col("packet_loss_pct"), 3).alias("packet_loss_pct"),
    "congestion_status",
    spark_round(col("avg_download_speed_pct") * 100, 1).alias("avg_download_speed_pct")
)

telemetry_df.write.mode("overwrite").saveAsTable("network_telemetry")
print(f"✅ Created network_telemetry table with {telemetry_df.count()} records")
display(telemetry_df.orderBy(col("timestamp").desc()).limit(50))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5️⃣ Incidents (Network Issues & Outages)
# MAGIC
# MAGIC Historical record of network incidents, outages, and maintenance events.

# COMMAND ----------

# Generate incidents over the past 12 months
poi_data = spark.table("poi_infrastructure")

# Create base incidents - about 2-5 per POI over 12 months
incidents_base = poi_data.select("poi_id", "suburb", "state", "technology_type") \
    .crossJoin(spark.range(1, 6).toDF("incident_num")) \
    .filter(rand() < 0.7)  # ~70% chance for each incident

incident_types = [
    ("Hardware Failure", "Critical", 2, 24),
    ("Fiber Cut", "Critical", 4, 48),
    ("Power Outage", "High", 1, 8),
    ("Capacity Exceeded", "Medium", 0.5, 4),
    ("Configuration Error", "Medium", 0.5, 2),
    ("Weather Damage", "High", 2, 12),
    ("Planned Maintenance", "Low", 2, 6),
    ("DDoS Attack", "Critical", 1, 4),
    ("Software Bug", "Medium", 0.5, 3),
]

incidents_df = incidents_base \
.withColumn("incident_id", concat(
    lit("INC-"),
    substring(sha2(concat(col("poi_id"), col("incident_num").cast("string")), 256), 1, 8)
)) \
.withColumn("incident_date", 
    date_sub(current_date(), (rand() * 365).cast("int"))
) \
.withColumn("incident_time",
    to_timestamp(concat(
        col("incident_date").cast("string"),
        lit(" "),
        lpad((rand() * 24).cast("int").cast("string"), 2, "0"),
        lit(":"),
        lpad((rand() * 60).cast("int").cast("string"), 2, "0"),
        lit(":00")
    ))
) \
.withColumn("rand_type", rand()) \
.withColumn("incident_type",
    when(col("rand_type") < 0.15, lit("Hardware Failure"))
    .when(col("rand_type") < 0.25, lit("Fiber Cut"))
    .when(col("rand_type") < 0.40, lit("Power Outage"))
    .when(col("rand_type") < 0.55, lit("Capacity Exceeded"))
    .when(col("rand_type") < 0.65, lit("Configuration Error"))
    .when(col("rand_type") < 0.75, lit("Weather Damage"))
    .when(col("rand_type") < 0.90, lit("Planned Maintenance"))
    .when(col("rand_type") < 0.95, lit("DDoS Attack"))
    .otherwise(lit("Software Bug"))
) \
.withColumn("severity",
    when(col("incident_type").isin("Hardware Failure", "Fiber Cut", "DDoS Attack"), lit("Critical"))
    .when(col("incident_type").isin("Power Outage", "Weather Damage"), lit("High"))
    .when(col("incident_type").isin("Capacity Exceeded", "Configuration Error", "Software Bug"), lit("Medium"))
    .otherwise(lit("Low"))
) \
.withColumn("duration_hours",
    when(col("incident_type") == "Hardware Failure", 2 + rand() * 22)
    .when(col("incident_type") == "Fiber Cut", 4 + rand() * 44)
    .when(col("incident_type") == "Power Outage", 1 + rand() * 7)
    .when(col("incident_type") == "Capacity Exceeded", 0.5 + rand() * 3.5)
    .when(col("incident_type") == "Configuration Error", 0.5 + rand() * 1.5)
    .when(col("incident_type") == "Weather Damage", 2 + rand() * 10)
    .when(col("incident_type") == "Planned Maintenance", 2 + rand() * 4)
    .when(col("incident_type") == "DDoS Attack", 1 + rand() * 3)
    .otherwise(0.5 + rand() * 2.5)
) \
.withColumn("customers_affected",
    (rand() * 5000 + 500).cast("int")
) \
.withColumn("resolution_time",
    expr("incident_time + interval '1' minute * cast(duration_hours as int)")
) \
.withColumn("root_cause",
    when(col("incident_type") == "Hardware Failure", lit("Faulty network equipment requiring replacement"))
    .when(col("incident_type") == "Fiber Cut", lit("Third-party excavation damage to fiber cable"))
    .when(col("incident_type") == "Power Outage", lit("Upstream power grid failure"))
    .when(col("incident_type") == "Capacity Exceeded", lit("Unexpected traffic surge during peak hours"))
    .when(col("incident_type") == "Configuration Error", lit("Incorrect routing table update"))
    .when(col("incident_type") == "Weather Damage", lit("Storm damage to above-ground infrastructure"))
    .when(col("incident_type") == "Planned Maintenance", lit("Scheduled equipment upgrade"))
    .when(col("incident_type") == "DDoS Attack", lit("Distributed denial of service attack mitigated"))
    .otherwise(lit("Software bug in network management system"))
) \
.withColumn("status",
    when(col("incident_date") > date_sub(current_date(), 2), 
         when(rand() < 0.3, lit("Open")).otherwise(lit("Resolved")))
    .otherwise(lit("Resolved"))
)

incidents_df = incidents_df.select(
    "incident_id", "poi_id", "suburb", "state", "technology_type",
    "incident_type", "severity", "incident_time", 
    spark_round(col("duration_hours"), 1).alias("duration_hours"),
    "resolution_time", "customers_affected", "root_cause", "status"
)

incidents_df.write.mode("overwrite").saveAsTable("incidents")
print(f"✅ Created incidents table with {incidents_df.count()} incidents")
display(incidents_df.orderBy(col("incident_time").desc()).limit(30))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6️⃣ Customer Usage (Daily Usage Patterns)
# MAGIC
# MAGIC Daily aggregated usage data per customer for the last 90 days.

# COMMAND ----------

# Get sample of customers (limit for performance)
customers_sample = spark.table("customers") \
    .filter(col("is_active") == True) \
    .sample(fraction=0.3, seed=42)

# Generate 90 days of usage data
usage_df = customers_sample.select(
    "customer_id", "poi_id", "download_speed_mbps", "upload_speed_mbps", 
    "plan_tier", "technology_type"
) \
.crossJoin(
    spark.range(0, 90).toDF("day_offset")
) \
.withColumn("usage_date", date_sub(current_date(), col("day_offset").cast("int"))) \
.withColumn("day_of_week", dayofweek(col("usage_date")))

# Calculate realistic usage patterns
usage_df = usage_df \
.withColumn("base_download_gb",
    when(col("plan_tier").contains("Enterprise"), 50 + rand() * 100)
    .when(col("plan_tier").contains("Business"), 20 + rand() * 50)
    .when(col("plan_tier").contains("1000"), 15 + rand() * 35)
    .when(col("plan_tier").contains("500"), 10 + rand() * 25)
    .when(col("plan_tier").contains("250"), 8 + rand() * 17)
    .when(col("plan_tier").contains("100"), 5 + rand() * 12)
    .when(col("plan_tier").contains("50"), 3 + rand() * 8)
    .otherwise(2 + rand() * 5)
) \
.withColumn("weekend_multiplier",
    when(col("day_of_week").isin([1, 7]), 1.3 + rand() * 0.3)
    .otherwise(1.0)
) \
.withColumn("download_gb", 
    spark_round(col("base_download_gb") * col("weekend_multiplier"), 2)
) \
.withColumn("upload_gb",
    spark_round(col("download_gb") * (0.1 + rand() * 0.15), 2)
) \
.withColumn("peak_hour_usage_pct",
    spark_round(40 + rand() * 35, 1)
) \
.withColumn("streaming_hours",
    spark_round(rand() * 8, 1)
) \
.withColumn("gaming_hours",
    spark_round(rand() * 4, 1)
) \
.withColumn("work_from_home_hours",
    when(col("day_of_week").isin([1, 7]), spark_round(rand() * 2, 1))
    .otherwise(spark_round(rand() * 8, 1))
) \
.withColumn("avg_achieved_download_mbps",
    spark_round(col("download_speed_mbps") * (0.7 + rand() * 0.28), 1)
) \
.withColumn("speed_achievement_pct",
    spark_round(col("avg_achieved_download_mbps") / col("download_speed_mbps") * 100, 1)
)

usage_df = usage_df.select(
    "customer_id", "poi_id", "usage_date", "day_of_week",
    "download_gb", "upload_gb", "peak_hour_usage_pct",
    "streaming_hours", "gaming_hours", "work_from_home_hours",
    "avg_achieved_download_mbps", "download_speed_mbps", "speed_achievement_pct"
)

usage_df.write.mode("overwrite").saveAsTable("customer_usage")
print(f"✅ Created customer_usage table with {usage_df.count()} records")
display(usage_df.limit(30))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7️⃣ Capacity Forecasts (ML Predictions)
# MAGIC
# MAGIC Simulated ML model predictions for capacity planning over the next 6 months.

# COMMAND ----------

# Generate 6-month forecasts for each POI
poi_data = spark.table("poi_infrastructure")

forecast_df = poi_data.select(
    "poi_id", "suburb", "state", "city", "technology_type", 
    "max_capacity_gbps", "premises_served"
) \
.crossJoin(
    spark.range(1, 7).toDF("months_ahead")
) \
.withColumn("forecast_date", 
    expr("add_months(current_date(), months_ahead)")
)

# Get current average utilization from telemetry
current_util = spark.table("network_telemetry") \
    .filter((col("hour") >= 18) & (col("hour") <= 21)) \
    .groupBy("poi_id") \
    .agg(
        expr("avg(utilization_pct)").alias("current_peak_utilization"),
        expr("max(utilization_pct)").alias("current_max_utilization")
    )

forecast_df = forecast_df.join(current_util, "poi_id", "left")

# Calculate projected growth
forecast_df = forecast_df \
.withColumn("monthly_growth_rate",
    when(col("suburb").isin("Werribee", "Cranbourne", "Tarneit", "Point Cook"), 0.025 + rand() * 0.015)
    .when(col("technology_type") == "FTTN", 0.015 + rand() * 0.01)
    .otherwise(0.008 + rand() * 0.008)
) \
.withColumn("projected_utilization",
    least(
        lit(99.0),
        col("current_peak_utilization") * (1 + col("monthly_growth_rate") * col("months_ahead"))
    )
) \
.withColumn("projected_premises",
    (col("premises_served") * (1 + col("monthly_growth_rate") * col("months_ahead"))).cast("int")
) \
.withColumn("capacity_headroom_pct",
    greatest(lit(0), 100 - col("projected_utilization"))
) \
.withColumn("risk_score",
    when(col("projected_utilization") > 90, lit("Critical"))
    .when(col("projected_utilization") > 80, lit("High"))
    .when(col("projected_utilization") > 70, lit("Medium"))
    .otherwise(lit("Low"))
) \
.withColumn("upgrade_recommended",
    col("projected_utilization") > 80
) \
.withColumn("estimated_upgrade_cost_aud",
    when(col("technology_type") == "FTTN", 
         when(col("upgrade_recommended"), (500000 + rand() * 1500000).cast("int")).otherwise(lit(0)))
    .when(col("technology_type") == "HFC",
         when(col("upgrade_recommended"), (300000 + rand() * 700000).cast("int")).otherwise(lit(0)))
    .otherwise(
         when(col("upgrade_recommended"), (200000 + rand() * 400000).cast("int")).otherwise(lit(0)))
) \
.withColumn("confidence_score",
    spark_round(0.75 + rand() * 0.2, 2)
) \
.withColumn("model_version", lit("capacity_forecast_v2.3"))

forecast_df = forecast_df.select(
    "poi_id", "suburb", "city", "state", "technology_type",
    "forecast_date", "months_ahead",
    spark_round(col("current_peak_utilization"), 1).alias("current_peak_utilization_pct"),
    spark_round(col("projected_utilization"), 1).alias("projected_utilization_pct"),
    spark_round(col("capacity_headroom_pct"), 1).alias("capacity_headroom_pct"),
    "projected_premises", "risk_score", "upgrade_recommended",
    "estimated_upgrade_cost_aud", "confidence_score", "model_version"
)

forecast_df.write.mode("overwrite").saveAsTable("capacity_forecasts")
print(f"✅ Created capacity_forecasts table with {forecast_df.count()} records")
display(forecast_df.filter(col("risk_score").isin("Critical", "High")).orderBy("projected_utilization_pct", ascending=False).limit(30))

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Data Generation Complete!
# MAGIC
# MAGIC ### Summary of Tables Created:

# COMMAND ----------

# Summary of all tables
tables = [
    "poi_infrastructure",
    "premises", 
    "customers",
    "network_telemetry",
    "incidents",
    "customer_usage",
    "capacity_forecasts"
]

print("=" * 70)
print("📊 SOUTHERNLINK NETWORKS - SYNTHETIC DATA SUMMARY")
print("=" * 70)
print(f"Catalog: {CATALOG}")
print(f"Schema: {SCHEMA}")
print("=" * 70)

for table in tables:
    count = spark.table(table).count()
    print(f"✅ {table:25} | {count:>12,} rows")

print("=" * 70)
print("\n🎉 All synthetic data has been generated successfully!")
print("You can now use these tables with AI/BI Genie for the demo.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔍 Sample Queries for Genie Demo
# MAGIC
# MAGIC Here are some sample questions you can ask Genie:
# MAGIC
# MAGIC 1. **"Which suburbs in Melbourne have the highest risk of congestion over the next 6 months?"**
# MAGIC 2. **"Show me the top 10 POIs with the most critical incidents in the last 3 months"**
# MAGIC 3. **"What percentage of customers are achieving their plan speeds during peak hours?"**
# MAGIC 4. **"Which technology type has the worst performance during evening peak?"**
# MAGIC 5. **"How many customers would be affected if we had an outage at the Werribee POI?"**
# MAGIC
