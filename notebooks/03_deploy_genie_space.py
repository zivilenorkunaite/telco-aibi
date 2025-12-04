# Databricks notebook source
# MAGIC %md
# MAGIC # 🧞 SouthernLink Networks - AI/BI Genie Space Deployment
# MAGIC 
# MAGIC This notebook provides the configuration and setup instructions for the **Genie Space** used in the demo.
# MAGIC 
# MAGIC Genie enables business users to ask questions in natural language and get instant answers from the data.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Genie Space Overview
# MAGIC 
# MAGIC **Space Name:** `SouthernLink Network Intelligence`
# MAGIC 
# MAGIC **Purpose:** Enable network operations, planning, and executive teams to explore network health data without SQL knowledge.
# MAGIC 
# MAGIC **Key Capabilities:**
# MAGIC - Natural language queries
# MAGIC - Automatic SQL generation
# MAGIC - Deep Research for complex analysis
# MAGIC - Governed access via Unity Catalog

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📋 Step 1: Create Genie Space
# MAGIC 
# MAGIC ### Manual Steps in Databricks UI:
# MAGIC 
# MAGIC 1. **Navigate to:** Workspace → Click **"+"** → Select **"Genie space"**
# MAGIC 
# MAGIC 2. **Configure Basic Settings:**
# MAGIC    - **Name:** `SouthernLink Network Intelligence`
# MAGIC    - **Description:** `AI-powered network analytics for SouthernLink Networks. Ask questions about network health, congestion, customer experience, and capacity planning.`
# MAGIC 
# MAGIC 3. **Add Tables** from `zivile.telco`:
# MAGIC    - ✅ `poi_infrastructure`
# MAGIC    - ✅ `network_telemetry`
# MAGIC    - ✅ `capacity_forecasts`
# MAGIC    - ✅ `incidents`
# MAGIC    - ✅ `customers`
# MAGIC    - ✅ `customer_usage`
# MAGIC    - ✅ `premises`

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📝 Step 2: Configure General Instructions
# MAGIC 
# MAGIC Copy and paste this into the **"General Instructions"** field in Genie Space settings:

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC You are an AI assistant for SouthernLink Networks, one of Australia's largest broadband providers.
# MAGIC 
# MAGIC DOMAIN KNOWLEDGE:
# MAGIC - SouthernLink operates a multi-technology network including FTTP (Fiber to the Premises), FTTN (Fiber to the Node), HFC (Hybrid Fiber Coaxial), and Fixed Wireless
# MAGIC - A POI (Point of Interconnect) is a network aggregation point that serves multiple customer premises
# MAGIC - Peak hours are typically 6 PM to 9 PM when residential usage is highest
# MAGIC - Congestion occurs when utilization exceeds 70% (Warning) or 85% (Critical)
# MAGIC - FTTN technology typically has lower speeds and higher congestion than FTTP
# MAGIC 
# MAGIC TERMINOLOGY:
# MAGIC - "Utilization" = percentage of maximum capacity being used
# MAGIC - "Speed achievement" = actual speed as percentage of plan speed
# MAGIC - "Premises" = customer locations (homes or businesses)
# MAGIC - "Churn risk" = likelihood of customer cancellation (0-1 score)
# MAGIC 
# MAGIC BUSINESS CONTEXT:
# MAGIC - Focus on customer experience and network reliability
# MAGIC - Proactive identification of congestion helps prevent complaints
# MAGIC - Capacity planning decisions require 6+ month forecasts
# MAGIC - FTTN to FTTP upgrades are a strategic priority
# MAGIC 
# MAGIC RESPONSE GUIDELINES:
# MAGIC - Always include relevant metrics (counts, percentages, averages)
# MAGIC - When showing POIs or suburbs, include the state for context
# MAGIC - For forecasts, always mention the confidence score
# MAGIC - Round percentages to 1 decimal place
# MAGIC - Format currency in AUD with $ symbol
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Step 3: Configure Table Descriptions
# MAGIC 
# MAGIC Add these descriptions to each table in the Genie Space settings:

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `poi_infrastructure`
# MAGIC ```
# MAGIC Network Points of Interconnect (POIs) - the physical network nodes that aggregate customer connections.
# MAGIC 
# MAGIC Key columns:
# MAGIC - poi_id: Unique identifier (format: STATE-XXXX)
# MAGIC - suburb, city, state: Geographic location
# MAGIC - technology_type: FTTP, FTTN, HFC, or Fixed Wireless
# MAGIC - premises_served: Number of customer locations connected to this POI
# MAGIC - max_capacity_gbps: Maximum throughput capacity
# MAGIC 
# MAGIC Use this table to understand network infrastructure and coverage.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `network_telemetry`
# MAGIC ```
# MAGIC Real-time and historical network performance metrics collected hourly from each POI.
# MAGIC 
# MAGIC Key columns:
# MAGIC - poi_id: Links to poi_infrastructure
# MAGIC - timestamp: When the measurement was taken
# MAGIC - utilization_pct: Percentage of max capacity in use (0-100)
# MAGIC - congestion_status: 'Normal' (<70%), 'Warning' (70-85%), 'Critical' (>85%)
# MAGIC - avg_latency_ms: Average network latency in milliseconds
# MAGIC - packet_loss_pct: Percentage of packets lost
# MAGIC - avg_download_speed_pct: Average customer speed as % of plan speed
# MAGIC - active_connections: Number of active customer connections
# MAGIC 
# MAGIC Contains 30 days of hourly data. Use for real-time monitoring and trend analysis.
# MAGIC Peak hours are typically 18:00-21:00 (6 PM - 9 PM).
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `capacity_forecasts`
# MAGIC ```
# MAGIC ML model predictions for network capacity over the next 6 months.
# MAGIC 
# MAGIC Key columns:
# MAGIC - poi_id: Links to poi_infrastructure
# MAGIC - forecast_date: The month being predicted
# MAGIC - months_ahead: 1-6 months into the future
# MAGIC - current_peak_utilization_pct: Current peak hour utilization
# MAGIC - projected_utilization_pct: Predicted utilization at forecast_date
# MAGIC - risk_score: 'Critical', 'High', 'Medium', or 'Low'
# MAGIC - upgrade_recommended: Boolean - should this POI be upgraded?
# MAGIC - estimated_upgrade_cost_aud: Cost to upgrade in Australian dollars
# MAGIC - confidence_score: Model confidence (0-1)
# MAGIC 
# MAGIC Use for capacity planning and prioritizing infrastructure investments.
# MAGIC High-growth suburbs like Werribee, Cranbourne, Point Cook show highest risk.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `incidents`
# MAGIC ```
# MAGIC Network incidents, outages, and maintenance events.
# MAGIC 
# MAGIC Key columns:
# MAGIC - incident_id: Unique identifier
# MAGIC - poi_id: Affected network node
# MAGIC - incident_type: 'Hardware Failure', 'Fiber Cut', 'Power Outage', 'Capacity Exceeded', etc.
# MAGIC - severity: 'Critical', 'High', 'Medium', 'Low'
# MAGIC - incident_time: When the incident started
# MAGIC - duration_hours: How long the incident lasted
# MAGIC - customers_affected: Number of impacted customers
# MAGIC - root_cause: Description of what caused the incident
# MAGIC - status: 'Open' or 'Resolved'
# MAGIC 
# MAGIC Contains 12 months of incident history. Use for root cause analysis and reliability metrics.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `customers`
# MAGIC ```
# MAGIC Customer accounts and their broadband plans.
# MAGIC 
# MAGIC Key columns:
# MAGIC - customer_id: Unique customer identifier
# MAGIC - premise_id: Customer's physical location
# MAGIC - poi_id: Network node serving this customer
# MAGIC - plan_tier: Plan name (e.g., 'Standard 50', 'Premium 250', 'Business 100')
# MAGIC - download_speed_mbps: Plan's advertised download speed
# MAGIC - upload_speed_mbps: Plan's advertised upload speed
# MAGIC - monthly_price: Monthly subscription cost in AUD
# MAGIC - premise_type: 'Residential', 'Business', or 'Enterprise'
# MAGIC - is_active: Whether the account is currently active
# MAGIC - churn_risk_score: ML-predicted likelihood of cancellation (0-1)
# MAGIC 
# MAGIC Use for customer experience analysis and churn prediction.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `customer_usage`
# MAGIC ```
# MAGIC Daily aggregated usage data per customer.
# MAGIC 
# MAGIC Key columns:
# MAGIC - customer_id: Links to customers table
# MAGIC - usage_date: Date of usage
# MAGIC - download_gb: Total download in gigabytes
# MAGIC - upload_gb: Total upload in gigabytes
# MAGIC - peak_hour_usage_pct: Percentage of usage during peak hours (6-9 PM)
# MAGIC - streaming_hours: Hours spent streaming video
# MAGIC - gaming_hours: Hours spent gaming
# MAGIC - work_from_home_hours: Hours of video conferencing/WFH activity
# MAGIC - avg_achieved_download_mbps: Actual speed achieved
# MAGIC - speed_achievement_pct: Actual speed as % of plan speed
# MAGIC 
# MAGIC Contains 90 days of daily data. Use for usage pattern analysis and speed performance tracking.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table: `premises`
# MAGIC ```
# MAGIC Physical customer locations that can be connected to the network.
# MAGIC 
# MAGIC Key columns:
# MAGIC - premise_id: Unique location identifier
# MAGIC - poi_id: Network node that serves this location
# MAGIC - address: Full street address
# MAGIC - suburb, state: Geographic location
# MAGIC - technology_type: Available connection technology
# MAGIC - premise_type: 'Residential', 'Business', or 'Enterprise'
# MAGIC - is_connected: Whether currently connected to the network
# MAGIC - connection_date: When the premise was connected
# MAGIC 
# MAGIC Use to understand coverage and connection rates.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎤 Step 4: Sample Questions for Demo
# MAGIC 
# MAGIC ### Quick Questions (Simple Queries)

# COMMAND ----------

# MAGIC %md
# MAGIC **Question 1: Current Status**
# MAGIC > "Which POIs are currently in Critical congestion status?"
# MAGIC 
# MAGIC **Expected Result:** Table of POIs with utilization > 85%

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verify query works
# MAGIC SELECT DISTINCT poi_id, suburb, state, technology_type, utilization_pct, congestion_status
# MAGIC FROM zivile.telco.network_telemetry
# MAGIC WHERE congestion_status = 'Critical'
# MAGIC   AND timestamp >= current_timestamp() - INTERVAL 2 HOURS
# MAGIC ORDER BY utilization_pct DESC

# COMMAND ----------

# MAGIC %md
# MAGIC **Question 2: Technology Comparison**
# MAGIC > "What is the average latency by technology type?"
# MAGIC 
# MAGIC **Expected Result:** Bar chart comparing FTTP, FTTN, HFC, Fixed Wireless

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT technology_type, ROUND(AVG(avg_latency_ms), 1) as avg_latency_ms
# MAGIC FROM zivile.telco.network_telemetry
# MAGIC WHERE timestamp >= current_timestamp() - INTERVAL 24 HOURS
# MAGIC GROUP BY technology_type
# MAGIC ORDER BY avg_latency_ms DESC

# COMMAND ----------

# MAGIC %md
# MAGIC **Question 3: Incident Analysis**
# MAGIC > "How many customers were affected by Critical incidents last month?"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC   incident_type,
# MAGIC   COUNT(*) as incident_count,
# MAGIC   SUM(customers_affected) as total_customers_affected
# MAGIC FROM zivile.telco.incidents
# MAGIC WHERE severity = 'Critical'
# MAGIC   AND incident_time >= current_date() - INTERVAL 30 DAYS
# MAGIC GROUP BY incident_type
# MAGIC ORDER BY total_customers_affected DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🌟 Deep Research Question (THE STAR OF THE DEMO)

# COMMAND ----------

# MAGIC %md
# MAGIC **Deep Research Question:**
# MAGIC 
# MAGIC > "Which suburbs in Melbourne have the highest risk of congestion during evening peak hours over the next 6 months, and what's driving the growth? Include recommendations for capacity upgrades."
# MAGIC 
# MAGIC **Why this works for Deep Research:**
# MAGIC - Multi-part question requiring analysis across multiple tables
# MAGIC - Requires joining telemetry data with forecasts
# MAGIC - Needs business reasoning (recommendations)
# MAGIC - Produces a comprehensive report format

# COMMAND ----------

# MAGIC %sql
# MAGIC -- This is what Genie Deep Research will generate (approximately)
# MAGIC WITH melbourne_forecasts AS (
# MAGIC   SELECT 
# MAGIC     cf.poi_id,
# MAGIC     cf.suburb,
# MAGIC     cf.technology_type,
# MAGIC     cf.current_peak_utilization_pct,
# MAGIC     cf.projected_utilization_pct,
# MAGIC     cf.risk_score,
# MAGIC     cf.upgrade_recommended,
# MAGIC     cf.estimated_upgrade_cost_aud,
# MAGIC     cf.confidence_score
# MAGIC   FROM zivile.telco.capacity_forecasts cf
# MAGIC   WHERE cf.city = 'Melbourne'
# MAGIC     AND cf.months_ahead = 6
# MAGIC ),
# MAGIC evening_peak_stats AS (
# MAGIC   SELECT 
# MAGIC     nt.poi_id,
# MAGIC     AVG(nt.utilization_pct) as avg_evening_utilization,
# MAGIC     MAX(nt.utilization_pct) as max_evening_utilization,
# MAGIC     AVG(nt.avg_latency_ms) as avg_latency
# MAGIC   FROM zivile.telco.network_telemetry nt
# MAGIC   WHERE nt.hour BETWEEN 18 AND 21  -- Evening peak
# MAGIC     AND nt.date >= current_date() - INTERVAL 7 DAYS
# MAGIC   GROUP BY nt.poi_id
# MAGIC ),
# MAGIC customer_growth AS (
# MAGIC   SELECT 
# MAGIC     poi_id,
# MAGIC     COUNT(DISTINCT customer_id) as customer_count,
# MAGIC     AVG(churn_risk_score) as avg_churn_risk
# MAGIC   FROM zivile.telco.customers
# MAGIC   WHERE is_active = true
# MAGIC   GROUP BY poi_id
# MAGIC )
# MAGIC SELECT 
# MAGIC   mf.suburb,
# MAGIC   mf.technology_type,
# MAGIC   ROUND(mf.current_peak_utilization_pct, 1) as current_utilization_pct,
# MAGIC   ROUND(mf.projected_utilization_pct, 1) as projected_6mo_pct,
# MAGIC   ROUND(eps.avg_evening_utilization, 1) as avg_evening_peak_pct,
# MAGIC   mf.risk_score,
# MAGIC   mf.upgrade_recommended,
# MAGIC   CONCAT('$', FORMAT_NUMBER(mf.estimated_upgrade_cost_aud, 0)) as estimated_cost,
# MAGIC   cg.customer_count,
# MAGIC   ROUND(mf.confidence_score * 100, 0) as confidence_pct
# MAGIC FROM melbourne_forecasts mf
# MAGIC JOIN evening_peak_stats eps ON mf.poi_id = eps.poi_id
# MAGIC JOIN customer_growth cg ON mf.poi_id = cg.poi_id
# MAGIC WHERE mf.risk_score IN ('Critical', 'High')
# MAGIC ORDER BY mf.projected_utilization_pct DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Additional Demo Questions

# COMMAND ----------

# MAGIC %md
# MAGIC **Operations Team Questions:**
# MAGIC 1. "What was the root cause of the most recent Critical incident?"
# MAGIC 2. "Show me POIs with utilization above 80% right now"
# MAGIC 3. "Which suburbs had the most outages in the last 3 months?"
# MAGIC 
# MAGIC **Planning Team Questions:**
# MAGIC 1. "What's the total estimated cost to upgrade all high-risk POIs?"
# MAGIC 2. "When will the Brisbane CBD POI reach 80% capacity?"
# MAGIC 3. "Compare congestion trends between FTTN and FTTP suburbs"
# MAGIC 
# MAGIC **Executive Questions:**
# MAGIC 1. "Give me a summary of network health by state"
# MAGIC 2. "How many customers are not achieving their plan speeds?"
# MAGIC 3. "What percentage of our customers are at high churn risk?"
# MAGIC 
# MAGIC **Customer Experience Questions:**
# MAGIC 1. "Which suburbs have the worst speed achievement during peak hours?"
# MAGIC 2. "How many customers would be affected if Werribee POI went down?"
# MAGIC 3. "What's the average streaming hours for customers on Premium plans?"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔗 Step 5: Unity Catalog Lineage Demo (Optional)
# MAGIC 
# MAGIC If time permits, show UC Lineage to demonstrate data governance:
# MAGIC 
# MAGIC ### Demo Flow:
# MAGIC 1. **Navigate to:** Data Explorer → `zivile.telco.capacity_forecasts`
# MAGIC 2. **Click:** "Lineage" tab
# MAGIC 3. **Show:** How the forecasts table is derived from:
# MAGIC    - `network_telemetry` (real-time data)
# MAGIC    - `poi_infrastructure` (capacity limits)
# MAGIC    - ML model predictions
# MAGIC 
# MAGIC ### Talking Points:
# MAGIC > *"Unity Catalog tracks where every piece of data comes from. Your governance team can see exactly which tables feed into these forecasts, who has access, and how the data flows through your organization."*
# MAGIC 
# MAGIC > *"When Genie answers a question, it only accesses data the user is authorized to see. If someone shouldn't see customer-level data, they won't - even through Genie."*

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Genie Space Deployment Complete
# MAGIC 
# MAGIC ### Demo Script for Genie:
# MAGIC 
# MAGIC 1. **Start with the Dashboard** (from previous notebook)
# MAGIC    - "This dashboard shows what we've pre-built..."
# MAGIC    - "But what if you have a question that's not here?"
# MAGIC 
# MAGIC 2. **Open Genie Space**
# MAGIC    - "Let me show you Genie - our AI assistant for data"
# MAGIC 
# MAGIC 3. **Ask a Simple Question First**
# MAGIC    - "Which POIs are currently critical?"
# MAGIC    - Watch Genie generate SQL and return results
# MAGIC    - "Notice - no SQL required. Plain English."
# MAGIC 
# MAGIC 4. **Show the Generated SQL**
# MAGIC    - "For technical users, you can see exactly what query was run"
# MAGIC    - "Full transparency and auditability"
# MAGIC 
# MAGIC 5. **🌟 Deep Research Demo (THE WOW MOMENT)**
# MAGIC    - "Now let's ask a complex planning question..."
# MAGIC    - Type the Melbourne congestion question
# MAGIC    - "Watch as Genie performs deep research across multiple tables..."
# MAGIC    - Show the comprehensive report with recommendations
# MAGIC 
# MAGIC 6. **Close with Business Value**
# MAGIC    - "This analysis used to take 2 weeks and 3 teams"
# MAGIC    - "Now any business user can get it in 90 seconds"
# MAGIC    - "And it's all governed by Unity Catalog"

