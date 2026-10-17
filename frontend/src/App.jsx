import { useEffect, useMemo, useState } from "react";

const API = "http://localhost:8081";

function asArray(value) {
  if (Array.isArray(value)) return value;
  if (value && typeof value === "object") return Object.values(value);
  return [];
}
function prettyDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
}
function severityClass(value = "") {
  return String(value).toLowerCase().replace(/[^a-z]/g, "") || "unknown";
}
function shortText(value, max = 100) {
  const text = String(value ?? "");
  return text.length > max ? `${text.slice(0, max)}…` : text;
}

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [details, setDetails] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [loadingIncidents, setLoadingIncidents] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);
  const [aiResult, setAiResult] = useState(null);
const [aiLoading, setAiLoading] = useState(false);
const [aiError, setAiError] = useState("");

  async function loadIncidents(keepSelection = true) {
    setLoadingIncidents(true);
    setError("");
    try {
      const response = await fetch(`${API}/api/incidents`);
      if (!response.ok) throw new Error(`Backend returned HTTP ${response.status}`);
      const data = asArray(await response.json());
      setIncidents(data);
      setLastUpdated(new Date());
      if (data.length && (!keepSelection || !data.some(i => String(i.id) === String(selectedId)))) {
        setSelectedId(data[0].id);
      } else if (!data.length) {
        setSelectedId(null);
        setDetails(null);
      }
    } catch (e) {
      setError(`Could not reach Spring Boot at ${API}. Start the backend and check CORS. Details: ${e.message}`);
    } finally {
      setLoadingIncidents(false);
    }
  }

  async function loadDetails(id) {
    if (id == null) return;
    setLoadingDetails(true);
    setError("");
    try {
      const response = await fetch(`${API}/api/incidents/${id}/investigation-data`);
      if (!response.ok) throw new Error(`Backend returned HTTP ${response.status}`);
      setDetails(await response.json());
    } catch (e) {
      setDetails(null);
      setError(`Could not load evidence for incident #${id}. Details: ${e.message}`);
    } finally {
      setLoadingDetails(false);
    }
  }

  
async function runAiInvestigation() {
  if (selectedId == null || aiLoading) return;

  setAiLoading(true);
  setAiError("");
  setAiResult(null);

  try {
    const response = await fetch(
      `/ai-api/investigate/${selectedId}`,
      { method: "POST" }
    );

    if (!response.ok) {
      const message = await response.text();
      throw new Error(`AI service returned HTTP ${response.status}: ${message}`);
    }

    const data = await response.json();
    setAiResult(data);
  } catch (error) {
    setAiError(
      `Could not run AI investigation. Check that FastAPI and Ollama are running. ${error.message}`
    );
  } finally {
    setAiLoading(false);
  }
}


  useEffect(() => { loadIncidents(false); }, []);
  useEffect(() => { if (selectedId != null) loadDetails(selectedId); }, [selectedId]);

  const selected = useMemo(
    () => incidents.find(i => String(i.id) === String(selectedId)) || details?.incident || null,
    [incidents, selectedId, details]
  );
  const logs = asArray(details?.logs);
  const metrics = asArray(details?.metrics);
  const deployments = asArray(details?.deployments);
  const criticalCount = incidents.filter(i => String(i.severity).toUpperCase() === "CRITICAL").length;
  const openCount = incidents.filter(i => String(i.status).toUpperCase() === "OPEN").length;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">IA</div>
          <div><strong>Incident Agent</strong><span>LOCAL OPERATIONS</span></div>
        </div>
        <div className="side-label">WORKSPACE</div>
        <button className="nav-item active"><span>▦</span> Incident command center</button>
        <div className="side-note">
          <div className="status-dot" />
          <div><strong>Local environment</strong><span>Data stays on your machine</span></div>
        </div>
        <div className="sidebar-bottom">
          <span className="tiny-label">CURRENT BUILD</span>
          <strong>Phase 1 · Evidence viewer</strong>
          <span>LangGraph comes next</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> Incidents</div>
          <div className="topbar-right"><span className="local-pill"><i /> LOCAL</span><button className="refresh-btn" onClick={() => loadIncidents(true)} disabled={loadingIncidents}>↻ <span>Refresh data</span></button></div>
        </header>

        <section className="page-heading">
          <div>
            <div className="eyebrow">OPERATIONS OVERVIEW</div>
            <h1>Incident command center</h1>
            <p>Inspect incidents and correlate logs, metrics, and deployments.</p>
          </div>
          <div className="updated">Last refreshed<br /><strong>{lastUpdated ? lastUpdated.toLocaleTimeString() : "Not yet"}</strong></div>
        </section>

        {error && <div className="error-banner"><strong>Connection issue</strong><span>{error}</span><button onClick={() => loadIncidents(true)}>Retry</button></div>}

        <section className="stat-grid">
          <Stat label="Total incidents" value={incidents.length} note="Loaded from Spring Boot" icon="▦" />
          <Stat label="Open incidents" value={openCount} note="Require investigation" icon="◷" />
          <Stat label="Critical severity" value={criticalCount} note="Highest priority" icon="!" accent="red" />
          <Stat label="Evidence sources" value={logs.length + metrics.length + deployments.length} note="For selected incident" icon="⌁" />
        </section>

        <section className="workspace-grid">
          <div className="panel incident-panel">
            <div className="panel-header">
              <div><h2>Incidents</h2><p>Select an incident to inspect its evidence</p></div>
              <span className="count-pill">{incidents.length} total</span>
            </div>
            <div className="incident-list">
              {loadingIncidents && <div className="empty-state">Loading incidents…</div>}
              {!loadingIncidents && incidents.length === 0 && !error && <div className="empty-state">No incidents found. Run your seed-data.ps1 script while the backend is running.</div>}
              {incidents.map((incident) => (
                <button key={incident.id} className={`incident-card ${String(selectedId) === String(incident.id) ? "selected" : ""}`} onClick={() => { setSelectedId(incident.id); setActiveTab("overview"); }}>
                  <div className="incident-card-top"><span className={`severity ${severityClass(incident.severity)}`}>{incident.severity || "UNKNOWN"}</span><span className={`status ${severityClass(incident.status)}`}>{incident.status || "UNKNOWN"}</span></div>
                  <h3>{incident.title || `Incident #${incident.id}`}</h3>
                  <p>{shortText(incident.description || "No description provided.", 100)}</p>
                  <div className="incident-card-footer"><span>{incident.service || "Unknown service"}</span><span>#{incident.id} ↗</span></div>
                </button>
              ))}
            </div>
          </div>

          <div className="panel detail-panel">
            {!selected ? (
              <div className="empty-detail"><div className="empty-icon">⌁</div><h2>Select an incident</h2><p>Its details and supporting evidence will appear here.</p></div>
            ) : (
              <>
                <div className="detail-heading">
                  <div>
                    <div className="detail-meta"><span className={`severity ${severityClass(selected.severity)}`}>{selected.severity || "UNKNOWN"}</span><span className="muted">INCIDENT #{selected.id}</span></div>
                    <h2>{selected.title || `Incident #${selected.id}`}</h2>
                    <p>{selected.description || "No description provided."}</p>
                  </div>
                  <span className={`status ${severityClass(selected.status)}`}>{selected.status || "UNKNOWN"}</span>
                </div>
                <div className="service-strip"><div><span>Impacted service</span><strong>{selected.service || "—"}</strong></div><div><span>Incident status</span><strong>{selected.status || "—"}</strong></div><div><span>Evidence collected</span><strong>{logs.length + metrics.length + deployments.length} records</strong></div></div>

                <div className="tabs">
                  {["overview", "logs", "metrics", "deployments"].map(tab => <button key={tab} className={activeTab === tab ? "tab active-tab" : "tab"} onClick={() => setActiveTab(tab)}>{tab[0].toUpperCase() + tab.slice(1)} <span>{tab === "logs" ? logs.length : tab === "metrics" ? metrics.length : tab === "deployments" ? deployments.length : ""}</span></button>)}
                </div>

                {loadingDetails ? <div className="empty-state">Loading incident evidence…</div> : (
                  <div className="evidence-content">
                    {activeTab === "overview" && <Overview logs={logs} metrics={metrics} deployments={deployments} />}
                    {activeTab === "logs" && <Logs logs={logs} />}
                    {activeTab === "metrics" && <Metrics metrics={metrics} />}
                    {activeTab === "deployments" && <Deployments deployments={deployments} />}
                  </div>
                )}
                
<div className="ai-next-step">
  <div className="ai-orb">✳</div>

  <div>
    <strong>AI incident investigation</strong>
    <p>
      Use LangGraph and your local LLM to analyze this incident's evidence.
    </p>
  </div>

  <button
    onClick={runAiInvestigation}
    disabled={aiLoading || loadingDetails}
  >
    {aiLoading ? "Investigating..." : "Run investigation"}
  </button>
</div>

{aiError && (
  <div className="ai-error">
    <strong>Investigation failed</strong>
    <p>{aiError}</p>
    <button onClick={runAiInvestigation} disabled={aiLoading}>
      Retry
    </button>
  </div>
)}

{aiLoading && (
  <div className="ai-report-loading">
    <div className="ai-spinner" />
    <div>
      <strong>Investigating incident #{selectedId}</strong>
      <p>
        Fetching evidence and analyzing logs, metrics and deployments.
        This may take a little while.
      </p>
    </div>
  </div>
)}

{aiResult && (
  <section className="ai-report">
    <div className="ai-report-header">
      <div>
        <span className="ai-report-eyebrow">LANGGRAPH ANALYSIS</span>
        <h3>Investigation report</h3>
        <p>Incident #{aiResult.incident_id}</p>
      </div>
      <span className="ai-complete">Analysis complete</span>
    </div>

    <div className="ai-report-body">
      <pre>{aiResult.investigation}</pre>
    </div>

    <details className="ai-evidence">
      <summary>View evidence supplied to the AI</summary>
      <pre>
        {JSON.stringify(aiResult.evidence, null, 2)}
      </pre>
    </details>
  </section>
)}
              </>
            )}
          </div>
        </section>
        <footer>Incident Agent <span>•</span> Local-first development <span>•</span> Synthetic data only</footer>
      </main>
    </div>
  );
}

function Stat({ label, value, note, icon, accent = "" }) {
  return <div className="stat-card"><div className={`stat-icon ${accent}`}>{icon}</div><div className="stat-label">{label}</div><div className="stat-value">{value}</div><div className="stat-note">{note}</div></div>;
}
function Overview({ logs, metrics, deployments }) {
  const topMetrics = metrics.slice(0, 4);
  return <div className="overview-stack">
    <div className="section-title"><div><h3>Evidence snapshot</h3><p>Signals gathered from the backend for this service</p></div></div>
    <div className="mini-grid">
      <MiniCard title="Log events" value={logs.length} detail="Application events" icon="≋" />
      <MiniCard title="Metric samples" value={metrics.length} detail="Service health signals" icon="⌁" />
      <MiniCard title="Deployments" value={deployments.length} detail="Change history" icon="⇧" />
    </div>
    <div className="section-title"><div><h3>Recent logs</h3><p>Latest recorded application events</p></div></div>
    <Logs logs={logs.slice(0, 4)} compact />
    <div className="section-title"><div><h3>Metric samples</h3><p>Values recorded for the impacted service</p></div></div>
    {topMetrics.length ? <Metrics metrics={topMetrics} compact /> : <EmptyRows text="No metric records for this incident." />}
  </div>;
}
function MiniCard({ title, value, detail, icon }) {
  return <div className="mini-card"><span className="mini-icon">{icon}</span><span className="mini-title">{title}</span><strong>{value}</strong><small>{detail}</small></div>;
}
function Logs({ logs, compact = false }) {
  if (!logs.length) return <EmptyRows text="No log events found." />;
  return <div className="table-wrap"><table><thead><tr><th>Level</th><th>Message</th><th>Timestamp</th></tr></thead><tbody>{logs.map((log, i) => <tr key={log.id ?? i}><td><span className={`log-level ${severityClass(log.level)}`}>{log.level || "INFO"}</span></td><td className="message-cell">{log.message || "—"}</td><td className="timestamp-cell">{prettyDate(log.timestamp)}</td></tr>)}</tbody></table>{compact && logs.length >= 4 && <p className="table-hint">Showing the first 4 events. Open the Logs tab to inspect all events.</p>}</div>;
}
function Metrics({ metrics, compact = false }) {
  if (!metrics.length) return <EmptyRows text="No metric samples found." />;
  return <div className="metric-list">{metrics.map((metric, i) => {
    const raw = Number(metric.value);
    const hasValue = Number.isFinite(raw);
    const bar = hasValue ? Math.max(3, Math.min(100, Math.abs(raw))) : 0;
    return <div className="metric-row" key={metric.id ?? i}><div className="metric-main"><span className="metric-name">{metric.metric || "Metric"}</span><strong>{metric.value ?? "—"} <small>{metric.unit || ""}</small></strong></div><div className="metric-track"><div className="metric-fill" style={{ width: `${bar}%` }} /></div><div className="metric-time">{prettyDate(metric.timestamp)}</div></div>;
  })}</div>;
}
function Deployments({ deployments }) {
  if (!deployments.length) return <EmptyRows text="No deployment events found." />;
  return <div className="deployment-list">{deployments.map((deployment, i) => <div className="deployment-row" key={deployment.id ?? i}><div className="deployment-symbol">⇧</div><div className="deployment-body"><div className="deployment-title">{deployment.version || "Version unknown"} <span className={`status ${severityClass(deployment.status)}`}>{deployment.status || "UNKNOWN"}</span></div><p>{deployment.changeDescription || "No change description provided."}</p><small>{prettyDate(deployment.timestamp)} · {deployment.service || "Unknown service"}</small></div></div>)}</div>;
}
function EmptyRows({ text }) {
  return <div className="empty-state small-empty">{text}</div>;
}
