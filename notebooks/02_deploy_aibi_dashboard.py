# Databricks notebook source
# MAGIC %md
# MAGIC # 📊 SouthernLink Networks - AI/BI Dashboard Deployment
# MAGIC 
# MAGIC This notebook creates the **Network Health Dashboard** for the demo.
# MAGIC 
# MAGIC > **Note:** AI/BI Dashboards are best created through the UI for visual design, but this notebook provides the SQL queries and structure to build the dashboard manually.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Dashboard Overview
# MAGIC 
# MAGIC **Dashboard Name:** `SouthernLink Network Intelligence`
# MAGIC 
# MAGIC ### Visualizations to Create:
# MAGIC 1. **Network Health Summary** - Key metrics cards
# MAGIC 2. **Congestion Heatmap by State** - Geographic overview
# MAGIC 3. **Technology Performance Comparison** - Bar chart
# MAGIC 4. **Real-time Congestion Status** - Status table
# MAGIC 5. **Peak Hour Trends** - Line chart
# MAGIC 6. **Capacity Risk Forecast** - Risk matrix
# MAGIC 7. **Recent Incidents** - Alert table

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📋 Step 1: Create Dashboard Queries
# MAGIC 
# MAGIC Run these queries to verify data, then use them in the AI/BI Dashboard builder.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.1 Network Health Summary (Counter Cards)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Network Health KPIs
# MAGIC -- Use for: Counter/KPI cards at top of dashboard
# MAGIC 
# MAGIC SELECT 
# MAGIC   COUNT(DISTINCT poi_id) as total_pois,
# MAGIC   ROUND(AVG(utilization_pct), 1) as avg_utilization_pct,
# MAGIC   SUM(CASE WHEN congestion_status = 'Critical' THEN 1 ELSE 0 END) as critical_pois,
# MAGIC   SUM(CASE WHEN congestion_status = 'Warning' THEN 1 ELSE 0 END) as warning_pois,
# MAGIC   ROUND(AVG(avg_latency_ms), 1) as avg_latency_ms,
# MAGIC   SUM(active_connections) as total_active_connections
# MAGIC FROM zivile.telco.network_telemetry
# MAGIC WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.2 Congestion by State (Bar Chart)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Average Utilization by State
# MAGIC -- Use for: Horizontal bar chart
# MAGIC 
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   ROUND(AVG(utilization_pct), 1) as avg_utilization_pct,
# MAGIC   COUNT(DISTINCT poi_id) as num_pois,
# MAGIC   SUM(CASE WHEN congestion_status = 'Critical' THEN 1 ELSE 0 END) as critical_count
# MAGIC FROM zivile.telco.network_telemetry
# MAGIC WHERE timestamp >= current_timestamp() - INTERVAL 1 HOUR
# MAGIC GROUP BY state
# MAGIC ORDER BY avg_utilization_pct DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.3 Technology Performance Comparison (Grouped Bar Chart)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Performance Metrics by Technology Type
# MAGIC -- Use for: Grouped bar chart comparing FTTP vs FTTN vs HFC vs Fixed Wireless
# MAGIC 
# MAGIC SELECT 
# MAGIC   technology_type,
# MAGIC   ROUND(AVG(utilization_pct), 1) as avg_utilization_pct,
# MAGIC   ROUND(AVG(avg_latency_ms), 1) as avg_latency_ms,
# MAGIC   ROUND(AVG(packet_loss_pct), 3) as avg_packet_loss_pct,
# MAGIC   ROUND(AVG(avg_download_speed_pct), 1) as avg_speed_achievement_pct
# MAGIC FROM zivile.telco.network_telemetry
# MAGIC WHERE timestamp >= current_timestamp() - INTERVAL 24 HOURS
# MAGIC GROUP BY technology_type
# MAGIC ORDER BY avg_utilization_pct DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.4 Current Congestion Status (Table with Status Icons)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Current POI Congestion Status
# MAGIC -- Use for: Table with conditional formatting (red/yellow/green)
# MAGIC 
# MAGIC WITH latest_telemetry AS (
# MAGIC   SELECT 
# MAGIC     poi_id,
# MAGIC     suburb,
# MAGIC     state,
# MAGIC     technology_type,
# MAGIC     utilization_pct,
# MAGIC     congestion_status,
# MAGIC     avg_latency_ms,
# MAGIC     active_connections,
# MAGIC     ROW_NUMBER() OVER (PARTITION BY poi_id ORDER BY timestamp DESC) as rn
# MAGIC   FROM zivile.telco.network_telemetry
# MAGIC )
# MAGIC SELECT 
# MAGIC   poi_id,
# MAGIC   suburb,
# MAGIC   state,
# MAGIC   technology_type,
# MAGIC   utilization_pct,
# MAGIC   congestion_status,
# MAGIC   avg_latency_ms,
# MAGIC   active_connections
# MAGIC FROM latest_telemetry
# MAGIC WHERE rn = 1
# MAGIC ORDER BY utilization_pct DESC
# MAGIC LIMIT 15

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.5 Peak Hour Utilization Trend (Line Chart)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Hourly Utilization Trend (Last 7 Days)
# MAGIC -- Use for: Line chart showing peak patterns
# MAGIC 
# MAGIC SELECT 
# MAGIC   hour,
# MAGIC   ROUND(AVG(utilization_pct), 1) as avg_utilization_pct,
# MAGIC   ROUND(MAX(utilization_pct), 1) as max_utilization_pct,
# MAGIC   ROUND(MIN(utilization_pct), 1) as min_utilization_pct
# MAGIC FROM zivile.telco.network_telemetry
# MAGIC WHERE date >= current_date() - INTERVAL 7 DAYS
# MAGIC GROUP BY hour
# MAGIC ORDER BY hour

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.6 Capacity Risk Forecast - High Risk Suburbs (Table)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: High Risk Suburbs for Congestion (6 Month Forecast)
# MAGIC -- Use for: Risk matrix table - THE KEY DEMO TABLE
# MAGIC 
# MAGIC SELECT 
# MAGIC   suburb,
# MAGIC   city,
# MAGIC   state,
# MAGIC   technology_type,
# MAGIC   ROUND(current_peak_utilization_pct, 1) as current_utilization_pct,
# MAGIC   ROUND(projected_utilization_pct, 1) as projected_6mo_pct,
# MAGIC   risk_score,
# MAGIC   upgrade_recommended,
# MAGIC   CONCAT('$', FORMAT_NUMBER(estimated_upgrade_cost_aud, 0)) as upgrade_cost,
# MAGIC   ROUND(confidence_score * 100, 0) as confidence_pct
# MAGIC FROM zivile.telco.capacity_forecasts
# MAGIC WHERE months_ahead = 6
# MAGIC   AND risk_score IN ('Critical', 'High')
# MAGIC ORDER BY projected_utilization_pct DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.7 Recent Incidents (Alert Table)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Recent Network Incidents
# MAGIC -- Use for: Incident alert table
# MAGIC 
# MAGIC SELECT 
# MAGIC   incident_id,
# MAGIC   suburb,
# MAGIC   state,
# MAGIC   incident_type,
# MAGIC   severity,
# MAGIC   DATE_FORMAT(incident_time, 'yyyy-MM-dd HH:mm') as incident_time,
# MAGIC   ROUND(duration_hours, 1) as duration_hours,
# MAGIC   FORMAT_NUMBER(customers_affected, 0) as customers_affected,
# MAGIC   status
# MAGIC FROM zivile.telco.incidents
# MAGIC WHERE incident_time >= current_timestamp() - INTERVAL 30 DAYS
# MAGIC ORDER BY incident_time DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1.8 Customer Speed Achievement (Pie Chart)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- QUERY: Speed Achievement Distribution
# MAGIC -- Use for: Pie or donut chart
# MAGIC 
# MAGIC SELECT 
# MAGIC   CASE 
# MAGIC     WHEN speed_achievement_pct >= 90 THEN '90-100% (Excellent)'
# MAGIC     WHEN speed_achievement_pct >= 75 THEN '75-90% (Good)'
# MAGIC     WHEN speed_achievement_pct >= 50 THEN '50-75% (Fair)'
# MAGIC     ELSE 'Below 50% (Poor)'
# MAGIC   END as speed_tier,
# MAGIC   COUNT(*) as customer_count,
# MAGIC   ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
# MAGIC FROM zivile.telco.customer_usage
# MAGIC WHERE usage_date >= current_date() - INTERVAL 7 DAYS
# MAGIC GROUP BY 
# MAGIC   CASE 
# MAGIC     WHEN speed_achievement_pct >= 90 THEN '90-100% (Excellent)'
# MAGIC     WHEN speed_achievement_pct >= 75 THEN '75-90% (Good)'
# MAGIC     WHEN speed_achievement_pct >= 50 THEN '50-75% (Fair)'
# MAGIC     ELSE 'Below 50% (Poor)'
# MAGIC   END
# MAGIC ORDER BY percentage DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📋 Step 2: Create Dashboard in UI
# MAGIC 
# MAGIC ### Manual Steps:
# MAGIC 
# MAGIC 1. **Navigate to Dashboards** → Click **"Create Dashboard"** → Select **"AI/BI Dashboard"**
# MAGIC 
# MAGIC 2. **Name the Dashboard:** `SouthernLink Network Intelligence`
# MAGIC 
# MAGIC 3. **Add Datasets:** Connect to `zivile.telco` schema and add:
# MAGIC    - `network_telemetry`
# MAGIC    - `capacity_forecasts`
# MAGIC    - `incidents`
# MAGIC    - `customer_usage`
# MAGIC    - `poi_infrastructure`
# MAGIC 
# MAGIC 4. **Create Visualizations** using the queries above:
# MAGIC 
# MAGIC    | Widget | Type | Query Section |
# MAGIC    |--------|------|---------------|
# MAGIC    | Total POIs | Counter | 1.1 |
# MAGIC    | Avg Utilization | Counter | 1.1 |
# MAGIC    | Critical Alerts | Counter | 1.1 |
# MAGIC    | State Performance | Bar Chart | 1.2 |
# MAGIC    | Technology Comparison | Bar Chart | 1.3 |
# MAGIC    | Current Status | Table | 1.4 |
# MAGIC    | Peak Hour Trend | Line Chart | 1.5 |
# MAGIC    | Risk Forecast | Table | 1.6 |
# MAGIC    | Recent Incidents | Table | 1.7 |
# MAGIC    | Speed Achievement | Pie Chart | 1.8 |
# MAGIC 
# MAGIC 5. **Apply Styling:**
# MAGIC    - Use conditional formatting on congestion_status (Red=Critical, Yellow=Warning, Green=Normal)
# MAGIC    - Add filters for State and Technology Type
# MAGIC    - Set auto-refresh to 5 minutes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎨 Dashboard Layout Recommendation
# MAGIC 
# MAGIC ```
# MAGIC ┌─────────────────────────────────────────────────────────────────────────────┐
# MAGIC │                    SOUTHERNLINK NETWORK INTELLIGENCE                        │
# MAGIC │  [Filter: State ▼]  [Filter: Technology ▼]  [Time: Last 24 Hours ▼]        │
# MAGIC ├─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────┤
# MAGIC │  TOTAL POIs │ AVG UTIL %  │  CRITICAL   │   WARNING   │  AVG LATENCY (ms)   │
# MAGIC │     40      │   62.3%     │     3       │     8       │      12.4           │
# MAGIC ├─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────┤
# MAGIC │                                                                             │
# MAGIC │  ┌─────────────────────────────┐  ┌─────────────────────────────────────┐   │
# MAGIC │  │   STATE PERFORMANCE (Bar)   │  │   TECHNOLOGY COMPARISON (Bar)       │   │
# MAGIC │  │   VIC ████████████ 72%      │  │   FTTN  ████████████ 68%            │   │
# MAGIC │  │   NSW ██████████ 65%        │  │   HFC   ████████ 55%                │   │
# MAGIC │  │   QLD ████████ 58%          │  │   FTTP  ██████ 45%                  │   │
# MAGIC │  └─────────────────────────────┘  └─────────────────────────────────────┘   │
# MAGIC │                                                                             │
# MAGIC │  ┌───────────────────────────────────────────────────────────────────────┐  │
# MAGIC │  │              PEAK HOUR UTILIZATION TREND (Line Chart)                 │  │
# MAGIC │  │  100%│                          ╭──╮                                  │  │
# MAGIC │  │   75%│                       ╭──╯  ╰──╮                               │  │
# MAGIC │  │   50%│  ╭──────────────╮  ╭──╯        ╰──╮                            │  │
# MAGIC │  │   25%│──╯              ╰──╯              ╰──                          │  │
# MAGIC │  │      └──────────────────────────────────────                         │  │
# MAGIC │  │        6AM    12PM    6PM    9PM    12AM                              │  │
# MAGIC │  └───────────────────────────────────────────────────────────────────────┘  │
# MAGIC │                                                                             │
# MAGIC │  ┌───────────────────────────────────────────────────────────────────────┐  │
# MAGIC │  │  🔴 HIGH RISK SUBURBS - 6 MONTH FORECAST                              │  │
# MAGIC │  │  ───────────────────────────────────────────────────────────────────  │  │
# MAGIC │  │  Suburb      │ Tech │ Current │ Projected │ Risk     │ Upgrade Cost  │  │
# MAGIC │  │  Werribee    │ FTTN │ 78%     │ 94%       │ Critical │ $1,200,000    │  │
# MAGIC │  │  Cranbourne  │ FTTN │ 72%     │ 89%       │ Critical │ $980,000      │  │
# MAGIC │  │  Point Cook  │ FTTN │ 69%     │ 85%       │ High     │ $750,000      │  │
# MAGIC │  └───────────────────────────────────────────────────────────────────────┘  │
# MAGIC │                                                                             │
# MAGIC │  ┌─────────────────────────────┐  ┌─────────────────────────────────────┐   │
# MAGIC │  │  RECENT INCIDENTS (Table)   │  │   SPEED ACHIEVEMENT (Pie)           │   │
# MAGIC │  │  🔴 Fiber Cut - Werribee    │  │        ┌───────┐                    │   │
# MAGIC │  │  🟡 Capacity - Point Cook   │  │   90%+ │███████│ 45%                │   │
# MAGIC │  │  🟢 Maintenance - Sydney    │  │   75%+ │████   │ 32%                │   │
# MAGIC │  └─────────────────────────────┘  └─────────────────────────────────────┘   │
# MAGIC └─────────────────────────────────────────────────────────────────────────────┘
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Dashboard Deployment Complete
# MAGIC 
# MAGIC ### Demo Talking Points for Dashboard:
# MAGIC 
# MAGIC 1. **"This is a real-time view of SouthernLink's entire network"**
# MAGIC    - Point to the KPI cards showing live metrics
# MAGIC 
# MAGIC 2. **"Instantly see which states and technologies need attention"**
# MAGIC    - Highlight VIC and FTTN showing higher utilization
# MAGIC 
# MAGIC 3. **"Peak hour patterns are clear - 6-9 PM is when issues occur"**
# MAGIC    - Show the line chart spike
# MAGIC 
# MAGIC 4. **"ML predictions show us problems BEFORE they happen"**
# MAGIC    - Focus on the Risk Forecast table
# MAGIC    - "Werribee will hit 94% utilization in 6 months if we don't act"
# MAGIC 
# MAGIC 5. **"Any business user can explore this without writing SQL"**
# MAGIC    - Use the filters to drill down
# MAGIC    - "But what if they have a question that's not on this dashboard?"
# MAGIC    - **→ Transition to Genie demo**

