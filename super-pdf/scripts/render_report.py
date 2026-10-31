from pathlib import Path
import re, html, json, hashlib, argparse, tempfile, os
from urllib.parse import urlparse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
SKILL=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Wrap a Markdown report in the approved Brayl PDF skin.')
parser.add_argument('--input',required=True,type=Path)
parser.add_argument('--output',required=True,type=Path)
parser.add_argument('--config',required=True,type=Path)
parser.add_argument('--sources',type=Path)
args=parser.parse_args()
SOURCE=args.input.resolve(); OUT=args.output.resolve()
config=json.loads(args.config.read_text())
for key in ['title','running_header','footer']:
 if not isinstance(config.get(key),str): raise ValueError('Config requires string: '+key)
FONT=SKILL/'assets/fonts'
OUT.parent.mkdir(parents=True,exist_ok=True)
work=tempfile.TemporaryDirectory(prefix='super-pdf-');TMP=Path(work.name)
attachments={}
for item in config.get('attachments',[]):
 path=Path(item['path']).expanduser()
 if not path.is_absolute():path=args.config.resolve().parent/path
 path=path.resolve();name=item.get('name',path.name)
 if name in attachments:raise ValueError('Duplicate attachment name: '+name)
 if not path.is_file():raise FileNotFoundError(path)
 attachments[name]=path
appendix=json.loads(args.sources.read_text()) if args.sources else None
external_urls=set()
for name,file in [('Inter','Inter-Regular.ttf'),('Inter-Bold','Inter-Semibold.ttf'),('Inter-Italic','Inter-Italic.ttf'),('Inter-BoldItalic','Inter-SemiboldItalic.ttf'),('Serif','InstrumentSerif-Regular.ttf'),('Mono','SplineSansMono-Regular.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Inter',normal='Inter',bold='Inter-Bold',italic='Inter-Italic',boldItalic='Inter-BoldItalic')
NAVY=colors.HexColor('#1a1a1a');TEAL=colors.HexColor('#7c7cff');INK=colors.HexColor('#1a1a1a');PALE=colors.HexColor('#fafaf9');LINE=colors.HexColor('#e5e5e5')
styles={
'body':ParagraphStyle('body',fontName='Inter',fontSize=10,leading=14.7,textColor=INK,spaceAfter=9,allowWidows=0,allowOrphans=0),
'h1':ParagraphStyle('title',fontName='Serif',fontSize=32,leading=34,textColor=NAVY,spaceAfter=12,keepWithNext=True),
'h2':ParagraphStyle('heading',fontName='Serif',fontSize=22,leading=26,textColor=NAVY,spaceBefore=17,spaceAfter=9,keepWithNext=True),
'meta':ParagraphStyle('meta',fontName='Mono',fontSize=8.2,leading=12,textColor=TEAL,spaceAfter=15),
'cell':ParagraphStyle('cell',fontName='Inter',fontSize=8.7,leading=12.8,textColor=INK,spaceAfter=0),
'firstcell':ParagraphStyle('firstcell',fontName='Inter',fontSize=8.3,leading=12.8,textColor=NAVY,spaceAfter=0),
'head':ParagraphStyle('head',fontName='Mono',fontSize=7.8,leading=11,textColor=colors.HexColor('#1a1a1a')),
'num':ParagraphStyle('num',fontName='Inter',fontSize=8.7,leading=12.8,textColor=INK,alignment=TA_RIGHT),
'list':ParagraphStyle('list',fontName='Inter',fontSize=10,leading=14.7,textColor=INK,leftIndent=15,firstLineIndent=-15,spaceAfter=9,allowWidows=0,allowOrphans=0)
}
def norm(s):return s.replace('\u2013','-').replace('\u2014',' - ').replace('\u2011','-')
def inline(s):
 s=norm(s); tokens=[]
 def link(m):
  label,url=m.groups();url=html.unescape(url)
  if urlparse(url).scheme in ('http','https'):
   external_urls.add(url)
   v='<link href="'+html.escape(url,quote=True)+'" color="#6868D8">'+html.escape(label)+'</link>'
  else:
   target=Path(url)
   if not target.is_absolute():target=SOURCE.parent/target
   matched=[name for name,path in attachments.items() if path==target.resolve()]
   if not matched:raise ValueError('Local link must map to an explicit attachment: '+url)
   v=html.escape(label)+' ('+html.escape(matched[0])+', embedded attachment)'
  tokens.append(v);return f'ZZLINK{len(tokens)-1}ZZ'
 # Supports one nested parenthesis pair in a URL; complex Markdown needs adaptation.
 s=re.sub(r'\[([^\]]+)\]\(((?:[^()\s]|\([^()\s]*\))+)\)',link,s);s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b><font color="#000000">\1</font></b>',s)
 s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
 for i,v in enumerate(tokens):s=s.replace(f'ZZLINK{i}ZZ',v)
 return s
class Doc(SimpleDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='heading':
   key=f'h{self.seq.nextf("heading")}';self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0,False)
def page(c,doc):
 w,h=A4;c.saveState();c.drawImage(str(SKILL/'assets/brayl-logo.png'),44,h-59,width=88,height=28.865,mask='auto')
 c.setFont('Mono',6.8);c.setFillColor(colors.HexColor('#1a1a1a'));c.drawRightString(w-44,h-44,config['running_header'])
 c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(44,h-73,w-44,h-73);c.line(44,37,w-44,37)
 c.setFont('Mono',6.8);c.setFillColor(colors.HexColor('#1a1a1a'));c.drawString(44,24,config['footer']);c.setFillColor(TEAL);c.drawRightString(w-44,24,str(doc.page));c.restoreState()
text=SOURCE.read_text();lines=text.splitlines();story=[];i=0;table_index=0;W=A4[0]-88
# Reject unsupported blocks explicitly; never silently drop report material.
for line in lines:
 if re.match(r'^\s*(?:```|~~~|>|!\[|<|#{3,} |[-*_]{3,}\s*$)',line) or re.match(r'^\s{2,}(?:[-*+] |\d+\. )',line) or '`' in line:
  raise ValueError('Unsupported Markdown construct; adapt renderer or convert explicitly: '+line[:100])
for key in ['running_header','footer']:
 limit=W-112 if key=='running_header' else W-25
 if pdfmetrics.stringWidth(config[key],'Mono',6.8)>limit:raise ValueError(key+' is too long; shorten metadata only.')
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line.startswith('# '):story.append(Paragraph(inline(line[2:]),styles['h1']));i+=1;continue
 if line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['h2']));i+=1;continue
 if line.startswith('|'):
  rows=[]; alignments=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
   if all(re.fullmatch(r':?-+:?',c) for c in cells):alignments=['right' if c.endswith(':') and not c.startswith(':') else 'left' for c in cells]
   else:rows.append(cells)
   i+=1
  cols=len(rows[0]);table_index+=1
  if any(len(row)!=cols for row in rows):raise ValueError('Inconsistent table column count')
  options=config.get('tables',{}).get(str(table_index),{})
  ratios=options.get('widths', [.23,.35,.42] if cols==3 else [1/cols]*cols)
  if len(ratios)!=cols or any(v<=0 for v in ratios):raise ValueError('Invalid table widths')
  widths=[W*v/sum(ratios) for v in ratios]
  right_columns=options.get('right_columns',[j for j,a in enumerate(alignments) if a=='right'])
  data=[]
  for k,row in enumerate(rows):data.append([Paragraph(inline(v),styles['head' if k==0 else 'num' if j in right_columns else 'firstcell' if j==0 else 'cell']) for j,v in enumerate(row)])
  tab=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1)
  commands=[('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.5,LINE),('BOX',(0,0),(-1,-1),.5,LINE)]
  for k in range(1,len(rows)):
   # Quiet white table body with hairline row separators.
   commands.append(('LINEBELOW',(0,k),(-1,k),.5,LINE))
  if options.get('total_row',False):commands.extend([('BACKGROUND',(0,len(rows)-1),(-1,-1),colors.HexColor('#F2F2FF')),('LINEABOVE',(0,len(rows)-1),(-1,-1),.5,TEAL)])
  tab.setStyle(TableStyle(commands));story.extend([Spacer(1,4),tab,Spacer(1,12)]);continue
 if config.get('subtitle') and line==config['subtitle']:story.append(Paragraph(inline(line),styles['meta']));i+=1;continue
 if re.match(r'^\d+\. ',line) or line.startswith('- '):
  if line.startswith('- '):line='• '+line[2:]
  story.append(Paragraph(inline(line),styles['list']));i+=1;continue
 para=[line];i+=1
 while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ')) and not re.match(r'^\d+\. ',lines[i]):para.append(lines[i].strip());i+=1
 story.append(Paragraph(inline(' '.join(para)),styles['body']))
# Full sourcing is the default for sourced reports; omission must be explicit.
body_urls=set(external_urls)
if body_urls and appendix is None and not config.get('omit_sources',False):
 raise ValueError('Sourced report requires --sources, or explicitly authorized omit_sources=true.')
if appendix:
 entries=appendix.get('entries',[])
 supplied={e['url'] for e in entries}|{u for e in entries for u in e.get('extra_urls',[])}
 missing=body_urls-supplied
 if missing:raise ValueError('Missing appendix references: '+str(sorted(missing)))
 for e in entries:
  for key in ['author','date','title','url','note']:
   if not e.get(key):raise ValueError('Reference requires '+key)
 refhead=ParagraphStyle('reference-heading',fontName='Inter-Bold',fontSize=9,leading=13,textColor=colors.black,spaceAfter=4)
 refbody=ParagraphStyle('reference-body',fontName='Inter',fontSize=8.6,leading=12.2,textColor=INK,spaceAfter=4)
 refurl=ParagraphStyle('reference-url',fontName='Inter',fontSize=8,leading=10.5,textColor=colors.HexColor('#6868D8'),spaceAfter=4,wordWrap='CJK')
 story.extend([PageBreak(),Paragraph(html.escape(appendix.get('title','Sources appendix')),styles['h2'])])
 if appendix.get('intro'):story.extend([Paragraph(inline(appendix['intro']),styles['body']),Spacer(1,8)])
 for number,entry in enumerate(entries,1):
  title=f"[{number:02d}] {entry['author']} ({entry['date']}). {entry['title']}"
  block=[Paragraph(html.escape(norm(title)),refhead)]
  if entry.get('detail'):block.append(Paragraph(html.escape(norm(entry['detail'])),refbody))
  for url in [entry['url']]+entry.get('extra_urls',[]):
   if urlparse(url).scheme not in ('http','https'):raise ValueError('Reference URL must be http(s)')
   escaped=html.escape(url,quote=True)
   block.append(Paragraph('<link href="'+escaped+'">'+escaped+'</link>',refurl))
  block.append(Paragraph(inline('**Use and limits:** '+entry['note']),refbody))
  trace=[]
  if entry.get('report_labels'):trace.append('**Report link:** '+', '.join(entry['report_labels'])+'.')
  if entry.get('source_id'):trace.append('**Source record:** '+entry['source_id']+'.')
  if trace:block.append(Paragraph(inline(' '.join(trace)),refbody))
  block.append(Spacer(1,10));story.append(KeepTogether(block))
 for number,item in enumerate(appendix.get('supplements',[]),len(entries)+1):
  block=[Paragraph(html.escape(f"[{number:02d}] {item['title']}"),refhead),Paragraph(inline(item['text']),refbody)]
  names=item.get('attachments',[])
  if any(name not in attachments for name in names):raise ValueError('Supplement references absent attachment')
  if names:block.append(Paragraph(html.escape('Embedded files: '+'; '.join(names)+'.'),refbody))
  story.append(KeepTogether(block))
doc=Doc(str(TMP/'render.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=88,bottomMargin=51,title=config['title'],author=config.get('author',''),pageCompression=1)
doc.build(story,onFirstPage=page,onLaterPages=page)
r=PdfReader(TMP/'render.pdf');w=PdfWriter();w.clone_document_from_reader(r)
for name,path in attachments.items():w.add_attachment(name,path.read_bytes())
staged=TMP/'final.pdf';w.write(staged)
# Validate structural invariants before publishing the artifact.
check=PdfReader(staged)
assert all(len(page.images)==1 for page in check.pages), 'Missing page logo'
for name,path in attachments.items():assert check.attachments[name][0]==path.read_bytes()
shutil_copy=__import__('shutil').copyfile
shutil_copy(staged,OUT)
record={'output':str(OUT),'pages':len(check.pages),'source':str(SOURCE),'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'output_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'body_external_urls':sorted(body_urls),'references':len(appendix.get('entries',[])) if appendix else 0,'attachments':{name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in attachments.items()},'visual_review':'pending'}
OUT.with_suffix('.export.json').write_text(json.dumps(record,indent=2)+'\n')
work.cleanup();print(json.dumps(record))
