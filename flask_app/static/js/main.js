/* ========================================================================
   main.js  –  Mustafa AI Travel Concierge
   GSAP animations + particle canvas + chat + Leaflet map + PDF + prefs
   ======================================================================== */

'use strict';

gsap.registerPlugin(ScrollTrigger);


/* ── 1. Particle background ──────────────────────────────────────────── */
(function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H, particles;

    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
    function createParticles(n = 70) {
        particles = Array.from({ length: n }, () => ({
            x: Math.random() * W, y: Math.random() * H,
            r: Math.random() * 1.5 + 0.5,
            dx: (Math.random() - 0.5) * 0.3, dy: (Math.random() - 0.5) * 0.3,
            alpha: Math.random() * 0.4 + 0.1,
        }));
    }
    function draw() {
        ctx.clearRect(0, 0, W, H);
        for (const p of particles) {
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 215, 0, ${p.alpha})`; ctx.fill();
            p.x += p.dx; p.y += p.dy;
            if (p.x < 0 || p.x > W) p.dx *= -1;
            if (p.y < 0 || p.y > H) p.dy *= -1;
        }
        requestAnimationFrame(draw);
    }
    window.addEventListener('resize', () => { resize(); createParticles(); });
    resize(); createParticles(); draw();
})();


/* ── 2. Hero entrance animation ──────────────────────────────────────── */
(function heroEntrance() {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    tl.to('#hero-badge', { opacity: 1, y: 0, duration: 0.6, delay: 0.3 })
        .to('#hero-title', { opacity: 1, y: 0, duration: 0.8 }, '-=0.3')
        .to('#hero-sub', { opacity: 1, y: 0, duration: 0.7 }, '-=0.5')
        .to('#cta-btn', { opacity: 1, y: 0, duration: 0.6 }, '-=0.4');

    gsap.to('#cta-btn', { y: -8, duration: 2.5, ease: 'sine.inOut', repeat: -1, yoyo: true, delay: 1.5 });
})();


/* ── 3. Feature cards scroll entrance (staggered) ────────────────────── */
(function featureCards() {
    gsap.set('.feature-card', { y: 40 });
    gsap.to('.feature-card', {
        opacity: 1, y: 0, duration: 0.7, stagger: 0.12, ease: 'power3.out',
        scrollTrigger: { trigger: '#features-grid', start: 'top 80%' },
    });
})();


/* ── 4. Leaflet Map ──────────────────────────────────────────────────── */
let travelMap = null;
let mapMarkers = [];

function initMap() {
    if (travelMap) return;
    travelMap = L.map('travel-map', { scrollWheelZoom: false }).setView([30, 10], 2);

    // Dark theme tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
    }).addTo(travelMap);
}

function clearMapMarkers() {
    mapMarkers.forEach(m => travelMap.removeLayer(m));
    mapMarkers = [];
}

/**
 * Build a gold-styled icon for map markers.
 */
function goldIcon() {
    return L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-gold.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41],
    });
}

/**
 * Extract latitude/longitude pairs from the AI response text and drop pins.
 * Supports multiple formats:
 *   - "latitude": 48.856, "longitude": 2.352
 *   - lat: 48.856, lng: 2.352
 *   - (48.856, 2.352)
 *   - Explicit coordinate blocks from tool output
 */
function extractAndPlotLocations(text) {
    initMap();
    clearMapMarkers();

    const coords = [];

    // Pattern 1: JSON-like keys  "latitude": ..., "longitude": ...
    const jsonRe = /"latitude"\s*:\s*(-?\d+\.?\d*)\s*,\s*"longitude"\s*:\s*(-?\d+\.?\d*)/gi;
    let m;
    while ((m = jsonRe.exec(text)) !== null) {
        coords.push({ lat: parseFloat(m[1]), lng: parseFloat(m[2]) });
    }

    // Pattern 2: key-value  lat: ..., lng: ...
    const kvRe = /lat(?:itude)?\s*[:=]\s*(-?\d+\.?\d*)\s*[,;]\s*l(?:on|ng|ong)(?:itude)?\s*[:=]\s*(-?\d+\.?\d*)/gi;
    while ((m = kvRe.exec(text)) !== null) {
        coords.push({ lat: parseFloat(m[1]), lng: parseFloat(m[2]) });
    }

    // Pattern 3: Parenthesised coords  (lat, lng)
    const parenRe = /\(\s*(-?\d{1,3}\.\d{2,})\s*,\s*(-?\d{1,3}\.\d{2,})\s*\)/g;
    while ((m = parenRe.exec(text)) !== null) {
        const lat = parseFloat(m[1]);
        const lng = parseFloat(m[2]);
        if (Math.abs(lat) <= 90 && Math.abs(lng) <= 180) {
            coords.push({ lat, lng });
        }
    }

    // Dedupe by rounding to 4 decimals
    const seen = new Set();
    const unique = [];
    for (const c of coords) {
        const key = `${c.lat.toFixed(4)},${c.lng.toFixed(4)}`;
        if (!seen.has(key)) { seen.add(key); unique.push(c); }
    }

    if (unique.length === 0) {
        document.getElementById('map-empty').classList.remove('hidden');
        return;
    }

    document.getElementById('map-empty').classList.add('hidden');

    // Try to extract place names near each coordinate from the text
    unique.forEach((c, i) => {
        const marker = L.marker([c.lat, c.lng], { icon: goldIcon() })
            .addTo(travelMap)
            .bindPopup(`<strong>📍 Location ${i + 1}</strong><br>Lat: ${c.lat}<br>Lng: ${c.lng}`);
        mapMarkers.push(marker);
    });

    // Fit map to all markers
    if (unique.length === 1) {
        travelMap.setView([unique[0].lat, unique[0].lng], 13);
    } else {
        const group = L.featureGroup(mapMarkers);
        travelMap.fitBounds(group.getBounds().pad(0.15));
    }

    // GSAP animate map section
    gsap.from('#map-section', { opacity: 0, y: 30, duration: 0.6, ease: 'power2.out' });
}


/* ── 5. Chat interface ────────────────────────────────────────────────── */
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const sendIcon = document.getElementById('send-icon');
const sendSpinner = document.getElementById('send-spinner');
const statusBar = document.getElementById('status-bar');
const exportBar = document.getElementById('export-bar');

let isLoading = false;
let lastBotAnswer = '';   // stored for PDF export

function scrollToBottom() {
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function appendUserMessage(text) {
    const w = document.createElement('div');
    w.className = 'flex gap-3 items-start justify-end';
    w.innerHTML = `<div class="chat-bubble-user">${escapeHtml(text)}</div><div class="avatar-user shrink-0">👤</div>`;
    chatMessages.appendChild(w);
    scrollToBottom();
}

function appendBotMessage(markdown) {
    const w = document.createElement('div');
    w.className = 'flex gap-3 items-start';
    const html = typeof marked !== 'undefined' ? marked.parse(markdown) : escapeHtml(markdown).replace(/\n/g, '<br>');
    w.innerHTML = `<div class="avatar-bot shrink-0">✈</div><div class="chat-bubble-bot glass-card-inner rounded-2xl rounded-tl-sm p-4 text-sm text-white/80 leading-relaxed max-w-[90%] overflow-auto md-content">${html}</div>`;
    chatMessages.appendChild(w);
    scrollToBottom();
    gsap.from(w, { opacity: 0, x: -12, duration: 0.4, ease: 'power2.out' });
}

function showTypingIndicator() {
    const el = document.createElement('div');
    el.id = 'typing-indicator';
    el.className = 'flex gap-3 items-start';
    el.innerHTML = `<div class="avatar-bot shrink-0">✈</div><div class="glass-card-inner rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-1.5"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>`;
    chatMessages.appendChild(el);
    scrollToBottom();
}
function hideTypingIndicator() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

function setLoading(loading) {
    isLoading = loading;
    sendBtn.disabled = loading;
    chatInput.disabled = loading;
    sendIcon.classList.toggle('hidden', loading);
    sendSpinner.classList.toggle('hidden', !loading);
    statusBar.classList.toggle('hidden', !loading);
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

async function sendQuery(question) {
    if (!question.trim() || isLoading) return;
    appendUserMessage(question);
    setLoading(true);
    showTypingIndicator();

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });
        hideTypingIndicator();
        const data = await response.json();

        if (response.ok && data.answer) {
            lastBotAnswer = data.answer;
            appendBotMessage(data.answer);
            exportBar.classList.remove('hidden');

            // Try to extract coordinates and plot on map
            extractAndPlotLocations(data.answer);
        } else {
            appendBotMessage(`⚠️ **Error:** ${data.error || 'An unknown error occurred.'}`);
        }
    } catch (err) {
        hideTypingIndicator();
        appendBotMessage('⚠️ **Connection error.** Please ensure both the Flask and FastAPI servers are running.');
    } finally {
        setLoading(false);
    }
}

sendBtn.addEventListener('click', () => {
    const q = chatInput.value.trim();
    if (!q) return;
    chatInput.value = '';
    sendQuery(q);
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const q = chatInput.value.trim();
        if (!q) return;
        chatInput.value = '';
        sendQuery(q);
    }
});

function fillSuggestion(el) {
    const text = el.textContent.replace(/[🗼🗾🌅🦁]/gu, '').trim();
    chatInput.value = `Plan a trip: ${text}`;
    chatInput.focus();
    document.getElementById('chat').scrollIntoView({ behavior: 'smooth' });
}


/* ── 6. PDF Export ────────────────────────────────────────────────────── */
async function exportPdf() {
    if (!lastBotAnswer) return;

    const btn = document.getElementById('export-pdf-btn');
    btn.textContent = '⏳ Generating…';
    btn.disabled = true;

    try {
        const response = await fetch('/export_pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: lastBotAnswer }),
        });

        if (!response.ok) {
            const err = await response.json();
            alert('PDF Error: ' + (err.error || 'Unknown error'));
            return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'travel_plan.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
    } catch (err) {
        alert('Could not generate PDF. Ensure the server is running.');
    } finally {
        btn.innerHTML = '📄 Export as PDF';
        btn.disabled = false;
    }
}


/* ── 7. Preferences Modal ─────────────────────────────────────────────── */
function openPrefsModal() {
    document.getElementById('prefs-modal').classList.remove('hidden');
    loadPrefs();
}
function closePrefsModal() {
    document.getElementById('prefs-modal').classList.add('hidden');
}

async function loadPrefs() {
    const list = document.getElementById('prefs-list');
    list.innerHTML = '<p class="text-white/30 text-xs">Loading…</p>';

    try {
        const res = await fetch('/preferences');
        const data = await res.json();
        const prefs = data.preferences || [];

        if (prefs.length === 0) {
            list.innerHTML = '<p class="text-white/30 text-xs">No preferences saved yet.</p>';
            return;
        }

        list.innerHTML = '';
        prefs.forEach(p => {
            const chip = document.createElement('div');
            chip.className = 'pref-chip';
            chip.innerHTML = `<span><span class="pref-key">${escapeHtml(p.key)}</span>: ${escapeHtml(p.value)}</span><button onclick="deletePref('${escapeHtml(p.key)}')" title="Delete">✕</button>`;
            list.appendChild(chip);
        });
    } catch {
        list.innerHTML = '<p class="text-red-400 text-xs">Could not load preferences.</p>';
    }
}

async function savePref() {
    const key = document.getElementById('pref-key').value.trim();
    const val = document.getElementById('pref-val').value.trim();
    if (!key || !val) return;

    try {
        await fetch('/preferences', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key, value: val }),
        });
        document.getElementById('pref-key').value = '';
        document.getElementById('pref-val').value = '';
        loadPrefs();
    } catch {
        alert('Could not save preference.');
    }
}

async function deletePref(key) {
    // The Flask app doesn't have a DELETE relay yet, so we just inform
    alert(`To delete "${key}", please use the API directly for now.`);
}


/* ── 8. Smooth nav scroll highlight ─────────────────────────────────── */
(function navHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const links = document.querySelectorAll('nav a[href^="#"]');

    const obs = new IntersectionObserver((entries) => {
        for (const entry of entries) {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                links.forEach(a => {
                    const active = a.getAttribute('href') === `#${id}`;
                    a.style.color = active ? '#FFD700' : '';
                });
            }
        }
    }, { rootMargin: '-40% 0px -55% 0px' });

    sections.forEach(s => obs.observe(s));
})();


/* ── 9. Init map on load ──────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    initMap();
});
