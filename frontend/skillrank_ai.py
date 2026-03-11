import streamlit as st
import requests
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SKILLRANK AI",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');

html, body, .stApp {
    background: #060912 !important;
    color: #e8eaf6 !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 10% 10%, rgba(0,255,200,0.05) 0%, transparent 55%),
        radial-gradient(ellipse 60% 60% at 90% 90%, rgba(100,0,255,0.06) 0%, transparent 55%),
        #060912;
    z-index: 0;
    pointer-events: none;
}
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 1rem 2rem 2rem !important; max-width: 100% !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: rgba(6,9,18,0.98) !important;
    border-right: 1px solid rgba(255,215,0,0.1) !important;
}
section[data-testid="stSidebar"] > div { padding: 2rem 1.2rem !important; }

/* ── HERO ── */
.hero-wrap { text-align: center; padding: 32px 0 20px; }
.trophy-orb {
    display: inline-flex; align-items: center; justify-content: center;
    width: 64px; height: 64px; border-radius: 18px;
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    font-size: 32px; margin-bottom: 12px;
    box-shadow: 0 0 40px rgba(255,180,0,0.55), 0 0 80px rgba(255,180,0,0.18);
    animation: trophyPulse 2.5s ease-in-out infinite;
}
@keyframes trophyPulse {
    0%,100% { box-shadow: 0 0 30px rgba(255,180,0,0.45), 0 0 60px rgba(255,180,0,0.12); }
    50%      { box-shadow: 0 0 60px rgba(255,180,0,0.85), 0 0 120px rgba(255,180,0,0.3); }
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(32px, 5vw, 64px); font-weight: 900;
    background: linear-gradient(135deg, #ffd700 0%, #00ffb4 50%, #7b61ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    letter-spacing: 6px; line-height: 1.1; margin-bottom: 8px;
}
.hero-tagline {
    font-family: 'Space Mono', monospace; font-size: 10px;
    color: rgba(200,220,255,0.45); letter-spacing: 5px; text-transform: uppercase; margin-bottom: 4px;
}
.hero-sub {
    font-family: 'Space Mono', monospace; font-size: 11px; color: #00ffb4; letter-spacing: 2px; opacity: 0.75;
}

/* ── SECTION LABELS ── */
.section-label {
    font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 4px;
    text-transform: uppercase; color: #ffd700; margin: 20px 0 10px;
    display: flex; align-items: center; gap: 10px;
}
.section-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(to right, rgba(255,215,0,0.3), transparent);
}

/* ── SCORE RING CARD ── */
.score-ring-wrap {
    display: flex; flex-direction: column; align-items: center; gap: 5px;
    padding: 20px 12px; background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,215,0,0.12); border-radius: 18px;
}
.score-ring-svg { filter: drop-shadow(0 0 12px rgba(255,215,0,0.35)); }
.score-value {
    font-family: 'Orbitron', monospace; font-size: 38px; font-weight: 900;
    color: #ffd700; text-align: center; line-height: 1;
}
.score-label {
    font-family: 'Space Mono', monospace; font-size: 9px;
    letter-spacing: 3px; color: rgba(200,220,255,0.45); text-transform: uppercase;
}
.rank-title { font-family: 'Orbitron', monospace; font-size: 13px; font-weight: 700; letter-spacing: 3px; margin-top: 2px; }
.prog-wrap { height: 5px; background: rgba(255,255,255,0.05); border-radius: 99px; overflow: hidden; width: 100%; margin-top: 4px; }
.prog-fill { height: 100%; border-radius: 99px; background: linear-gradient(to right, #00ffb4, #ffd700); }

/* ── METRIC MINI ── */
.metric-mini {
    padding: 12px 14px; background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06); border-radius: 12px;
    text-align: center; margin-bottom: 8px;
}
.metric-mini-val { font-family: 'Orbitron', monospace; font-size: 20px; font-weight: 700; }
.metric-mini-label {
    font-family: 'Space Mono', monospace; font-size: 8px;
    letter-spacing: 2px; color: rgba(200,220,255,0.35); text-transform: uppercase; margin-top: 3px;
}

/* ── RANK LADDER ── */
.rank-row {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 10px; border-radius: 9px; margin-bottom: 4px;
    font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 1px;
}
.rank-row-active { background: rgba(255,215,0,0.08); border: 1px solid rgba(255,215,0,0.25); }
.rank-row-done   { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); opacity: 0.5; }
.rank-row-locked { background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); opacity: 0.25; }

/* ── BADGE CHIPS ── */
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 5px 11px; border-radius: 8px;
    font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 1px;
    margin: 3px; border: 1px solid;
}
.badge-earned { background: rgba(255,215,0,0.07); border-color: rgba(255,215,0,0.28); color: #ffd700; }
.badge-locked { background: rgba(255,255,255,0.01); border-color: rgba(255,255,255,0.05); color: rgba(200,220,255,0.2); }

/* ── CHAT HEADER BAR ── */
.chat-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px; background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06); border-bottom: none;
    border-radius: 16px 16px 0 0;
}
.chat-header-title { font-family: 'Orbitron', monospace; font-size: 12px; font-weight: 700; letter-spacing: 3px; color: #00ffb4; }
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #00ffb4; display: inline-block; margin-right: 8px; animation: blink 1.2s step-end infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.15} }

/* ── SCORE FLASH BANNER ── */
.score-banner {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 18px; background: rgba(255,215,0,0.06);
    border: 1px solid rgba(255,215,0,0.2); border-radius: 10px; margin-bottom: 12px;
    font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 1px;
}
.score-gained { color: #00ffb4; font-weight: 700; font-family: 'Orbitron', monospace; }
.score-total  { color: #ffd700; font-weight: 700; font-family: 'Orbitron', monospace; }

/* ── Streamlit chat bubbles ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.015) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,255,180,0.25) !important;
    border-radius: 12px !important;
    color: #e8eaf6 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 16px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(0,255,180,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,255,180,0.07) !important;
}
[data-testid="stChatInput"] button {
    background: rgba(0,255,180,0.15) !important;
    border-radius: 10px !important;
    color: #00ffb4 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: rgba(200,220,255,0.6) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    padding: 10px 18px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(255,80,80,0.08) !important;
    border-color: rgba(255,80,80,0.25) !important;
    color: #ff6b6b !important;
}

/* ── Error ── */
[data-testid="stAlert"] {
    background: rgba(255,80,80,0.07) !important;
    border: 1px solid rgba(255,80,80,0.2) !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SESSION STATE  (mandatory fields preserved from original)
# ════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "score" not in st.session_state:
    st.session_state.score = 0
# Extra UI-only state
if "last_score_added" not in st.session_state:
    st.session_state.last_score_added = 0
if "interactions" not in st.session_state:
    st.session_state.interactions = 0

# ── Rank helpers ──────────────────────────────────────────────────────────────
RANKS = [
    (0,    "NOVICE",     "#64748b"),
    (150,  "APPRENTICE", "#22d3ee"),
    (350,  "SCHOLAR",    "#a78bfa"),
    (600,  "EXPERT",     "#f59e0b"),
    (900,  "MASTER",     "#ef4444"),
    (1200, "LEGEND",     "#ffd700"),
]

def get_rank(score):
    r = RANKS[0]
    for t, n, c in RANKS:
        if score >= t:
            r = (t, n, c)
    return r

def rank_progress(score):
    ci = 0
    for i, (t, n, c) in enumerate(RANKS):
        if score >= t:
            ci = i
    if ci == len(RANKS) - 1:
        return 100
    return int((score - RANKS[ci][0]) / (RANKS[ci+1][0] - RANKS[ci][0]) * 100)

def rank_svg(score):
    prog   = rank_progress(score)
    radius = 48
    circ   = 2 * math.pi * radius
    dash   = circ * prog / 100
    gap    = circ - dash
    return f"""<svg width="120" height="120" viewBox="0 0 120 120" class="score-ring-svg">
      <circle cx="60" cy="60" r="{radius}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="9"/>
      <circle cx="60" cy="60" r="{radius}" fill="none" stroke="url(#rg)" stroke-width="9"
        stroke-dasharray="{dash:.1f} {gap:.1f}" stroke-dashoffset="{circ/4:.1f}" stroke-linecap="round"/>
      <defs>
        <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#00ffb4"/>
          <stop offset="100%" stop-color="#ffd700"/>
        </linearGradient>
      </defs>
    </svg>"""

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    score = st.session_state.score
    rinfo = get_rank(score)
    prog  = rank_progress(score)

    # Score ring
    st.markdown(f"""
    <div class="score-ring-wrap">
      {rank_svg(score)}
      <div class="score-value">{score}</div>
      <div class="score-label">CURIOSITY XP</div>
      <div class="rank-title" style="color:{rinfo[2]}">{rinfo[1]}</div>
      <div class="prog-wrap">
        <div class="prog-fill" style="width:{prog}%"></div>
      </div>
      <div style="font-family:'Space Mono',monospace; font-size:9px;
           color:rgba(200,220,255,0.3); margin-top:4px;">{prog}% to next rank</div>
    </div>
    """, unsafe_allow_html=True)

    # Mini stats
    st.markdown('<div class="section-label">▸ SESSION</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="metric-mini">
          <div class="metric-mini-val" style="color:#00ffb4">{st.session_state.interactions}</div>
          <div class="metric-mini-label">Messages</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-mini">
          <div class="metric-mini-val" style="color:#ff6348">+{st.session_state.last_score_added}</div>
          <div class="metric-mini-label">Last XP</div></div>""", unsafe_allow_html=True)

    # Rank ladder
    st.markdown('<div class="section-label">▸ RANK LADDER</div>', unsafe_allow_html=True)
    for t, n, c in RANKS:
        if score >= t and get_rank(score)[1] == n:
            cls = "rank-row-active"; icon = "▶"
        elif score >= t:
            cls = "rank-row-done";   icon = "✓"
        else:
            cls = "rank-row-locked"; icon = "🔒"
        st.markdown(f"""
        <div class="rank-row {cls}">
          <span>{icon}</span>
          <span style="color:{c}; font-weight:700; letter-spacing:2px;">{n}</span>
          <span style="margin-left:auto; opacity:0.5;">{t} XP</span>
        </div>""", unsafe_allow_html=True)

    # Badges
    st.markdown('<div class="section-label">▸ BADGES</div>', unsafe_allow_html=True)
    badges = [
        ("⚡", "FIRST STEP",   st.session_state.interactions >= 1),
        ("🧠", "THINKER",      st.session_state.score >= 100),
        ("🔥", "ON FIRE",      st.session_state.interactions >= 5),
        ("💎", "SCHOLAR",      st.session_state.score >= 350),
        ("👑", "LEGEND CHASE", st.session_state.score >= 800),
    ]
    badge_html = "".join(
        f'<span class="badge {"badge-earned" if e else "badge-locked"}">{i} {n}</span>'
        for i, n, e in badges
    )
    st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MANDATORY: Reset button ───────────────────────────────────────────────
    if st.button("↺  RESET CONVERSATION"):
        st.session_state.messages = []
        st.session_state.score = 0
        st.session_state.last_score_added = 0
        st.session_state.interactions = 0
        st.rerun()

    st.markdown("""
    <div style="margin-top:24px; text-align:center; font-family:'Space Mono',monospace;
         font-size:9px; letter-spacing:2px; color:rgba(200,220,255,0.2);">
      SKILLRANK AI · v1.0<br>
      <span style="color:rgba(200,220,255,0.12);">Curiosity is your currency</span>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════

# Hero header
st.markdown("""
<div class="hero-wrap">
  <div class="trophy-orb">🏆</div>
  <div class="hero-tagline">Competitive Learning Platform</div>
  <div class="hero-title">SKILLRANK AI</div>
  <div class="hero-sub">// CURIOSITY IS YOUR CURRENCY · LEARN · RANK · CONQUER //</div>
</div>
""", unsafe_allow_html=True)

# XP flash banner — shows after first interaction
if st.session_state.last_score_added > 0:
    st.markdown(f"""
    <div class="score-banner">
      <span style="color:rgba(200,220,255,0.5);">⚡ Last response scored</span>
      <span class="score-gained">+{st.session_state.last_score_added} XP earned</span>
      <span style="color:rgba(200,220,255,0.4);">Total XP:</span>
      <span class="score-total">{st.session_state.score}</span>
    </div>
    """, unsafe_allow_html=True)

# Chat header bar
st.markdown("""
<div class="chat-header">
  <div class="chat-header-title"><span class="live-dot"></span>TUTOR SESSION</div>
  <div style="font-family:'Space Mono',monospace; font-size:9px; letter-spacing:2px;
       color:rgba(200,220,255,0.3);">DEEPER QUESTIONS = MORE XP ⚡</div>
</div>
""", unsafe_allow_html=True)

# ── MANDATORY: Display full chat history ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome message on fresh session
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
🎓 **Welcome to SKILLRANK AI!**

I'm your AI tutor — and every question you ask **earns you XP**. The more curious and
detailed your questions, the higher your score climbs and the faster you rank up.

**Tips to earn more XP:**
- Ask *why* and *how* questions 🧠
- Go deeper with follow-ups 🔍
- Keep your conversation going 🔥

**Ready? Ask your first question below! ⚡**
        """)

# ── MANDATORY: st.chat_input — the actual message input box ──────────────────
prompt = st.chat_input("Ask something curious… deeper questions earn more XP 🧠")

if prompt:

    # Show user message immediately (mandatory behaviour)
    with st.chat_message("user"):
        st.markdown(prompt)

    # ── MANDATORY: POST to backend ────────────────────────────────────────────
    try:
        res = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "message": prompt,
                "history": st.session_state.messages   # mandatory field
            }
        )

        data = res.json()

        # ── MANDATORY: Exact response keys from backend ───────────────────────
        reply       = data["reply"]
        score_added = data["score_added"]
        total_score = data["total_score"]

        # ── MANDATORY: Persist score ──────────────────────────────────────────
        st.session_state.score = total_score

        # Extra UI state
        st.session_state.last_score_added = score_added
        st.session_state.interactions    += 1

        # ── MANDATORY: Append messages ONLY ONCE ─────────────────────────────
        st.session_state.messages.append({"role": "user",      "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Show assistant reply (mandatory)
        with st.chat_message("assistant"):
            st.markdown(reply)

        # Inline XP toast
        if score_added > 0:
            st.markdown(f"""
            <div style="display:inline-flex; align-items:center; gap:10px;
                 padding:7px 16px; background:rgba(0,255,180,0.06);
                 border:1px solid rgba(0,255,180,0.2); border-radius:9px;
                 font-family:'Space Mono',monospace; font-size:11px; color:#00ffb4; margin-top:4px;">
              ⚡ <strong>+{score_added} XP</strong> earned &nbsp;·&nbsp;
              Total: <strong style="color:#ffd700">{total_score} XP</strong>
            </div>
            """, unsafe_allow_html=True)

    # ── MANDATORY: Error handling ─────────────────────────────────────────────
    except Exception:
        st.error("⚠️  Backend connection failed — make sure your FastAPI server is running on port 8000")

# Footer
st.markdown("""
<div style="text-align:center; padding:32px 0 8px; margin-top:16px;
     border-top:1px solid rgba(255,255,255,0.04);">
  <span style="font-family:'Orbitron',monospace; font-size:14px; font-weight:900;
       background:linear-gradient(135deg,#ffd700,#00ffb4);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:4px;">
    SKILLRANK AI
  </span>
  <span style="font-family:'Space Mono',monospace; font-size:9px; letter-spacing:3px;
       color:rgba(200,220,255,0.2); display:block; margin-top:4px;">
    CURIOSITY IS YOUR CURRENCY
  </span>
</div>
""", unsafe_allow_html=True)
