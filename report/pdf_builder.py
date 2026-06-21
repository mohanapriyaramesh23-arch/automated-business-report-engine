import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors

def create_report(output_path: str, report_title: str, source_filename: str, stats_data: dict = None, chart_paths: list = None) -> str:
    """
    Generates a polished, multi-page PDF report with cover page,
    custom tables displaying tie-proof summary statistics, and embedded data charts.
    """
    # 1. Page Frame Configuration
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold',
        fontSize=32, leading=38, textColor=colors.HexColor('#1f4e78'), alignment=1, spaceAfter=15
    )
    meta_style = ParagraphStyle(
        'CoverMeta', parent=styles['Normal'], fontName='Helvetica',
        fontSize=12, leading=16, textColor=colors.HexColor('#595959'), alignment=1, spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'SectionHeading', parent=styles['Normal'], fontName='Helvetica-Bold',
        fontSize=18, leading=22, textColor=colors.HexColor('#1f4e78'), spaceBefore=15, spaceAfter=10, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'TableBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#333333')
    )
    header_style = ParagraphStyle(
        'TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.white
    )
    caption_style = ParagraphStyle(
        'Caption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, leading=12, textColor=colors.HexColor('#595959'), alignment=1, spaceAfter=15
    )

    story = []
    
    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 150))
    story.append(Paragraph(report_title, title_style))
    story.append(Spacer(1, 30))
    current_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"<b>Generated On:</b> {current_date}", meta_style))
    story.append(Paragraph(f"<b>Source Dataset:</b> {source_filename}", meta_style))
    story.append(PageBreak())
    
    # Skip processing parts if data payloads are absent
    if stats_data or chart_paths:
        
        # ================= PAGE 2: SUMMARY STATISTICS =================
        story.append(Paragraph("Dataset Executive Summary", h1_style))
        story.append(Spacer(1, 10))
        
        # 2A. Render Numeric Summary Grid
        if "numeric" in stats_data and stats_data["numeric"]:
            story.append(Paragraph("Key Financial & Metric Summary", ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=6)))
            
            # Setup structured table data grid rows
            grid_data = [[Paragraph("Metric Column", header_style), Paragraph("Total Sum", header_style), Paragraph("Average", header_style), Paragraph("Range (Min / Max)", header_style)]]
            
            for col, metrics in stats_data["numeric"].items():
                col_name = col.replace('_', ' ')
                range_str = f"${metrics['min']:.2f} - ${metrics['max']:.2f}" if "Sales" in col else f"{int(metrics['min'])} - {int(metrics['max'])}"
                total_str = f"${metrics['total']:.2f}" if "Sales" in col else f"{int(metrics['total'])}"
                avg_str = f"${metrics['average']:.2f}" if "Sales" in col else f"{metrics['average']:.2f}"
                
                grid_data.append([
                    Paragraph(col_name, body_style),
                    Paragraph(total_str, body_style),
                    Paragraph(avg_str, body_style),
                    Paragraph(range_str, body_style)
                ])
                
            num_table = Table(grid_data, colWidths=[150, 100, 100, 154])
            num_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1f4e78')),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('TOPPADDING', (0,0), (-1,0), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d9d9d9')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')]),
                ('BOTTOMPADDING', (0,1), (-1,-1), 6),
                ('TOPPADDING', (0,1), (-1,-1), 6),
            ]))
            story.append(num_table)
            story.append(Spacer(1, 20))
            
        # 2B. Render Categorical Summary Grid (With robust multi-way tie protection)
        if "categorical" in stats_data and stats_data["categorical"]:
            story.append(Paragraph("Structural Category Allocations", ParagraphStyle('Sub2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=6)))
            
            cat_grid = [[Paragraph("Attribute Field", header_style), Paragraph("Most Frequent Value(s)", header_style), Paragraph("Distribution Breakdown", header_style)]]
            
            for col, metrics in stats_data["categorical"].items():
                col_name = col.replace('_', ' ')
                
                # Unpack rule-guarded tie elements correctly
                if metrics.get("is_tie", False):
                    winners = ", ".join(metrics["most_frequent"])
                    winner_str = f"{winners} <font color='#c0504d'><b>(Tie Multi-Winner)</b></font>"
                else:
                    winner_str = metrics["most_frequent"]
                    
                counts_str = ", ".join([f"{k}: {v}" for k, v in metrics["value_counts"].items()])
                
                cat_grid.append([
                    Paragraph(col_name, body_style),
                    Paragraph(winner_str, body_style),
                    Paragraph(counts_str, body_style)
                ])
                
            cat_table = Table(cat_grid, colWidths=[130, 170, 204])
            cat_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2e75b6')),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('TOPPADDING', (0,0), (-1,0), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d9d9d9')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')]),
                ('BOTTOMPADDING', (0,1), (-1,-1), 6),
                ('TOPPADDING', (0,1), (-1,-1), 6),
            ]))
            story.append(cat_table)
            story.append(PageBreak())
            
        # ================= PAGE 3: VISUALIZATION CHARTS =================
        if chart_paths:
            story.append(Paragraph("Data Visualization Visual Insights", h1_style))
            story.append(Spacer(1, 10))
            
            for path in chart_paths:
                if os.path.exists(path):
                    # Scale down to cleanly map target page parameters
                    img_flowable = Image(path, width=400, height=240)
                    story.append(img_flowable)
                    
                    # Generate a clean label caption based on file context
                    base_name = os.path.basename(path)
                    caption_text = f"Figure: Data representation extracted from '{base_name.replace('_', ' ')}'."
                    story.append(Paragraph(caption_text, caption_style))
                    story.append(Spacer(1, 15))
                    
    # 4. Render out the assembled pipeline
    doc.build(story)
    return output_path