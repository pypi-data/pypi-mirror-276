import Utils.Generic as Generic;
import os;

from reportlab.lib.pagesizes import A4;
from reportlab.lib import colors;
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle;
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle;

def GeneratePdf(client_info, orders):
    try:
        now = Generic.now();
        now_month = now.month if now.month > 9 else f"0{now.month}";
        now_day = now.day if now.day > 9 else f"0{now.day}";
        now_hour = now.hour if now.hour > 9 else f"0{now.hour}";
        now_minute = now.minute if now.minute > 9 else f"0{now.minute}";
        now_second = now.second if now.second > 9 else f"0{now.second}";

        file_path = f"{now.year}/{now_month}";
        if not os.path.exists(file_path):
            os.makedirs(file_path);
        file_path = f"{file_path}/{now_day}_{now_hour}{now_minute}{now_second}.pdf";
        file_path = "test.pdf";

        size_societyName = 25;
        margin = 10;
        doc = SimpleDocTemplate(
            file_path, 
            pagesize=A4, 
            leftMargin=margin, 
            rightMargin=margin, 
            topMargin=margin, 
            bottomMargin=margin
        );

        content = [];
        styles = getSampleStyleSheet();

        header_table_data = [
            [
                Paragraph(
                    f"<font color='red' size={size_societyName}>M</font><font color='black' size={size_societyName}>A</font> SRLS", 
                    ParagraphStyle(
                        name=any,
                        parent=styles['Normal'],
                        fontName='Times-Roman',  # Cambia con il tuo font preferito
                        fontSize=12
                    )
                ), 
                "Preventivo"
            ],
            [
                "", 
                ""
            ],
            [
                Paragraph(
                    f"Via Cefalonia 24, Brescia (BS)", 
                    ParagraphStyle(
                        name=any,
                        parent=styles['Normal'],
                        fontName='Times-Roman',
                    )
                ), 
                f"Spettabile {client_info['name']}"
            ],
            [
                Paragraph(
                    f"P.IVA 04033430986", 
                    ParagraphStyle(
                        name=any,
                        parent=styles['Normal'],
                        fontName='Times-Roman',
                    )
                ), 
                ""
            ]
        ];
            
        header_table_style = TableStyle([
            # startcol, startrow - endcol, endrow
            ('FONT',(0, 0), (1, 0), 'Times-Bold'),
            ('SIZE',(0, 0), (1, 0), 15),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('TEXTCOLOR', (0, 0), (1, 0), colors.red)
        ]);
        
        header_table = Table(header_table_data, colWidths=[doc.width / 2 - 10, doc.width / 2 - 10]);
        header_table.setStyle(header_table_style);
        content.append(header_table);

        content.append(Spacer(1, 10))  # Aggiungi spaziatura

        body_table_data = [
            [
                "Descrizione", 
                "Quantità",
                "Prezzo",
                "Totale (no IVA)"
            ]
        ];
        for order in orders:
            body_table_data.append(ToParagraph_ForTable(order.Description, order.Quantity, order.Price, order.Total));

        body_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            ('TEXTCOLOR', (0, 0), (-1, -1), colors.red),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ]);
        body_table = Table(
            body_table_data,
            colWidths=[370,48,60,80]
        );
        body_table.setStyle(body_table_style);
        content.append(body_table);

        content.append(Spacer(1, 12))  # Aggiungi spaziatura
        content.append(Paragraph("Il tuo testo qui", styles['Normal']))

        # Build the PDF
        doc.build(content);

        print(f'PDF generated successfully at: {file_path}');
    except Exception as e:
        print(f'Error generating PDF: {e}');


def ToParagraph_ForTable(Description, Quantity, Price, Total):
    style = ParagraphStyle(
        name="Centered",
        parent=getSampleStyleSheet()['Normal'],
        fontName='Times-Roman',
        alignment=1 # 0=left, 1=center, 2=right
    );
    return [
        Paragraph(
            f"{Description}"
        ),
        Paragraph(
            f"{Quantity}", 
            style
        ),
        Paragraph(
            f"{Price}€", 
            style
        ),
        Paragraph(
            f"{Total}€", 
            style
        )
    ];