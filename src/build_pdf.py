"""Build the manuscript and the required 245-word abstract/bio attachment."""
import csv, json, re
from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                              TableStyle, KeepTogether, PageBreak)
from src.make_figures import timing, sensitivity

ROOT=Path(__file__).resolve().parents[1]
WIDTH=A4[0]-108
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyAcademic',fontName='Times-Roman',fontSize=11,
                        leading=14.3,spaceAfter=7.5))
styles.add(ParagraphStyle(name='AcademicTitle',fontName='Times-Bold',fontSize=18,
                        leading=21.5,alignment=TA_CENTER,spaceAfter=14))
styles.add(ParagraphStyle(name='AuthorAcademic',fontName='Times-Roman',fontSize=11,
                        leading=14,alignment=TA_CENTER,spaceAfter=14))
styles.add(ParagraphStyle(name='AcademicH2',fontName='Times-Bold',fontSize=12,
                        leading=15,spaceBefore=13,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='AcademicH3',fontName='Times-Italic',fontSize=11,
                        leading=14,spaceBefore=9,spaceAfter=5,keepWithNext=True))
styles.add(ParagraphStyle(name='CaptionAcademic',fontName='Times-Roman',fontSize=9,
                        leading=11.5,spaceBefore=5,spaceAfter=11))
styles.add(ParagraphStyle(name='CellAcademic',fontName='Times-Roman',fontSize=8.8,leading=11))
styles.add(ParagraphStyle(name='RefAcademic',fontName='Times-Roman',fontSize=9,
                        leading=11.8,spaceAfter=6,leftIndent=17,firstLineIndent=-17))

def markup(text):
    text=escape(text)
    return re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',text)

def para(text,style='BodyAcademic'): return Paragraph(markup(text),styles[style])

def footer(c,doc):
    c.saveState(); c.setStrokeColor(colors.HexColor('#c3c8cb'))
    c.line(54,43,A4[0]-54,43); c.setFont('Times-Roman',8.5)
    c.setFillColor(colors.HexColor('#555555'))
    c.drawString(54,30,'Gupta | Continuity by Permission')
    c.drawRightString(A4[0]-54,30,str(doc.page));c.restoreState()

def table(rows,widths):
    data=[[para(c,'CellAcademic') for c in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9eef2')),
       ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),
       ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),5),
       ('RIGHTPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.7,colors.gray),
       ('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#cbd1d5'))]))
    return t

def table1():
    rows=[['Institutional unit','Reported scope / term','Unresolved assurance question'],
      ['ASEAN coordination [7,8]','Repair permitting and coordination; no service term coded','Dispatch and domestic implementation'],
      ['Tonga [9]','Event-specific exemption; six months from Gazette publication','Event eligibility and later permissions'],
      ['Niue [10]','Spectrum / Internet trial; twelve months','Commencement and continuation terms'],
      ['FSM [11]','Operating licence; 19 Mar 2024-18 Mar 2044','Other permissions and service commitment'],
      ['Sri Lanka [12]','Satellite broadband; 12 Aug 2024-11 Aug 2029','Modification and continuity obligations'],
      ['Kiribati [13]','Interim capacity / IP transit; expiry unreported','Gateway site readiness and commissioning'],
      ['LTMS importer [14]','Imports; two-year extension to 2026','Exact expiry and subsequent renewal'],
      ['LTMS wheeling [15]','Lao PDR transit; two years from Jan 2026 signing','Complete contract and permission alignment']]
    return [table(rows,[120,190,WIDTH-310]),para('Table 1. Documentary comparison. Terms refer to different instruments and are not country resilience scores. Unknowns refer to the reviewed documents, not demonstrated absence of rights. The public ledger supplies locators and document types.','CaptionAcademic')]

def table2():
    rows=[['Hypothetical portfolio','Covered starts','Uncovered starts'],
      ['One path [0,365)','276','89'],
      ['Two paths, both [0,365)','276','89'],
      ['Paths [0,365) and [180,545)','365','0'],
      ['Service [0,365), required site [0,180)','91','274'],
      ['One complete path continued through day 455','365','0']]
    return [table(rows,[WIDTH-150,75,75]),para('Table 2. Exact coverage for a 90-day recovery and candidate starts [0,365), without switching. These synthetic inputs are not named-country licence terms. Every path is assumed to have adequate capacity and satisfied scope. Counts are start days, not empirical cases.','CaptionAcademic')]

def build_paper():
    text=(ROOT/'paper/manuscript.md').read_text()
    blocks=text.split('\n\n'); story=[]
    for block in blocks:
        if block.startswith('# '):story.append(para(block[2:],'AcademicTitle'))
        elif block.startswith('Shivam Gupta\n'):
            story.append(Paragraph('<br/>'.join(escape(x) for x in block.splitlines()),styles['AuthorAcademic']))
        elif block=='[[TABLE1]]': story.extend(table1())
        elif block=='[[TABLE2]]': story.extend(table2())
        elif block=='[[FIGURE1]]':
            story.append(KeepTogether([timing(),para('Figure 1. A shorter required permission constrains the complete path. For effective window [0,180) and R=90, start days 0-90 are covered, represented by [0,91). Hypothetical inputs; not a country case.','CaptionAcademic')]))
        elif block=='[[FIGURE2]]':
            story.append(KeepTogether([sensitivity(),para('Figure 2. Recovery-period coverage declines as duration requirements increase. One path and two co-expiring paths share the blue curve. Staggering or continuation improves coverage under the specified inputs. No switching is assumed; all values come from the released 1,800-row stress grid.','CaptionAcademic')]))
        elif block.startswith('### '):story.append(para(block[4:],'AcademicH3'))
        elif block.startswith('## '):story.append(para(block[3:],'AcademicH2'))
        else: story.append(para(block))
    story.append(PageBreak());story.append(para('References','AcademicH2'))
    sources=json.loads((ROOT/'data/sources.json').read_text())
    for i,s in enumerate(sources,1):
        ref=f'[{i}] {escape(s["author"])} ({escape(s["year"])}). {escape(s["title"])}. <i>{escape(s["publication"])}</i>. <link href="{escape(s["url"],quote=True)}" color="#244d75">Online source</link>.'
        story.append(Paragraph(ref,styles['RefAcademic']))
    story.append(para('All online sources accessed 14 October 2026.','CaptionAcademic'))
    doc=SimpleDocTemplate(str(ROOT/'paper/Continuity_by_Permission_Shivam_Gupta.pdf'),pagesize=A4,
            rightMargin=54,leftMargin=54,topMargin=51,bottomMargin=55,
            title='Continuity by Permission',author='Shivam Gupta')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

def build_submission():
    txt=(ROOT/'paper/submission.txt').read_text()
    before,after=txt.split('\nABSTRACT\n')
    ab,bio=after.split('\nSHORT BIO\n')
    lines=before.strip().split('\n\n')
    story=[para(lines[0],'AcademicTitle'),Paragraph('<br/>'.join(escape(x) for x in lines[1].splitlines()),styles['AuthorAcademic']),para('Abstract','AcademicH2')]
    story += [para(p.strip()) for p in ab.strip().split('\n\n')]
    story += [para('Short bio','AcademicH2'),para(bio.strip())]
    doc=SimpleDocTemplate(str(ROOT/'paper/CAG_Abstract_and_Bio_Shivam_Gupta.pdf'),pagesize=A4,
            rightMargin=54,leftMargin=54,topMargin=51,bottomMargin=55,
            title='CAG Digital Infrastructure Workshop - Abstract and Bio',author='Shivam Gupta')
    doc.build(story)

if __name__=='__main__':build_paper();build_submission();print('Paper and abstract/bio PDFs built')
