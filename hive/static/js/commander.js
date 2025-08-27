// commander.js
function launchCyberWar() {
  const ip = document.getElementById('target-ip').value;
  if (!ip) { alert("Masukkan IP!"); return; }
  const logDiv = document.getElementById('war-log');
  logDiv.innerHTML = '⚔️ Memulai operasi perang digital...';

  fetch('/api/retaliate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ip: ip, key: 'watcher123' })
  })
  .then(r => r.json())
  .then(data => {
    logDiv.innerHTML += '<p>✅ Operasi selesai. Musuh dinetralisir.</p>';
  })
  .catch(e => {
    logDiv.innerHTML += `<p>❌ Gagal: ${e.message}</p>`;
  });
}

// Fungsi lain: scanZombie, activateSwitch, dll → seperti sebelumnya