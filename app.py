import os
import streamlit as plt_stream
import pandas as pd

from data_processing.loader import load_csv
from data_processing.column_detector import detect_column_types
from data_processing.stats_generator import generate_stats
from visualization.chart_generator import select_relevant_charts, create_bar_chart, create_pie_chart, create_line_chart
from report.pdf_builder import create_report

# Page Configuration Setup
plt_stream.set_page_config(
    page_title="Automated Business Report Engine",
    page_icon="📊",
    layout="wide"  # Changed to wide to fit side-by-side column previews beautifully
)

plt_stream.title("📊 Automated Business Report Engine")
plt_stream.markdown(
    "Upload any raw corporate CSV dataset file to automatically analyze column structures, "
    "compute tie-proof summary metrics, paint data trends, and compile a downloadable executive PDF report."
)

plt_stream.divider()

uploaded_file = plt_stream.file_uploader("Choose a corporate CSV dataset file", type=["csv"])

if uploaded_file is not None:
    plt_stream.success("📁 Dataset file uploaded successfully!")
    
    output_pdf = "assets/screenshots/final_executive_report.pdf"
    screenshot_dir = "assets/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    try:
        temp_path = os.path.join(screenshot_dir, "temp_uploaded_data.csv")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with plt_stream.spinner("Running dataset analytics and drawing charts..."):
            df = load_csv(temp_path)
            column_types = detect_column_types(df)
            stats_data = generate_stats(df, column_types)
            
            chart_queue = select_relevant_charts(column_types)
            generated_chart_paths = []
            for chart in chart_queue:
                target_path = os.path.join(screenshot_dir, chart["filename"])
                if chart["type"] == "bar":
                    create_bar_chart(df, chart["cat_col"], chart["num_col"], target_path)
                elif chart["type"] == "pie":
                    create_pie_chart(df, chart["cat_col"], target_path)
                elif chart["type"] == "line":
                    create_line_chart(df, chart["date_col"], chart["num_col"], target_path)
                generated_chart_paths.append(target_path)
                
            create_report(
                output_path=output_pdf,
                report_title="Executive Performance Analysis Report",
                source_filename=uploaded_file.name,
                stats_data=stats_data,
                chart_paths=generated_chart_paths
            )
            
        
        
        # ================= NEW: SCREEN PREVIEW & LAYOUT ENGINE =================
        plt_stream.header("👀 Live Report Executive Preview")
        
        # Layout columns split into two distinct panels
        left_panel, right_panel = plt_stream.columns(2)
        
        with left_panel:
            plt_stream.subheader("🔍 Column Structure Analysis")
            # Convert dictionary mapping into a clean visible dataframe table
            col_df = pd.DataFrame(list(column_types.items()), columns=["Column Name", "Detected Role"])
            plt_stream.dataframe(col_df, use_container_width=True)
            
            plt_stream.subheader("🔢 Numerical Statistics")
            for col, metrics in stats_data.get("numeric", {}).items():
                plt_stream.markdown(f"**Field:** `{col}`")
                plt_stream.text(f"  • Total Sum: {metrics['total']:,.2f}\n  • Average:   {metrics['average']:,.2f}\n  • Min/Max:   {metrics['min']} to {metrics['max']}")
        
        with right_panel:
            plt_stream.subheader("🔠 Categorical Allocations")
            for col, metrics in stats_data.get("categorical", {}).items():
                plt_stream.markdown(f"**Field:** `{col}`")
                
                # Dynamic string formatting evaluating our tie rules safely!
                if metrics.get("is_tie", False):
                    winners = ", ".join(metrics["most_frequent"])
                    plt_stream.error(f"  • Most Frequent: {winners} (Tie Multi-Winner Detected!)")
                else:
                    plt_stream.markdown(f"  • Most Frequent: **{metrics['most_frequent']}**")
                
                plt_stream.text("  • Value Distribution Breakdown:")
                for category_name, count in metrics["value_counts"].items():
                    plt_stream.text(f"    - {category_name}: {count} records")
        
        plt_stream.divider()
        
        # ================= NEW: SECURE PDF DOWNLOAD LINK BUTTON =================
        plt_stream.subheader("📥 Export Finalized Document")
        
        # Read the compiled binary report asset securely from disk storage
        with open(output_pdf, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            
        plt_stream.download_button(
            label="🚀 Download Executive PDF Report Document",
            data=pdf_bytes,
            file_name="Executive_Data_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    except Exception as e:
        plt_stream.error(f"❌ Structural Execution Failure: {e}")
        
else:
    plt_stream.info("💡 Please upload a corporate CSV file above to trigger the analytical report pipeline.")