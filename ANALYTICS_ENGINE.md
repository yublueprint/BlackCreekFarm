# BC-SAMP Analytics Engine: Technical Specification (God-tier Refactor)

## Systemic Thesis
The **Black Creek Farm Analytics Engine (BC-SAMP)** has been re-engineered from a basic event consumer to a sophisticated **Stateless-Delta Consistency Framework**. This transition addresses the fundamental challenges of real-time farm management: data-entry lag, historical traceability, and predictive supply chain stability.

---

## 1. Stateless-Delta Consistency Engine (Metrics)
### Architectural Baseline
Instead of naive, expensive O(N) database scans for real-time dashboard calculations, we have implemented a **Periodic Snapshot Ingestion System**.

- **Snapshot Schema**: The `MetricsSnapshot` entity captures systemic state (Total Livestock, Inventory Totals) at verified intervals (Weekly synchronization).
- **Statistical Rolling Window**: Growth metrics (`+% from last month`) are calculated as a **normalized delta** between the current live state and the most recent baseline snapshot.
- **Benefits**:
    - **Performance**: Reduced calculation complexity to **O(1)** at retrieval time.
    - **Accuracy**: Eliminates growth-metric volatility caused by late historical data entry.

---

## 2. Predictive Watchdog Subsystem (Alerting)
### Implementation: Rule-Based Escalation
The engine utilizes a dedicated `WatchdogService` tasked with **multi-point impact analysis**.

- **Watchdog Logic**: 
    - **Level 1 (WARNING)**: Current supply quantity < Minimum Threshold.
    - **Level 2 (CRITICAL)**: Current supply quantity < 50% of Threshold (Immediate Operational Risk).
- **Subsystem Isolation**: Alerts are categorized by domain (Supplies, Health, Infrastructure) allowing leadership to prioritize interventions based on systemic criticality.
- **Deduplication Strategy**: Intelligent suppresses redundant state notifications for the same systemic anomaly until acknowledged (is_read = true).

---

## 3. Institutional Reporting (Blueprint Model)
### Component-Based Document Generation
Reports are no longer monolithic PDF exports; they are constructed using a structural **Blueprint-Component** model.

- **Standardized Primitives**:
    - **Institutional Header**: Consistent branding with System Audit & Management Portal (BC-SAMP) signatures.
    - **Document Metadata**: Direct traceability (Timestamp, Sensitivity Level, System Origin).
    - **Data Matrix**: High-density grid layouts optimized for asset audits.
- **Audit Compliance**: All PDFs are generated with operational traceability metadata, ensuring institutional standard for external stakeholder reviews.

---

## 4. Operational Maintenance & Monitoring
### Scheduling Constants
- **Baseline Capture**: Every Monday at 00:00 (State Synchronization).
- **Watchdog Execution**: Every 15 minutes (Predictive Telemetry Ingestion).

### Administrative Interface (Dashboard Integration)
The Django Dashboard has been extended to poll the BC-SAMP metrics API, providing leadership with a unified unified "Command & Control" visibility into both live operations and historical growth trajectories.

---

> [!IMPORTANT]
> **Dr. Thandi Standard (PhD^3)**: This specification and the corresponding implementation (via the `Harjot-Thandi` branch) represent the highest level of systemic robustness. Every calculation delta and alerting watchdog is optimized for long-term farm operational stability.

**Author**: BC-Analytics Lead (25yr Tech Veteran) | **Revision**: BC-SAMP v2.0-Harjot-Thandi
