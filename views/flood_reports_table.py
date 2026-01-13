import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_current_month_reports(controller):
    """Display current month's flood reports"""
    
    st.markdown("""
    <style>
    .time-badge {
        background: rgba(0, 168, 255, 0.15);
        color: #00a8ff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    .today-badge {
        background: rgba(40, 167, 69, 0.15);
        color: #28a745;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    reports = controller.get_today_reports()
    
    if not reports:
        st.info("📭 Belum ada laporan banjir hari ini.")
        return
    
    total_reports = len(reports)
    unique_locations = len(set(r.get('Alamat', '') for r in reports))
    unique_reporters = len(set(r.get('Nama Pelapor', '') for r in reports))
    
    today = datetime.now().strftime('%d %B %Y')
    st.markdown(f"### 📊 Laporan Harian - {today}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Laporan", total_reports)
    with col2:
        st.metric("Lokasi Berbeda", unique_locations)
    with col3:
        st.metric("Jumlah Pelapor", unique_reporters)
    
    st.markdown("---")
    
    for i, report in enumerate(reports, 1):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
            
            with col1:
                address_text = f"**{i}. {report.get('Alamat', 'N/A')}**"
                st.markdown(address_text, unsafe_allow_html=True)
                
                time_display = format_time(report.get('report_time', ''))
                if time_display:
                    st.markdown(f'<span class="today-badge">🕐 {time_display}</span>', unsafe_allow_html=True)
            
            with col2:
                st.write(f"**{report.get('Tinggi Banjir', 'N/A')}**")
            
            with col3:
                date_display = format_date(report.get('report_date', ''))
                st.write(date_display)
            
            with col4:
                st.write(report.get('Nama Pelapor', 'N/A'))
            
            with col5:
                if report.get('Photo URL') and os.path.exists(report['Photo URL']):
                    if st.button("👁️", key=f"view_{report['id']}", help="Lihat foto"):
                        with st.expander(f"Foto - {report.get('Alamat', 'N/A')}"):
                            try:
                                st.image(report['Photo URL'], use_column_width=True)
                            except:
                                st.warning("Foto tidak dapat ditampilkan")
                else:
                    st.write("📭")
        
        if i < total_reports:
            st.divider()
    
    st.markdown("---")
    
    with st.expander("📋 Data dalam Tabel"):
        table_data = []
        for report in reports:
            table_data.append({
                'No': reports.index(report) + 1,
                'Alamat': report.get('Alamat', ''),
                'Tinggi Banjir': report.get('Tinggi Banjir', ''),
                'Pelapor': report.get('Nama Pelapor', ''),
                'No HP': report.get('No HP', ''),
                'Waktu': report.get('report_time', '')[:5],
                'Status': report.get('Status', 'pending')
            })
        
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

def format_date(date_string):
    """Format date to Indonesian format"""
    try:
        if not date_string:
            return "N/A"
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except:
        return date_string

def format_time(time_string):
    """Format time to HH:MM"""
    try:
        if time_string and len(time_string) >= 5:
            return time_string[:5]
        return ""
    except:
        return ""
