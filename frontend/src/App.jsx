import { useEffect, useState } from "react";
import "./App.css";
const API_URL = "http://127.0.0.1:8000";
function App() {
const [samples, setSamples] = useState([]);
const [selected, setSelected] = useState(null);
const [result, setResult] = useState(null);
const [transactions, setTransactions] = useState([]);
const [stats, setStats] = useState({ total: 0, low: 0, medium: 0, high: 0 });
const [metrics, setMetrics] = useState(null);
const [analytics, setAnalytics] = useState(null);
const [comparison, setComparison] = useState(null);
const [featureImportance, setFeatureImportance] = useState(null);
const [loading, setLoading] = useState(false);
const loadSamples = async () => {
try {
const response = await fetch(`${API_URL}/sample-transactions`);
const data = await response.json();
setSamples(data);
setSelected(data[0]);
} catch (error) {
console.error("Could not load samples:", error);
}
};
const loadTransactions = async () => {
try {
const response = await fetch(`${API_URL}/transactions`);
const data = await response.json();
setTransactions(data);
} catch (error) {
console.error("Could not load transactions:", error);
}
};
const loadStats = async () => {
try {
const response = await fetch(`${API_URL}/stats`);
const data = await response.json();
setStats(data);
} catch (error) {
console.error("Could not load stats:", error);
}
};
const loadMetrics = async () => {
try {
const response = await fetch(`${API_URL}/model-performance`);
const data = await response.json();
setMetrics(data);
} catch (error) {
console.error("Could not load model metrics:", error);
}
};
const loadAnalytics = async () => {
try {
const response = await fetch(`${API_URL}/analytics`);
const data = await response.json();
setAnalytics(data);
} catch (error) {
console.error("Could not load analytics:", error);
}
};
const loadComparison = async () => {
try {
const response = await fetch(`${API_URL}/model-comparison`);
const data = await response.json();
setComparison(data);
} catch (error) {
console.error("Could not load model comparison:", error);
}
};
const loadFeatureImportance = async () => {
try {
const response = await fetch(`${API_URL}/feature-importance`);
const data = await response.json();
setFeatureImportance(data);
} catch (error) {
console.error("Could not load feature importance:", error);
}
};
useEffect(() => {
loadSamples();
loadTransactions();
loadStats();
loadMetrics();
loadAnalytics();
loadComparison();
loadFeatureImportance();
}, []);
const analyzeTransaction = async () => {
if (!selected) return;
setLoading(true);
setResult(null);
try {
const response = await fetch(`${API_URL}/predict`, {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({
Time: selected.Time,
V1: selected.V1,
V2: selected.V2,
V3: selected.V3,
V4: selected.V4,
V5: selected.V5,
V6: selected.V6,
V7: selected.V7,
V8: selected.V8,
V9: selected.V9,
V10: selected.V10,
V11: selected.V11,
V12: selected.V12,
V13: selected.V13,
V14: selected.V14,
V15: selected.V15,
V16: selected.V16,
V17: selected.V17,
V18: selected.V18,
V19: selected.V19,
V20: selected.V20,
V21: selected.V21,
V22: selected.V22,
V23: selected.V23,
V24: selected.V24,
V25: selected.V25,
V26: selected.V26,
V27: selected.V27,
V28: selected.V28,
Amount: selected.Amount
})
});
const data = await response.json();
setResult(data);
await loadTransactions();
await loadStats();
await loadAnalytics();
} catch (error) {
  console.error("Fraud analysis failed:", error);
  alert("Could not connect to TrustLedger API. Check the browser console.");
} finally {
  setLoading(false);
}

};
const getRiskClass = (risk) => {
if (risk === "LOW") return "risk-low";
if (risk === "MEDIUM") return "risk-medium";
return "risk-high";
};
return (
<div className="app">
<header className="hero">
<div className="hero-badge">AI FRAUD DETECTION PLATFORM</div>
<h1>TrustLedger</h1>
<p>Intelligent transaction monitoring and risk assessment powered by machine learning.</p>
<div className="hero-status"><span className="status-dot"></span>System Online</div>
</header>
<main>
<section className="section-block">
<div className="section-heading"><span>01</span><div><h2>Risk Overview</h2><p>Real-time summary of analyzed transactions</p></div></div>
<div className="stats">
<div className="stat-card"><div className="stat-icon">Σ</div><h3>Total Transactions</h3><strong>{stats.total}</strong></div>
<div className="stat-card low-card"><div className="stat-icon">✓</div><h3>Low Risk</h3><strong>{stats.low}</strong></div>
<div className="stat-card medium-card"><div className="stat-icon">!</div><h3>Medium Risk</h3><strong>{stats.medium}</strong></div>
<div className="stat-card high-card"><div className="stat-icon">!</div><h3>High Risk</h3><strong>{stats.high}</strong></div>
</div>
</section>
{metrics && (
<section className="section-block">
<div className="section-heading"><span>02</span><div><h2>Model Performance</h2><p>Evaluation results on the held-out test dataset</p></div></div>
<div className="metrics">
<div className="metric-card"><h3>Accuracy</h3><strong>{metrics.accuracy}%</strong></div>
<div className="metric-card"><h3>Precision</h3><strong>{metrics.precision}%</strong></div>
<div className="metric-card"><h3>Recall</h3><strong>{metrics.recall}%</strong></div>
<div className="metric-card"><h3>F1 Score</h3><strong>{metrics.f1_score}%</strong></div>
<div className="metric-card"><h3>ROC-AUC</h3><strong>{metrics.roc_auc}%</strong></div>
</div>
</section>
)}
{comparison && (
<section className="section-block">
<div className="section-heading"><span>03</span><div><h2>Model Comparison</h2><p>Comparing candidate models before deployment</p></div></div>
<div className="comparison-table">
<div className="comparison-header"><strong>Metric</strong><strong>Logistic Regression</strong><strong>Random Forest</strong></div>
<div className="comparison-row"><span>Accuracy</span><span>{comparison.models["Logistic Regression"].accuracy}%</span><span className="best-value">{comparison.models["Random Forest"].accuracy}%</span></div>
<div className="comparison-row"><span>Precision</span><span>{comparison.models["Logistic Regression"].precision}%</span><span className="best-value">{comparison.models["Random Forest"].precision}%</span></div>
<div className="comparison-row"><span>Recall</span><span className="best-value">{comparison.models["Logistic Regression"].recall}%</span><span>{comparison.models["Random Forest"].recall}%</span></div>
<div className="comparison-row"><span>F1 Score</span><span>{comparison.models["Logistic Regression"].f1_score}%</span><span className="best-value">{comparison.models["Random Forest"].f1_score}%</span></div>
<div className="comparison-row"><span>ROC-AUC</span><span className="best-value">{comparison.models["Logistic Regression"].roc_auc}%</span><span>{comparison.models["Random Forest"].roc_auc}%</span></div>
</div>
<div className="selected-model"><span className="selected-dot"></span>Selected Production Model: <strong>{comparison.selected_model}</strong></div>
</section>
)}
{featureImportance && (
<section className="section-block">
<div className="section-heading"><span>04</span><div><h2>Feature Importance</h2><p>Top features influencing the Random Forest model</p></div></div>
<div className="feature-card">
{featureImportance.features.map((item, index) => (
<div className="feature-row" key={item.feature}>
<div className="feature-name"><span className="feature-rank">{String(index + 1).padStart(2, "0")}</span><strong>{item.feature}</strong><span className="feature-percent">{item.importance}%</span></div>
<div className="feature-bar-background"><div className="feature-bar" style={{ width: `${item.importance}%` }} /></div>
</div>
))}
</div>
</section>
)}
{analytics && (
<section className="section-block">
<div className="section-heading"><span>05</span><div><h2>Transaction Analytics</h2><p>Dataset and model evaluation insights</p></div></div>
<div className="analytics-card">
<h3>Risk Distribution</h3>
<div className="risk-row"><span>Low Risk</span><div className="risk-bar-background"><div className="risk-bar low-risk-bar" style={{ width: `${stats.total > 0 ? (stats.low / stats.total) * 100 : 0}%` }}>{stats.low}</div></div></div>
<div className="risk-row"><span>Medium Risk</span><div className="risk-bar-background"><div className="risk-bar medium-risk-bar" style={{ width: `${stats.total > 0 ? (stats.medium / stats.total) * 100 : 0}%` }}>{stats.medium}</div></div></div>
<div className="risk-row"><span>High Risk</span><div className="risk-bar-background"><div className="risk-bar high-risk-bar" style={{ width: `${stats.total > 0 ? (stats.high / stats.total) * 100 : 0}%` }}>{stats.high}</div></div></div>
</div>
<div className="analytics-card">
<h3>Fraud vs Normal Transactions</h3>
<div className="bar-row"><span>Normal</span><div className="bar-background"><div className="bar normal-bar" style={{ width: `${(analytics.normal_count / (analytics.normal_count + analytics.fraud_count)) * 100}%` }}>{analytics.normal_count}</div></div></div>
<div className="bar-row"><span>Fraud</span><div className="bar-background"><div className="bar fraud-bar" style={{ width: `${(analytics.fraud_count / (analytics.normal_count + analytics.fraud_count)) * 100}%` }}>{analytics.fraud_count}</div></div></div>
</div>
<div className="analytics-card">
<h3>Confusion Matrix</h3>
<div className="confusion-matrix">
<div></div><strong>Predicted Normal</strong><strong>Predicted Fraud</strong>
<strong>Actual Normal</strong>
<div className="matrix-cell tn"><span>TN</span>{analytics.confusion_matrix.true_negative}</div>
<div className="matrix-cell fp"><span>FP</span>{analytics.confusion_matrix.false_positive}</div>
<strong>Actual Fraud</strong>
<div className="matrix-cell fn"><span>FN</span>{analytics.confusion_matrix.false_negative}</div>
<div className="matrix-cell tp"><span>TP</span>{analytics.confusion_matrix.true_positive}</div>
</div>
</div>
</section>
)}
<section className="analysis-section">
<div className="section-heading"><span>06</span><div><h2>Analyze a Transaction</h2><p>Run a transaction through the fraud detection model</p></div></div>
<div className="analysis-card">
<div className="analysis-left">
<div className="input-label">Select Transaction</div>
<select value={samples.indexOf(selected)} onChange={(e) => setSelected(samples[Number(e.target.value)])}>
{samples.map((transaction, index) => (
<option key={index} value={index}>Transaction {index + 1} — ₹{transaction.Amount.toFixed(2)}</option>
))}
</select>
{selected && (
<div className="transaction-info">
<div><span>Transaction Amount</span><strong>₹{selected.Amount.toFixed(2)}</strong></div>
<div><span>Dataset Label</span><strong>{selected.Class === 1 ? "Fraud" : "Normal"}</strong></div>
</div>
)}
<button onClick={analyzeTransaction} disabled={loading}>{loading ? "Analyzing Transaction..." : "Run Fraud Analysis →"}</button>
</div>
<div className="analysis-result">
{!result ? (
<div className="empty-result"><div className="empty-icon">◎</div><h3>Awaiting Analysis</h3><p>Select a transaction and run the model to generate a risk assessment.</p></div>
) : (
<div className="result-content">
<span className="result-label">TRUST SCORE</span>
<div className="score">{result.trust_score}<span>/100</span></div>
<div className="probability"><span>Fraud Probability</span><strong>{result.fraud_probability}%</strong></div>
<div className={`risk-badge ${getRiskClass(result.risk_level)}`}>{result.risk_level} RISK</div>
</div>
)}
</div>
</div>
</section>
</main>
<section className="history">
<div className="section-heading"><span>07</span><div><h2>Transaction History</h2><p>Previously analyzed transactions</p></div></div>
{transactions.length === 0 ? (
<div className="no-transactions">No transactions analyzed yet.</div>
) : (
<div className="table-wrapper">
<table>
<thead><tr><th>ID</th><th>Amount</th><th>Fraud Probability</th><th>Trust Score</th><th>Risk</th></tr></thead>
<tbody>
{transactions.map((transaction) => (
<tr key={transaction.id}>
<td>#{transaction.id}</td>
<td>₹{transaction.amount.toFixed(2)}</td>
<td>{transaction.fraud_probability}%</td>
<td>{transaction.trust_score}</td>
<td><span className={`table-risk ${getRiskClass(transaction.risk_level)}`}>{transaction.risk_level}</span></td>
</tr>
))}
</tbody>
</table>
</div>
)}
</section>
<footer><p>TrustLedger • AI-Powered Financial Fraud Detection</p></footer>
</div>
);
}
export default App;