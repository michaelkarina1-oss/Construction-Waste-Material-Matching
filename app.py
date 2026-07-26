# -*- coding: utf-8 -*-
import streamlit as st
import pyodbc
import pandas as pd

# =====================================================================
# 1. הגדרות תשתית ועיצוב הייטק בהיר (Tech Light RTL UI) לפי האינפוגרפיקה
# =====================================================================
st.set_page_config(
    page_title="SiteSync Next-Gen UI", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# הזרקת קוד CSS מלא לתיקון כל בעיות הניגודיות והטקסט הלבן
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;900&display=swap');
    
    /* רקע כללי בהיר וגופן נקי - טקסט גלובלי כחול כהה */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Assistant', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8fafc; /* רקע אפרפר-תכלת בהיר ונקי */
        color: #0f172a !important; /* טקסט כחול כהה קריא */
    }
    
    h1, h2, h3, h4, h5, p, label, th, td, span, strong { 
        text-align: right !important; 
        direction: rtl !important;
        color: #0f172a !important; /* הגנה מוחלטת: כל הטקסטים בכחול כהה */
    }
    
    /* כרטיסיות לבנות נקיות עם מסגרת תכלת עדינה */
    .cyber-glass-card { 
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }
    .cyber-glass-card table, .cyber-glass-card tr, .cyber-glass-card td {
        color: #0f172a !important;
    }
    
    /* מוני נתונים (Metrics) מעודכנים */
    .metric-container {
        background: #ffffff !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    .metric-container h5 {
        color: #0f172a !important; 
    }
    /* כחול נייבי עמוק מהכותרת המרכזית */
    .metric-val-blue { color: #0f172a !important; font-size: 38px; font-weight: bold; text-align: center !important;}
    /* ארגמן/ורוד מכפתורי המודל */
    .metric-val-red { color: #db2777 !important; font-size: 38px; font-weight: bold; text-align: center !important;}
    /* כחול בהיר/תכלת מהאלמנטים הטכניים */
    .metric-val-purple { color: #0284c7 !important; font-size: 38px; font-weight: bold; text-align: center !important;}
    
    /* כרטיסיית שידוך מעוצבת בכחול נייבי עם מסגרת מודגשת */
    .match-neon-box {
        background: #ffffff !important;
        border: 2px solid #0f172a !important;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.1) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }
    
    /* ווידג'ט לוגיסטי עם מסגרת מקווקוות עדינה */
    .telemetry-box {
        background: #f1f5f9 !important;
        border: 1px dashed #0284c7 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin-top: 15px !important;
    }
    .telemetry-box table, .telemetry-box tr, .telemetry-box td {
        color: #0f172a !important;
    }
    
    /* כפתורים בצבע כחול נייבי מקצועי עם טקסט לבן חריג */
    .stButton>button { 
        width: 100% !important; 
        background: #0f172a !important;
        color: white !important; /* כאן נשאר לבן בכוונה בשביל הניגודיות על הכפתור הכהה */
        border: none !important;
        font-weight: bold !important; 
        height: 3.3em !important; 
        border-radius: 10px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.2) !important;
        transition: all 0.2s !important;
    }
    .stButton>button:hover { background: #1e293b !important; transform: translateY(-1px) !important; }
    .stButton>button div, .stButton>button p, .stButton>button span {
        color: white !important; /* תיקון לכפתורי Streamlit פנימיים */
    }
    
    /* עיצוב הטאבים (Tabs) להתאמה לפלטה הבהירה */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important;
        background-color: #e2e8f0 !important;
        padding: 8px !important;
        border-radius: 12px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #475569 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #0f172a !important;
    }
    
    /* אלמנטים של טפסים */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# מחרוזת החיבור לשרת ה-MS SQL ב-166 (CasaOS)
DB_CONN_STRING = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=0.0.0.0,1433;'
    'DATABASE=SiteSyncDB;'
    'UID=sa;'
    'PWD=Your Pass;'
    'TrustServerCertificate=yes;'
    'Connection Timeout=10;'
)

def run_query(sql, params=None, is_select=True):
    try:
        with pyodbc.connect(DB_CONN_STRING) as conn:
            if is_select: return pd.read_sql(sql, conn, params=params)
            else:
                cursor = conn.cursor()
                cursor.execute(sql, params or ())
                conn.commit()
                return True
    except Exception as e:
        st.error(f"❌ שגיאת סנכרון מול שרת 166: {e}")
        return None

# כותרת המערכת
st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #0f172a !important; font-size: 38px; font-weight: 900; letter-spacing: 1px;'>
            🏗️ SITESYNC NEXT-GEN
        </h1>
        <p style='color: #475569 !important; font-size: 15px; margin-top: 5px; font-weight: 600;'>מערכת אופטימיזציה ושדכנות עודפי בנייה דיגיטלית | פיילוט מעבדה POC</p>
        <div style='font-size:11px; color:#94a3b8 !important;'>Host: 10.0.0.180 &nbsp;|&nbsp; DB Target: 10.0.0.166</div>
    </div>
""", unsafe_allow_html=True)

# פריסת הטאבים
tab_main, tab_reg, tab_extension = st.tabs([
    "⚡ פאנל בקרה ומנוע שידוכים", 
    "📝 רישום דרישות אתר",
    "🔌 תוסף חכם ליומני עבודה (Extension)"
])

# =====================================================================
# טאב 1: פאנל בקרה ומנוע שידוכים
# =====================================================================
with tab_main:
    col_m1, col_m2, col_m3 = st.columns(3)
    df_stats = run_query("SELECT Status, ActionType, Quantity FROM t_ConstructionPool")
    active_count, disposal_trucks, matched_count = 0, 0, 0
    if isinstance(df_stats, pd.DataFrame) and not df_stats.empty:
        active_count = len(df_stats[df_stats['Status'] == 'פעיל'])
        disposal_trucks = df_stats[(df_stats['ActionType'] == 'DISPOSAL') & (df_stats['Status'] == 'פעיל')]['Quantity'].sum()
        matched_count = run_query("SELECT COUNT(*) as cnt FROM t_MatchHistory").iloc[0]['cnt']

    with col_m1:
        st.markdown(f"<div class='metric-container'><h5>פרויקטים פעילים ברשת</h5><div class='metric-val-blue'>{active_count}</div></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-container'><h5>משאיות לפינוי מיידי</h5><div class='metric-val-red'>{disposal_trucks}</div></div>", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"<div class='metric-container'><h5>שידוכי רשת מוצלחים</h5><div class='metric-val-purple'>{matched_count}</div></div>", unsafe_allow_html=True)

    st.write("---")
    col_pool, col_matcher = st.columns([3, 2])

    with col_pool:
        st.markdown("<h4 style='color: #0f172a;'>📡 דרישות פתוחות בצינור הלוגיסטי (Live Pool)</h4>", unsafe_allow_html=True)
        df_all = run_query("SELECT Id, CompanyName, SiteName, ActionType, MaterialType, Quantity FROM t_ConstructionPool WHERE Status = N'פעיל'")
        if isinstance(df_all, pd.DataFrame) and not df_all.empty:
            for _, row in df_all.iterrows():
                action_lbl = "🔴 פינוי" if row['ActionType'] == 'DISPOSAL' else "🟢 איסוף"
                border_color = "#ef4444" if row['ActionType'] == 'DISPOSAL' else "#10b981"
                st.markdown(f"""
                    <div class='cyber-glass-card' style='border-right: 5px solid {border_color};'>
                        <table style='width:100%; font-size:14px;'>
                            <tr>
                                <td><strong style='color: #0f172a;'>חברה:</strong> <span style='color: #0f172a;'>{row['CompanyName']}</span></td>
                                <td><strong style='color: #0f172a;'>אתר:</strong> <span style='color: #0f172a;'>{row['SiteName']}</span></td>
                                <td style='color:{border_color} !important; font-weight:bold;'>{action_lbl}</td>
                            </tr>
                            <tr>
                                <td><strong style='color: #0f172a;'>חומר:</strong> <span style='color: #0f172a;'>{row['MaterialType']}</span></td>
                                <td><strong style='color: #0f172a;'>כמות:</strong> <span style='color: #0f172a;'>{row['Quantity']} משאיות</span></td>
                                <td style='color:#64748b !important;'>ID: #{row['Id']}</td>
                            </tr>
                        </table>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ה-Live Pool ריק כרגע. הרץ את סקריפט הזרקת הנתונים.")

    with col_matcher:
        st.markdown("<h4 style='color: #0284c7;'>⚡ מנוע ההצלבות האלגוריתמי</h4>", unsafe_allow_html=True)
        df_disp = run_query("SELECT * FROM t_ConstructionPool WHERE ActionType = 'DISPOSAL' AND Status = N'פעיל'")
        df_coll = run_query("SELECT * FROM t_ConstructionPool WHERE ActionType = 'COLLECTION' AND Status = N'פעיל'")
        
        match_triggered = False
        if isinstance(df_disp, pd.DataFrame) and isinstance(df_coll, pd.DataFrame):
            for _, disp in df_disp.iterrows():
                matched_targets = df_coll[df_coll['MaterialType'] == disp['MaterialType']]
                if not matched_targets.empty:
                    for _, coll in matched_targets.iterrows():
                        match_triggered = True
                        
                        st.markdown(f"""
                            <div class='match-neon-box'>
                                <div style='color:#0284c7 !important; font-weight:bold; margin-bottom:10px; font-size:16px;'>🔮 שידוך אופטימלי זוהה לחומר: {disp['MaterialType']}</div>
                                <div style='font-size:14px; margin-bottom:5px; color:#0f172a !important;'>🔴 <strong style='color:#0f172a !important;'>מוסר:</strong> {disp['CompanyName']} ({disp['SiteName']})</div>
                                <div style='font-size:14px; margin-bottom:15px; color:#0f172a !important;'>🟢 <strong style='color:#0f172a !important;'>קולט:</strong> {coll['CompanyName']} ({coll['SiteName']})</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"🤝 אשר עסקה: {disp['CompanyName']} ⟷ {coll['CompanyName']}", key=f"m_{disp['Id']}_{coll['Id']}"):
                            run_query("UPDATE t_ConstructionPool SET Status = N'שודך' WHERE Id IN (?, ?)", params=(disp['Id'], coll['Id']), is_select=False)
                            min_qty = min(disp['Quantity'], coll['Quantity'])
                            run_query("INSERT INTO t_MatchHistory (GiverId, ReceiverId, MaterialType, QuantityMatched) VALUES (?, ?, ?, ?)", 
                                      params=(disp['Id'], coll['Id'], disp['MaterialType'], min_qty), is_select=False)
                            st.balloons()
                            st.rerun()
        if not match_triggered:
            st.write("מחפש הצלבות חופפות ב-DB...")

# =====================================================================
# טאב 2: טופס רישום וארכיון היסטוריה
# =====================================================================
with tab_reg:
    col_form, col_hist = st.columns([2, 3])
    with col_form:
        st.markdown("<h4 style='color: #0f172a;'>📝 רישום דרישה חדשה</h4>", unsafe_allow_html=True)
        with st.form("new_site_form", clear_on_submit=True):
            c_name = st.text_input("Company Name")
            cont_name = st.text_input("Contractor Name")
            p_num = st.text_input("Phone Number")
            s_loc = st.text_input("Site Location")
            l_purpose = st.selectbox("Logistic Purpose", [("פינוי עודפים", "DISPOSAL"), ("איסוף חומר", "COLLECTION")])
            m_type = st.selectbox("Material Type", ["בטון גרוס / מצע", "חול נקי", "פסולת בניין נקייה", "אדמה גסה", "סלע / אבן לשבירה"])
            qty = st.number_input("Quantity (Trucks)", min_value=1, value=10)
            
            btn_submit = st.form_submit_button("⚡ הזרק ישות ל-SQL Server")
            if btn_submit and c_name and cont_name:
                sql_add = "INSERT INTO t_ConstructionPool (CompanyName, ContractorName, SiteName, Phone, ActionType, MaterialType, Quantity) VALUES (?, ?, ?, ?, ?, ?, ?)"
                run_query(sql_add, params=(c_name, cont_name, s_loc, p_num, l_purpose[1], m_type, qty), is_select=False)
                st.success("הנתונים נרשמו בשרת 166!")
                st.rerun()

    with col_hist:
        st.markdown("<h4 style='color: #0f172a;'>📜 ארכיון עסקאות מלא (History Log)</h4>", unsafe_allow_html=True)
        df_h = run_query("""
            SELECT h.MatchId as [ID], g.CompanyName as [חברה מוסרת], g.SiteName as [אתר מוסר], 
                   r.CompanyName as [חברה קולטת], r.SiteName as [אתר קולט], 
                   h.MaterialType as [סוג חומר], h.QuantityMatched as [משאיות]
            FROM t_MatchHistory h
            JOIN t_ConstructionPool g ON h.GiverId = g.Id
            JOIN t_ConstructionPool r ON h.ReceiverId = r.Id
        """)
        if isinstance(df_h, pd.DataFrame) and not df_h.empty:
            st.dataframe(df_h.set_index('ID'), use_container_width=True)
        else:
            st.caption("אין עסקאות חתומות בארכיון כרגע.")

# =====================================================================
# טאב 3: סימולציית תוסף יומני עבודה
# =====================================================================
with tab_extension:
    st.markdown("<h3 style='color: #0f172a; text-align: center;'>🔌 הדמיית ה-Extension בתוך יומן עבודה קיים</h3>", unsafe_allow_html=True)
    st.write("---")
    
    col_log, col_popup = st.columns([2, 2])
    
    with col_log:
        st.markdown("<h4 style='color: #475569;'>📋 מבט מפקח: מילוי יומן עבודה דיגיטלי</h4>", unsafe_allow_html=True)
        st.write("מילוי שוטף של נתוני השטח ביומני העבודה.")
        
        with st.container():
            st.date_input("תאריך יומן", value=pd.to_datetime("2026-10-14"))
            ext_company = st.selectbox("שם החברה הקבלנית באתר", ["דניה סיבוס בע''מ", "אשטרום תשתיות", "שפיר הנדסה"])
            ext_site = st.text_input("מיקום האתר שלך", value="שכונת המעיין, כרמיאל")
            ext_target_site = st.text_input("מיקום אתר היעד ברשת", value="אזור תעשייה, עכו")
            ext_code = st.text_input("קוד סעיף דקל", value="02.04.01")
            ext_desc = st.text_input("תיאור הסעיף", value="פינוי עודפי חפירה / בטון גרוס")
            ext_qty = st.number_input("כמות מדווחת ביומן (משאיות)", min_value=10, max_value=500, value=120, step=10)

    with col_popup:
        st.markdown("<h4 style='color: #0284c7;'>💡 שכבת ה-AI: הצעה חלומית לשידוך מיידי</h4>", unsafe_allow_html=True)
        st.write("כרטיסיית ניתוח כלכלי המוצגת למפקח ישירות על גבי המסך על סמך נתוני ה-SQL הפנימיים.")
        
        dumping_fee_saved = ext_qty * 100
        transport_saved = ext_qty * 20.83
        total_saved_giver = dumping_fee_saved + transport_saved
        total_saved_receiver = ext_qty * 75
        
        # תיבת המידע הלבנה והנקייה בסגנון ה"סיכום כללי" מהאינפוגרפיקה - כל הטקסטים בכחול כהה מוחלט
        st.markdown(f"""
            <div class='match-neon-box' style='border-top: 6px solid #0f172a !important;'>
                <div style='font-size: 18px; color: #0f172a !important; font-weight: bold; margin-bottom: 15px;'>
                    🔮 הצעה חלומית לשידוך מיידי: [חברה א'] ⟷ [חברה B']
                </div>
                <p style='font-size: 14px; margin-bottom: 8px; color: #0f172a !important;'>
                    <span style='color:#ef4444 !important;'>🔴</span> <strong style='color:#0f172a !important;'>קבלן מוסר ({ext_company}):</strong> מפנה {ext_qty} משאיות.<br>
                    <strong style='color:#0f172a !important;'>מיקום מקור:</strong> {ext_site}<br>
                    <span style='color:#16a34a !important; font-weight:bold;'>סה"כ חיסכון למוסר: {total_saved_giver:,.0f} ש"ח.</span>
                </p>
                <hr style='border-color: #e2e8f0; margin: 10px 0;'>
                <p style='font-size: 14px; margin-bottom: 8px; color: #0f172a !important;'>
                    <span style='color:#16a34a !important;'>🟢</span> <strong style='color:#0f172a !important;'>קבלן קולט מדומה:</strong> צורך מילוי חומר.<br>
                    <strong style='color:#0f172a !important;'>מיקום יעד מחובר:</strong> {ext_target_site}<br>
                    <span style='color:#16a34a !important; font-weight:bold;'>סה"כ חיסכון לקולט: {total_saved_receiver:,.0f} ש"ח.</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 📊 ווידג'ט נתונים לוגיסטיים בהיר ונקי 
        st.markdown("""
            <div class='telemetry-box'>
                <div style='font-size:14px; color:#0284c7 !important; font-weight:bold; margin-bottom:8px;'>📊 נתוני טלמטריה ולוגיסטיקה של הצי</div>
                <table style='width:100%; font-size:13px;'>
                    <tr>
                        <td><strong style='color: #0f172a;'>🛣️ נתיב תובלה:</strong> כרמיאל ⟷ עכו (כביש 85 ישיר)</td>
                        <td><strong style='color: #0f172a;'>⏱️ זמן סבב משוער:</strong> 14 דקות</td>
                    </tr>
                    <tr>
                        <td><strong style='color: #0f172a;'>🔋 ייעול מסלול:</strong> קו קצר (ללא מעברים עירוניים)</td>
                        <td><strong style='color: #0f172a;'>🌱 צמצום פליטות פחמן:</strong> 35% חיסכון אנרגטי</td>
                    </tr>
                </table>
            </div>
            <br>
        """, unsafe_allow_html=True)
        
        if st.button("✅ אשר שידוך והחתם יומנים (Save Both Sides Money)", key="ext_btn_match"):
            sql_disp = "INSERT INTO t_ConstructionPool (CompanyName, ContractorName, SiteName, Phone, ActionType, MaterialType, Quantity, Status) VALUES (?, N'מנהל עבודה', ?, '054-0000000', 'DISPOSAL', N'בטון גרוס / מצע', ?, N'שודך')"
            sql_coll = "INSERT INTO t_ConstructionPool (CompanyName, ContractorName, SiteName, Phone, ActionType, MaterialType, Quantity, Status) VALUES (N'חברה קולטת מדומה', N'מפקח אזורי', ?, '054-1111111', 'COLLECTION', N'בטון גרוס / מצע', ?, N'שודך')"
            
            run_query(sql_disp, params=(ext_company, ext_site, ext_qty), is_select=False)
            run_query(sql_coll, params=(ext_target_site, ext_qty), is_select=False)
            
            df_last = run_query("SELECT TOP 2 Id FROM t_ConstructionPool ORDER BY Id DESC")
            if isinstance(df_last, pd.DataFrame) and len(df_last) >= 2:
                id_coll = df_last.iloc[0]['Id']
                id_disp = df_last.iloc[1]['Id']
                run_query("INSERT INTO t_MatchHistory (GiverId, ReceiverId, MaterialType, QuantityMatched) VALUES (?, ?, N'בטון גרוס / מצע', ?)", 
                          params=(id_disp, id_coll, ext_qty), is_select=False)
            
            st.balloons()
            st.success("🏆 השידוך אושר! יומני העבודה עודכנו ונחתמו דיגיטלית בשרת 166.")
            st.rerun()