import React, { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// -----------------------------------------------------------------------------
// Rakhsh Dashboard — WebSocket & plain React version
// - No shadcn/ui dependency
// - Real-time data via WebSocket
// - Inline HTML-ready for Vite build
// - Handles redirect with feedback from target module
// -----------------------------------------------------------------------------

const WS_URL = "ws://localhost:8080/ws"; // replace with real source

function renderStatusBadge(status) {
  const map = {
    ok: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    error: "bg-red-100 text-red-800",
    blocked: "bg-gray-800 text-white",
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${map[status] || map.ok}`}>{status}</span>
  );
}

export default function RakhshDashboard({ onRedirect }) {
  const [machines, setMachines] = useState([]);
  const [log, setLog] = useState([]);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [redirectTarget, setRedirectTarget] = useState("");
  const [liveChartData, setLiveChartData] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (Array.isArray(data)) {
          setMachines(data);
          const total = data.reduce((s, x) => s + x.throughput, 0);
          setLiveChartData((d) => [...d, { ts: new Date().toLocaleTimeString(), total }].slice(-30));
        }
      } catch (e) {
        console.error("WS parse error", e);
      }
    };
    ws.onerror = (err) => console.error("WS error", err);
    return () => ws.close();
  }, []);

  const filtered = useMemo(() => {
    return machines.filter((m) => {
      if (filter !== "all" && m.status !== filter) return false;
      if (search && !`${m.name} ${m.id}`.toLowerCase().includes(search.toLowerCase())) return false;
      return true;
    });
  }, [machines, search, filter]);

  function detectBottlenecks() {
    return machines
      .filter((m) => m.queue >= 8 || m.throughput <= 3 || m.temp > 85)
      .sort((a, b) => b.queue - a.queue)
      .slice(0, 6);
  }

  async function sendOutputToTarget(payload) {
    if (onRedirect && typeof onRedirect === "function") {
      try {
        const result = await onRedirect(redirectTarget, payload);
        setLog((L) => [{ ts: Date.now(), id: "SYS", text: `Redirect callback result: ${JSON.stringify(result)}` }, ...L].slice(0, 200));
      } catch (e) {
        setLog((L) => [{ ts: Date.now(), id: "ERR", text: `Callback error: ${String(e)}` }, ...L].slice(0, 200));
      }
      return;
    }

    if (!redirectTarget) {
      setLog((L) => [{ ts: Date.now(), id: "WARN", text: `Redirect target not set` }, ...L].slice(0, 200));
      return;
    }

    try {
      const res = await fetch(redirectTarget, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const text = await res.text();
      setLog((L) => [{ ts: Date.now(), id: "SYS", text: `Posted to ${redirectTarget}, response: ${text}` }, ...L].slice(0, 200));
    } catch (e) {
      setLog((L) => [{ ts: Date.now(), id: "ERR", text: `POST failed: ${String(e)}` }, ...L].slice(0, 200));
    }
  }

  return (
    <div className="p-4 max-w-7xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Rakhsh — Панель управления (Душанбе)</h1>

      <div className="flex items-center gap-3 mb-4">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Поиск по станкам..."
          className="border rounded px-2 py-1 text-sm flex-1"
        />
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="border rounded px-2 py-1 text-sm">
          <option value="all">Все</option>
          <option value="ok">OK</option>
          <option value="warning">Warning</option>
          <option value="error">Error</option>
          <option value="blocked">Blocked</option>
        </select>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2 grid grid-cols-2 gap-4">
          {filtered.map((m) => (
            <motion.div key={m.id} layout className={`p-3 rounded-lg shadow-sm border bg-white ${m.status === 'error' ? 'border-red-300' : ''}`}>
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-sm text-gray-500">{m.id}</div>
                  <div className="text-lg font-semibold">{m.name}</div>
                </div>
                {renderStatusBadge(m.status)}
              </div>
              <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                <div className="flex flex-col">
                  <span className="text-xs text-gray-400">Производительность</span>
                  <span className="font-medium">{m.throughput} u/min</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-gray-400">Очередь</span>
                  <span className={`font-medium ${m.queue > 10 ? 'text-red-600' : ''}`}>{m.queue}</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-gray-400">Темп.</span>
                  <span className={`font-medium ${m.temp > 85 ? 'text-red-600' : ''}`}>{m.temp}°C</span>
                </div>
              </div>
              <div className="mt-3 flex gap-2">
                <button className="px-2 py-1 bg-blue-600 text-white rounded text-sm" onClick={() => sendOutputToTarget({ machine: m, ts: Date.now() })}>Отправить в модуль</button>
              </div>
            </motion.div>
          ))}
        </div>

        <aside className="flex flex-col gap-4">
          <div className="p-3 border rounded">
            <h2 className="font-semibold mb-2">Суммарная производительность</h2>
            <div style={{ height: 160 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={liveChartData}>
                  <XAxis dataKey="ts" hide />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="total" stroke="#8884d8" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="p-3 border rounded">
            <h2 className="font-semibold mb-2">Пробки / Бутылочные места</h2>
            {detectBottlenecks().length === 0 && <div className="text-sm text-gray-500">Спокойно — явных проблем нет.</div>}
            {detectBottlenecks().map((b) => (
              <div key={b.id} className="flex justify-between items-center mb-1">
                <div>
                  <div className="font-medium">{b.name} <span className="text-xs text-gray-400">{b.id}</span></div>
                  <div className="text-xs text-gray-500">Очередь: {b.queue} • Темп: {b.temp}°C</div>
                </div>
                <button className="px-2 py-1 bg-yellow-600 text-white rounded text-xs" onClick={() => sendOutputToTarget({ alert: 'bottleneck', machine: b })}>Перенаправить</button>
              </div>
            ))}
          </div>

          <div className="p-3 border rounded">
            <h2 className="font-semibold mb-2">Перенаправление выхода</h2>
            <input
              placeholder="http://localhost:5000/module-endpoint"
              value={redirectTarget}
              onChange={(e) => setRedirectTarget(e.target.value)}
              className="border rounded px-2 py-1 text-sm w-full mb-2"
            />
            <div className="flex gap-2">
              <button className="px-2 py-1 bg-blue-600 text-white rounded text-sm" onClick={() => sendOutputToTarget({ summary: machines })}>Отправить снимок всех</button>
              <button className="px-2 py-1 border rounded text-sm" onClick={() => setRedirectTarget(redirectTarget || 'http://localhost:5000/ingest')}>Выбрать дефолт</button>
            </div>
          </div>

          <div className="p-3 border rounded">
            <h2 className="font-semibold mb-2">Журнал событий</h2>
            <div className="max-h-48 overflow-y-auto text-sm space-y-1">
              {log.length === 0 && <div className="text-gray-500">Журнал пуст</div>}
              {log.map((l, i) => (
                <div key={i} className="flex justify-between items-center border-b py-1">
                  <div>
                    <div className="font-medium text-xs">{l.id}</div>
                    <div className="text-xs text-gray-600">{l.text}</div>
                  </div>
                  <div className="text-xs text-gray-400">{new Date(l.ts).toLocaleTimeString()}</div>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
