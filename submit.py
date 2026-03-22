# ============================================================
#  ระบบส่งข้อมูล Valuation — สำหรับทำสไลด์รายงาน
#  รันด้วย: streamlit run submit.py
# ============================================================

import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

TOPICS = [
    "ข้อ 1: เป้าหมายรักษ์โลก",
    "ข้อ 2: สัดส่วนรายได้",
    "ข้อ 3: ความเสี่ยงอากาศ",
    "ข้อ 4: ตัวเลขวัตถุดิบ",
    "ข้อ 5: ยอดขายแบรนด์รักษ์โลก",
    "ข้อ 6: การตั้งราคา",
    "ข้อ 7: ตัวเลขลดต้นทุน",
    "ข้อ 8: ตัวเลขงบลงทุน",
    "ข้อ 9: กำไรจากการดำเนินงาน",
    "ข้อ 10: หนี้และดอกเบี้ย",
    "ข้อ 11: คะแนน ESG",
    "ข้อ 12: คะแนนพนักงาน",
]

SOURCES = [
    "Annual Report 2025",
    "Climate Action Plan",
    "Investor Presentation",
    "Sustainability Report",
    "Company Website",
    "อื่นๆ (พิมพ์เอง)",
]

def insert_row(data, image_path):
    supabase.table("submissions").insert({
        "full_name":      data["full_name"],
        "nickname":       data["nickname"],
        "student_id":     data["student_id"],
        "team":           data["team"],
        "key_findings":   data["key_findings"],
        "highlight_nums": data["highlight_nums"],
        "source":         data["source"],
        "page_number":    data["page_number"],
        "image_path":     image_path,
        "submitted_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }).execute()

def fetch_all():
    res = supabase.table("submissions").select("*").order("id", desc=True).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

st.set_page_config(page_title="ส่งข้อมูล Valuation", page_icon="📝", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800&family=Sarabun:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun',sans-serif; }
.stApp { background: #f7f9fd; }
.block-container { padding-top: 2rem !important; }
.stTextInput label, .stSelectbox label, .stTextArea label, .stFileUploader label {
    color:#191c1f !important; font-weight:600 !important;
    font-size:0.82rem !important; text-transform:uppercase !important;
}
div[data-testid="stForm"] .stButton > button {
    background:#003d7c; color:#fff; border:none; border-radius:12px;
    padding:13px 0; font-size:0.85rem; font-weight:800; width:100%;
    letter-spacing:0.1em; text-transform:uppercase;
    box-shadow:0 4px 14px rgba(0,61,124,0.25);
}
div[data-testid="stForm"] .stButton > button:hover { background:#00468c; }
.stDownloadButton > button {
    background:#fff !important; color:#003d7c !important;
    border:1.5px solid #dde3f0 !important; border-radius:10px !important; font-weight:700 !important;
}
.note-box {
    background:#fef9c3; border-left:4px solid #eab308;
    padding:10px 16px; border-radius:0 8px 8px 0;
    font-size:0.88rem; color:#713f12; margin:6px 0 14px 0;
}
</style>
""", unsafe_allow_html=True)

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

def sec(title):
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#003d7c,#1254a1);color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.95rem;margin:16px 0 14px 0;">
  {title}
</div>
""", unsafe_allow_html=True)

tab_form, tab_data = st.tabs(["✏️  ส่งข้อมูล", "👥  ดูข้อมูลทั้งหมด"])

# ══════════════════════
# TAB 1 — FORM
# ══════════════════════
with tab_form:
    sec("📋 ส่วนที่ 1 — ข้อมูลคนทำ")
    with st.form("submit_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1: full_name  = st.text_input("ชื่อ-นามสกุล *", placeholder="สมชาย ใจดี")
        with c2: nickname   = st.text_input("ชื่อเล่น *",      placeholder="โจ้")
        with c3: student_id = st.text_input("รหัสนักศึกษา *",  placeholder="6XXXXXXX")

        sec("📌 ส่วนที่ 2 — หัวข้อที่รับผิดชอบ")
        team = st.selectbox("เลือกหัวข้อ *", TOPICS)

        sec("✍️ ส่วนที่ 3 — เนื้อหาที่วิเคราะห์")
        st.markdown('<div class="note-box">⚠️ <b>ห้ามก๊อปแปะ!</b> สรุปมาเป็นภาษาตัวเองเท่านั้น</div>', unsafe_allow_html=True)
        key_findings = st.text_area("สรุปประเด็นหลักที่ค้นพบ *",
            placeholder="เช่น บริษัทมีรายได้หลักมาจาก...", height=130)
        st.markdown('<div class="note-box">💡 ระบุตัวเลขให้ชัด เช่น &quot;ยอดขายโต 69%&quot;</div>', unsafe_allow_html=True)
        highlight_nums = st.text_input("ตัวเลขทางการเงิน / สถิติสำคัญ *",
            placeholder="เช่น Revenue +69% YoY, EBIT margin 18.3%")

        sec("📖 ส่วนที่ 4 — หลักฐานอ้างอิง")
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            source_choice = st.selectbox("แหล่งอ้างอิง *", SOURCES)
            source_custom = ""
            if source_choice == "อื่นๆ (พิมพ์เอง)":
                source_custom = st.text_input("ระบุแหล่งอ้างอิง", placeholder="Bloomberg...")
        with sc2:
            page_number = st.text_input("เลขหน้า * (บังคับ)", placeholder="42")

        sec("🖼️ ส่วนที่ 5 — ไฟล์แนบ")
        uploaded_file = st.file_uploader("อัปโหลดรูปกราฟ / ตาราง (ถ้ามี)",
            type=["png","jpg","jpeg","webp","pdf"])

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀  ส่งข้อมูล")

    if submitted:
        source_final = source_custom.strip() if source_choice == "อื่นๆ (พิมพ์เอง)" else source_choice
        errors = []
        if not full_name.strip():      errors.append("ชื่อ-นามสกุล")
        if not nickname.strip():       errors.append("ชื่อเล่น")
        if not student_id.strip():     errors.append("รหัสนักศึกษา")
        if not key_findings.strip():   errors.append("สรุปประเด็นหลัก")
        if not highlight_nums.strip(): errors.append("ตัวเลขสำคัญ")
        if not source_final:           errors.append("แหล่งอ้างอิง")
        if not page_number.strip():    errors.append("เลขหน้า")
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
            st.success(f"✅ บันทึกข้อมูลของ **{nickname.strip()}** ({team}) เรียบร้อยแล้ว!")
            st.balloons()

# ══════════════════════
# TAB 2 — DATA
# ══════════════════════
with tab_data:
    df = fetch_all()
    total = len(df)
    topics_done = df["team"].nunique() if not df.empty else 0

    c1, c2 = st.columns(2)
    for col, label, value, color in [
        (c1, "ส่งข้อมูลแล้ว",   f"{total} รายการ",      "#003d7c"),
        (c2, "หัวข้อที่ส่งแล้ว", f"{topics_done} / 12",  "#16a34a"),
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
        topic_filter = st.multiselect("กรองตามหัวข้อ", options=TOPICS, placeholder="ไม่เลือก = ดูทั้งหมด")
        display_df = df[df["team"].isin(topic_filter)] if topic_filter else df

        show_cols = [c for c in ["full_name","nickname","student_id","team","key_findings","highlight_nums","source","page_number"] if c in display_df.columns]
        rename_map = {
            "full_name":"ชื่อ-นามสกุล","nickname":"ชื่อเล่น","student_id":"รหัส",
            "team":"หัวข้อ","key_findings":"ประเด็นหลัก","highlight_nums":"ตัวเลขสำคัญ",
            "source":"แหล่งอ้างอิง","page_number":"หน้า"
        }
        st.dataframe(display_df[show_cols].rename(columns=rename_map),
                     use_container_width=True, hide_index=True, height=400)

        st.divider()
        csv = display_df[show_cols].rename(columns=rename_map).to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️  Export CSV", data=csv,
                           file_name=f"submissions_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv")

        st.divider()
        with st.expander("✏️ แก้ไขหรือลบรายการ"):
            options = [f"{r.get('nickname','?')} — {r.get('team','?')} (#{r.get('id','?')})"
                       for _, r in display_df.iterrows()]
            selected = st.selectbox("เลือกรายการ", options)
            idx = options.index(selected)
            row = display_df.iloc[idx]

            col1, col2 = st.columns(2)
            with col1:
                new_name    = st.text_input("ชื่อ-นามสกุล",  value=str(row.get("full_name","")))
                new_nick    = st.text_input("ชื่อเล่น",       value=str(row.get("nickname","")))
                new_sid     = st.text_input("รหัสนักศึกษา",   value=str(row.get("student_id","")))
                cur_team    = row.get("team", TOPICS[0])
                team_idx    = TOPICS.index(cur_team) if cur_team in TOPICS else 0
                new_team    = st.selectbox("หัวข้อ", TOPICS, index=team_idx)
            with col2:
                new_finding = st.text_area("ประเด็นหลัก",     value=str(row.get("key_findings","")), height=120)
                new_nums    = st.text_input("ตัวเลขสำคัญ",     value=str(row.get("highlight_nums","")))
                new_source  = st.text_input("แหล่งอ้างอิง",    value=str(row.get("source","")))
                new_page    = st.text_input("เลขหน้า",         value=str(row.get("page_number","")))

            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("💾 บันทึกการแก้ไข", use_container_width=True):
                    supabase.table("submissions").update({
                        "full_name":      new_name.strip(),
                        "nickname":       new_nick.strip(),
                        "student_id":     new_sid.strip(),
                        "team":           new_team,
                        "key_findings":   new_finding.strip(),
                        "highlight_nums": new_nums.strip(),
                        "source":         new_source.strip(),
                        "page_number":    new_page.strip(),
                    }).eq("id", int(row["id"])).execute()
                    st.success("✅ แก้ไขเรียบร้อย!")
                    st.rerun()
            with btn2:
                if st.button("🗑️ ลบรายการนี้", type="primary", use_container_width=True):
                    supabase.table("submissions").delete().eq("id", int(row["id"])).execute()
                    st.success("✅ ลบเรียบร้อย!")
                    st.rerun()
