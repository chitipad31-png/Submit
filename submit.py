# ============================================================
#  ระบบส่งข้อมูล Valuation — สำหรับทำสไลด์รายงาน
#  รันด้วย: streamlit run submit.py
# ============================================================

import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

TEAMS = [
    "ทีม 1: โมเดลธุรกิจ & ความเสี่ยง (ข้อ 1-2)",
    "ทีม 2: ฝั่งรายได้ / ยอดขาย (ข้อ 3)",
    "ทีม 3: ฝั่งต้นทุน & งบลงทุน (ข้อ 3)",
    "ทีม 4: กระแสเงินสด & การเติบโต (ข้อ 4)",
    "ทีม 5: ต้นทุนเงินทุน / WACC (ข้อ 4)",
    "ทีม 6: การสร้างมูลค่าที่แท้จริง / ROIC (ข้อ 5)",
]

SOURCES = [
    "Annual Report 2023",
    "Annual Report 2022",
    "Climate Action Plan",
    "Investor Presentation",
    "Sustainability Report",
    "Company Website",
    "อื่นๆ (พิมพ์เอง)",
]

DB_FILE = "submissions.db"

def init_db():
    con = sqlite3.connect(DB_FILE)
    con.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name      TEXT NOT NULL,
            nickname       TEXT NOT NULL,
            student_id     TEXT NOT NULL,
            team           TEXT NOT NULL,
            key_findings   TEXT NOT NULL,
            highlight_nums TEXT NOT NULL,
            source         TEXT NOT NULL,
            page_number    TEXT NOT NULL,
            image_path     TEXT,
            submitted_at   TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def insert_row(data, image_path):
    con = sqlite3.connect(DB_FILE)
    con.execute("""
        INSERT INTO submissions
            (full_name, nickname, student_id, team, key_findings,
             highlight_nums, source, page_number, image_path, submitted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["full_name"], data["nickname"], data["student_id"],
        data["team"], data["key_findings"], data["highlight_nums"],
        data["source"], data["page_number"], image_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    con.commit()
    con.close()

def fetch_all():
    con = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("""
        SELECT id,
            full_name      AS 'ชื่อ-นามสกุล',
            nickname       AS 'ชื่อเล่น',
            student_id     AS 'รหัสนักศึกษา',
            team           AS 'ทีม',
            key_findings   AS 'ประเด็นหลัก',
            highlight_nums AS 'ตัวเลขสำคัญ',
            source         AS 'แหล่งอ้างอิง',
            page_number    AS 'หน้า',
            image_path     AS 'ไฟล์รูป',
            submitted_at   AS 'ส่งเมื่อ'
        FROM submissions ORDER BY id DESC
    """, con)
    con.close()
    return df

init_db()

st.set_page_config(page_title="ส่งข้อมูล Valuation", page_icon="📝", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800&family=Sarabun:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun',sans-serif; }
.stApp { background: #f7f9fd; }
.block-container { padding-top: 2rem !important; }
.stTextInput label, .stSelectbox label, .stTextArea label, .stFileUploader label {
    color: #191c1f !important; font-weight: 600 !important;
    font-size: 0.82rem !important; text-transform: uppercase !important;
}
div[data-testid="stForm"] .stButton > button {
    background: #003d7c; color: #fff; border: none; border-radius: 12px;
    padding: 13px 0; font-size: 0.85rem; font-weight: 800; width: 100%;
    letter-spacing: 0.1em; text-transform: uppercase;
    box-shadow: 0 4px 14px rgba(0,61,124,0.25);
}
div[data-testid="stForm"] .stButton > button:hover { background: #00468c; }
.stDownloadButton > button {
    background: #fff !important; color: #003d7c !important;
    border: 1.5px solid #dde3f0 !important; border-radius: 10px !important;
    font-weight: 700 !important;
}
.note-box {
    background: #fef9c3; border-left: 4px solid #eab308;
    padding: 10px 16px; border-radius: 0 8px 8px 0;
    font-size: 0.88rem; color: #713f12; margin: 6px 0 14px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div style="display:flex;align-items:center;padding:0 0 20px 0;border-bottom:1px solid #e8eaf0;margin-bottom:28px;">
  <div>
    <div style="font-family:'Public Sans',sans-serif;font-size:1.1rem;font-weight:800;color:#003d7c;">📝 Unilever Valuation</div>
    <div style="font-size:0.75rem;color:#727782;margin-top:1px;">ระบบส่งข้อมูลสำหรับทำสไลด์รายงาน</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-size:0.65rem;font-weight:800;letter-spacing:0.2em;color:#003d7c;text-transform:uppercase;margin-bottom:6px;">Data Submission</div>
<div style="font-family:'Public Sans',sans-serif;font-size:2.2rem;font-weight:800;color:#191c1f;letter-spacing:-0.04em;line-height:1.1;margin:0 0 8px 0;">ส่งข้อมูลที่ค้นคว้ามา</div>
<div style="color:#424751;font-size:0.95rem;margin:0 0 28px 0;">กรอกให้ครบทุกช่อง — คนทำสไลด์จะได้ใช้งานได้ทันที</div>
""", unsafe_allow_html=True)

tab_form, tab_data = st.tabs(["✏️  ส่งข้อมูล", "👥  ดูข้อมูลทั้งหมด"])

# ══════════════════════
# TAB 1 — FORM
# ══════════════════════
with tab_form:

    # ── ส่วนที่ 1 ──
    st.markdown("""
<div style="background:linear-gradient(135deg,#003d7c,#1254a1);color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.95rem;margin:8px 0 14px 0;">
  📋 ส่วนที่ 1 — ข้อมูลคนทำ
</div>
""", unsafe_allow_html=True)
    with st.form("submit_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1: full_name  = st.text_input("ชื่อ-นามสกุล *", placeholder="สมชาย ใจดี")
        with c2: nickname   = st.text_input("ชื่อเล่น *",      placeholder="โจ้")
        with c3: student_id = st.text_input("รหัสนักศึกษา *",  placeholder="6XXXXXXX")

        # ── ส่วนที่ 2 ──
        st.markdown("""
<div style="background:linear-gradient(135deg,#003d7c,#1254a1);color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.95rem;margin:16px 0 14px 0;">
  📌 ส่วนที่ 2 — หมวดหมู่งาน
</div>
""", unsafe_allow_html=True)
        team = st.selectbox("หัวข้อที่รับผิดชอบ *", TEAMS)

        # ── ส่วนที่ 3 ──
        st.markdown("""
<div style="background:linear-gradient(135deg,#003d7c,#1254a1);color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.95rem;margin:16px 0 14px 0;">
  ✍️ ส่วนที่ 3 — เนื้อหาที่วิเคราะห์
</div>
""", unsafe_allow_html=True)
        st.markdown('<div class="note-box">⚠️ <b>ห้ามก๊อปแปะ!</b> สรุปมาเป็นภาษาตัวเองเท่านั้น</div>', unsafe_allow_html=True)
        key_findings = st.text_area("สรุปประเด็นหลักที่ค้นพบ *",
            placeholder="เช่น บริษัทมีรายได้หลักมาจาก... โดยมีการเติบโต... เนื่องจาก...", height=130)

        st.markdown('<div class="note-box">💡 ระบุตัวเลขให้ชัด เช่น &quot;ยอดขายโต 69%&quot; หรือ &quot;ประหยัดต้นทุน 1.2 พันล้านยูโร&quot;</div>', unsafe_allow_html=True)
        highlight_nums = st.text_input("ตัวเลขทางการเงิน / สถิติสำคัญ *",
            placeholder="เช่น Revenue +69% YoY, EBIT margin 18.3%")

        # ── ส่วนที่ 4 ──
        st.markdown("""
<div style="background:linear-gradient(135deg,#003d7c,#1254a1);color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.95rem;margin:16px 0 14px 0;">
  📖 ส่วนที่ 4 — หลักฐานอ้างอิง
</div>
""", unsafe_allow_html=True)
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            source_choice = st.selectbox("แหล่งอ้างอิง *", SOURCES)
            source_custom = ""
            if source_choice == "อื่นๆ (พิมพ์เอง)":
                source_custom = st.text_input("ระบุแหล่งอ้างอิง", placeholder="Bloomberg, SEC Filing ...")
        with sc2:
            page_number = st.text_input("เลขหน้า * (บังคับ)", placeholder="42")

        # ── ส่วนที่ 5 ──
        st.markdown("""
<div style="background:linear-gradient(135deg,#003d7c,#1254a1);color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.95rem;margin:16px 0 14px 0;">
  🖼️ ส่วนที่ 5 — ไฟล์แนบ
</div>
""", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "อัปโหลดรูปกราฟ / ตาราง (ถ้ามี)",
            type=["png", "jpg", "jpeg", "webp", "pdf"],
            help="แคปหน้าจอจาก Annual Report แล้วแนบมาได้เลย",
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀  ส่งข้อมูล")

    if submitted:
        source_final = source_custom.strip() if source_choice == "อื่นๆ (พิมพ์เอง)" else source_choice
        errors = []
        if not full_name.strip():       errors.append("ชื่อ-นามสกุล")
        if not nickname.strip():        errors.append("ชื่อเล่น")
        if not student_id.strip():      errors.append("รหัสนักศึกษา")
        if not key_findings.strip():    errors.append("สรุปประเด็นหลัก")
        if not highlight_nums.strip():  errors.append("ตัวเลขสำคัญ")
        if not source_final:            errors.append("แหล่งอ้างอิง")
        if not page_number.strip():     errors.append("เลขหน้า")
        if errors:
            st.error(f"⚠️ กรุณากรอกให้ครบ: **{', '.join(errors)}**")
        else:
            img_path = None
            if uploaded_file:
                safe_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
                img_path = str(UPLOAD_DIR / safe_name)
                with open(img_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            insert_row({
                "full_name": full_name.strip(), "nickname": nickname.strip(),
                "student_id": student_id.strip(), "team": team,
                "key_findings": key_findings.strip(), "highlight_nums": highlight_nums.strip(),
                "source": source_final, "page_number": page_number.strip(),
            }, img_path)
            st.success(f"✅ บันทึกข้อมูลของ **{nickname.strip()}** ({team.split(':')[0]}) เรียบร้อยแล้ว!")
            st.balloons()

# ══════════════════════
# TAB 2 — DATA
# ══════════════════════
with tab_data:
    df = fetch_all()
    total = len(df)
    teams_done = df["ทีม"].nunique() if not df.empty else 0
    has_img = int(df["ไฟล์รูป"].notna().sum()) if not df.empty else 0

    m1, m2, m3 = st.columns(3)
    for col, label, value, color in [
        (m1, "ส่งข้อมูลแล้ว", f"{total} รายการ", "#003d7c"),
        (m2, "ทีมที่ส่งแล้ว",  f"{teams_done} / 6 ทีม", "#1254a1"),
        (m3, "มีไฟล์แนบ",     f"{has_img} รายการ", "#16a34a"),
    ]:
        with col:
            st.markdown(f"""
<div style="background:#fff;border-radius:16px;padding:18px 20px;border:1px solid rgba(194,198,211,0.2);box-shadow:0 4px 20px rgba(0,27,61,0.04);margin-bottom:16px;">
  <div style="font-size:0.62rem;font-weight:800;color:#727782;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:4px;">{label}</div>
  <div style="font-family:'Public Sans',sans-serif;font-size:1.6rem;font-weight:800;color:{color};">{value}</div>
</div>
""", unsafe_allow_html=True)

    st.divider()

    if df.empty:
        st.info("ยังไม่มีข้อมูล — รอเพื่อนส่งก่อนนะ!")
    else:
        team_filter = st.multiselect("กรองตามทีม", options=TEAMS, placeholder="ไม่เลือก = ดูทั้งหมด")
        display_df = df[df["ทีม"].isin(team_filter)] if team_filter else df

        st.dataframe(display_df.drop(columns=["ไฟล์รูป"]),
                     use_container_width=True, hide_index=True, height=400)

        img_rows = display_df[display_df["ไฟล์รูป"].notna()]
        if not img_rows.empty:
            st.markdown("#### 🖼️ รูปภาพที่แนบมา")
            for _, row in img_rows.iterrows():
                p = row["ไฟล์รูป"]
                if p and os.path.exists(p) and p.lower().endswith(("png","jpg","jpeg","webp")):
                    st.caption(f"**{row['ชื่อเล่น']}** — {row['ทีม'].split(':')[0]}")
                    st.image(p, use_container_width=True)

        st.divider()
        csv = display_df.drop(columns=["ไฟล์รูป"]).to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️  Export CSV",
            data=csv,
            file_name=f"valuation_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv")
