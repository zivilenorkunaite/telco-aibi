# 🚀 15-Minute Databricks AI/BI Demo
## "Network Health Dashboard with AI-Powered Insights"

**Demo Focus:** Self-Service Analytics for Business Users

---

## 📋 Executive Summary

**Audience:** Technical & Business Leadership  
**Duration:** 15 minutes  
**Focus:** Self-service AI/BI capabilities (Dashboard, Genie, Deep Research)

**What We're NOT Showing:**
- ❌ Platform compute / infrastructure setup
- ❌ Data engineering pipelines
- ❌ Code-heavy notebooks
- ❌ MLOps / model training

**What We ARE Showing:**
- ✅ AI/BI Dashboard - Interactive network health visualization
- ✅ AI/BI Genie - Natural language queries
- ✅ Genie Deep Research - Complex multi-table analysis
- ✅ (Optional) Unity Catalog Lineage - Data governance

---

## 🎯 The Story Arc

> *"Your network team currently spends days pulling reports from multiple systems. Your planning team waits weeks for data science to answer capacity questions. What if ANY business user could get answers in seconds - in plain English?"*

---

## 🔴 Pain Points We're Addressing

| Pain Point | Current State | With Databricks AI/BI |
|------------|---------------|----------------------|
| **Report Generation** | Days to create, static, outdated | Real-time dashboards, always current |
| **Ad-hoc Questions** | Submit ticket → wait days → get data dump | Ask Genie → get answer in seconds |
| **Complex Analysis** | Need data science team | Deep Research generates full reports |
| **Data Access** | Only analysts can query | Any business user, governed access |

---

## 🎬 DEMO SCRIPT (15 Minutes)

### ⏱️ MINUTE 0-2: The Hook

**TALKING POINTS:**

> *"Let me show you how your team could work differently..."*

- "Today: Your planning team needs to know which suburbs will hit capacity limits - that's a 2-week project involving 3 teams"
- "With Databricks AI/BI: They ask a question in plain English and get a comprehensive report in 90 seconds"
- "No SQL. No tickets. No waiting."

---

### ⏱️ MINUTE 2-6: AI/BI Dashboard Demo

**OPEN:** `SouthernLink Network Intelligence` dashboard

**TALKING POINTS:**

> *"This is your network operations command center..."*

**Walk Through the Dashboard:**

1. **KPI Cards (Top Row)**
   - "At a glance: 40 POIs, current utilization, critical alerts"
   - "This updates in real-time - no overnight batch jobs"

2. **State Performance Chart**
   - "Instantly see which states need attention"
   - "Click VIC to drill down..." (use filter)

3. **Technology Comparison**
   - "Compare FTTN vs FTTP vs HFC performance"
   - "Notice FTTN runs hotter - that's expected given the technology"

4. **Peak Hour Trend**
   - "Clear pattern: 6-9 PM is when congestion happens"
   - "This helps ops teams prepare"

5. **🔴 High Risk Suburbs Table (KEY MOMENT)**
   - "This is powered by ML predictions"
   - "Werribee will hit 94% utilization in 6 months if we don't upgrade"
   - "The business case is right here - upgrade cost, confidence score"

**TRANSITION:**
> *"This dashboard answers the questions we knew to ask. But what about the questions that aren't pre-built?"*

---

### ⏱️ MINUTE 6-8: AI/BI Genie - Simple Query

**OPEN:** `SouthernLink Network Intelligence` Genie Space

**TALKING POINTS:**

> *"Meet Genie - your AI assistant for data..."*

**Type Simple Question:**
```
Which POIs are currently in Critical congestion status?
```

**While Genie Works:**
- "I'm asking in plain English - no SQL"
- "Genie understands our terminology - it knows what a POI is, what Critical means"

**Show Results:**
- "Instant answer with a visualization"
- "Click 'Show generated SQL' - full transparency for technical users"

**Ask Follow-up:**
```
What's the average latency for FTTN vs FTTP?
```

- "Follow-up questions build on context"
- "Any business user can explore data this way"

---

### ⏱️ MINUTE 8-13: 🌟 Genie Deep Research (THE WOW MOMENT)

**TALKING POINTS:**

> *"Now let's ask something complex - the kind of question that used to require a full analytics project..."*

**Type Deep Research Question:**
```
Which suburbs in Melbourne have the highest risk of congestion 
during evening peak hours over the next 6 months, and what's 
driving the growth? Include recommendations for capacity upgrades.
```

**While Deep Research Runs (Narrate):**
> *"Watch what's happening:*
> - *Genie is analyzing the question...*
> - *Querying multiple tables - telemetry, forecasts, customer data...*
> - *Generating a comprehensive research report...*
> - *Including recommendations based on the data..."*

**Show Deep Research Output:**

**SAMPLE OUTPUT:**

```
## 🔍 Deep Research Report: Melbourne Congestion Risk Analysis

### Executive Summary
Analysis of Melbourne metro area identifies 5 high-risk suburbs 
for evening peak congestion over the next 6 months.

### Top 5 High-Risk Suburbs:
| Suburb      | Tech | Current | 6-Month Proj | Risk     | Upgrade Cost |
|-------------|------|---------|--------------|----------|--------------|
| Werribee    | FTTN | 78%     | 94%          | Critical | $1,200,000   |
| Cranbourne  | FTTN | 72%     | 89%          | Critical | $980,000     |
| Point Cook  | FTTN | 69%     | 85%          | High     | $750,000     |
| Tarneit     | FTTP | 65%     | 82%          | High     | $420,000     |
| Epping      | HFC  | 63%     | 79%          | High     | $380,000     |

### Key Drivers:
1. **Population Growth:** Western Melbourne suburbs seeing 4.2% YoY growth
2. **Work-from-Home:** 34% increase in daytime usage persisting
3. **Streaming Demand:** 4K adoption up 67% in these areas

### Recommendations:
1. Priority FTTN-to-FTTP upgrades: Werribee, Cranbourne (ROI: 18 months)
2. Capacity augmentation: Point Cook POI backhaul
3. Proactive communication: ~12,400 customers should be notified
```

**KEY TALKING POINTS:**

1. **"No SQL Required"**
   > *"Your planning team didn't write a single line of code. They asked a business question and got a business answer."*

2. **"Multi-Table Analysis"**
   > *"This pulled from telemetry data, capacity forecasts, AND customer records - automatically."*

3. **"Actionable Recommendations"**
   > *"Not just data - actual recommendations with costs and ROI estimates."*

4. **"90 Seconds vs 2 Weeks"**
   > *"This analysis used to require a data scientist, an analyst, and a planning lead. Now any business user can do it."*

---

### ⏱️ MINUTE 13-14: (Optional) Unity Catalog Lineage

**IF TIME PERMITS:**

**Navigate to:** Data Explorer → `zivile.telco.capacity_forecasts` → Lineage tab

**TALKING POINTS:**

> *"All of this is governed by Unity Catalog..."*

- "See exactly where this forecast data comes from"
- "Full lineage from raw telemetry through ML model to final table"
- "When Genie answers questions, it only accesses data the user is authorized to see"
- "If someone shouldn't see customer-level data, they won't - even through Genie"

---

### ⏱️ MINUTE 14-15: The Close

**TALKING POINTS:**

> *"Let me recap what we've seen..."*

| Capability | Business Value |
|------------|----------------|
| **AI/BI Dashboard** | Real-time visibility for ops teams |
| **Genie** | Any user can query data in plain English |
| **Deep Research** | Complex analysis in seconds, not weeks |
| **Unity Catalog** | Governed, secure, auditable |

**THE ASK:**

> *"We'd love to explore a focused proof-of-value:*
> - *Pick ONE high-impact use case - capacity planning is a great fit*
> - *4-week sprint to show real results on YOUR data*
> - *Your business users test Genie on real questions*
> - *No risk - you see value before you commit"*

---

## 🎤 Key Messages Throughout Demo

### Message 1: Self-Service
> *"The people who have the questions can now get the answers - without filing tickets or waiting for analysts."*

### Message 2: Plain English
> *"No SQL, no code, no training required. If you can type a question, you can analyze data."*

### Message 3: Governed
> *"Self-service doesn't mean ungoverned. Unity Catalog ensures the right people see the right data."*

### Message 4: Speed
> *"From weeks to seconds. Your teams can make decisions while the data is still relevant."*

---

## 📊 Demo Environment Setup

### Prerequisites:
1. Run `01_generate_synthetic_data.py` to create sample data
2. Run `02_deploy_aibi_dashboard.py` queries to verify data
3. Create AI/BI Dashboard using queries from notebook
4. Create Genie Space using config from `03_deploy_genie_space.py`

### Pre-Demo Checklist:
- [ ] Dashboard loads quickly with current data
- [ ] Genie Space responds to test questions
- [ ] Deep Research question tested and returns expected format
- [ ] Filters work on dashboard
- [ ] Backup screenshots ready (just in case)

---

## 🗣️ Objection Handling

| Objection | Response |
|-----------|----------|
| *"We already have Tableau/Power BI"* | "Great - keep using them for static reports. Genie adds the AI layer for ad-hoc questions that aren't pre-built. They complement each other." |
| *"Can we trust AI-generated queries?"* | "Two safeguards: First, you can always see the generated SQL. Second, Genie can only access data the user is authorized to see via Unity Catalog." |
| *"Our users won't adopt this"* | "That's why we start with a proof-of-value. Pick 5 power users, give them real questions. Adoption follows value." |
| *"How accurate is Deep Research?"* | "It uses your actual data and shows confidence scores. Think of it as a smart analyst who works instantly - you still review the output." |

---

## 📎 Backup Demo Questions

If you need alternatives during the demo:

**Simple Questions:**
- "Show me the top 5 POIs by utilization"
- "How many customers are on FTTN technology?"
- "What was our worst incident this month?"

**Medium Complexity:**
- "Compare speed achievement between residential and business customers"
- "Which technology type has the most capacity headroom?"

**Deep Research Alternatives:**
- "Create a summary of network health for the executive team, including key risks and recommendations"
- "Analyze the correlation between congestion events and customer churn risk"

---

*Demo materials prepared for Databricks AI/BI showcase*  
*Last updated: December 2024*
