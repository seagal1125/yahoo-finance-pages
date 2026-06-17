from pathlib import Path
from datetime import datetime
import re

repo = Path('/Users/minim4/.openclaw/workspace/yahoo-finance-pages')
digests = repo / 'digests'
ts = '2026-06-17-1350'
pretty = '2026-06-17 13:50 CST'
out = digests / f'{ts}.html'

html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Yahoo Finance Digest｜{pretty}</title>
  <style>
    :root{{--bg:#f3f6fb;--panel:#ffffff;--panel-soft:rgba(255,255,255,.78);--text:#132033;--muted:#607086;--line:#d8e1ec;--accent:#2563eb;--accent2:#0f766e;--danger:#b91c1c;--danger-bg:#fff1f2;--shadow:0 18px 48px rgba(15,23,42,.08);--radius-xl:28px;--radius-lg:22px;--radius-md:16px;--max:1180px;}}
    *{{box-sizing:border-box}} html{{scroll-behavior:smooth}} body{{margin:0;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--text);background:radial-gradient(circle at top left, rgba(37,99,235,.11), transparent 28%),radial-gradient(circle at top right, rgba(15,118,110,.10), transparent 26%),linear-gradient(180deg,#f7f9fc 0%,#eef3f8 100%);line-height:1.72}}
    a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
    .shell{{max-width:var(--max);margin:0 auto;padding:28px 18px 72px}} .hero{{position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.6);background:linear-gradient(135deg, rgba(255,255,255,.93), rgba(240,247,255,.86));backdrop-filter:blur(12px);border-radius:var(--radius-xl);box-shadow:var(--shadow);padding:34px}}
    .hero:before{{content:"";position:absolute;inset:auto -60px -60px auto;width:220px;height:220px;border-radius:999px;background:radial-gradient(circle, rgba(37,99,235,.16), transparent 68%)}}
    .eyebrow{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}} .pill{{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:rgba(255,255,255,.74);border:1px solid var(--line);color:#28425f;font-size:.87rem;font-weight:700}}
    h1,h2,h3{{margin:0;line-height:1.18}} h1{{font-size:clamp(2.15rem,5vw,3.5rem);letter-spacing:-.03em;margin-bottom:14px}} h2{{font-size:1.38rem;letter-spacing:-.02em;margin-bottom:16px}} h3{{font-size:1rem;margin:0 0 12px;color:#28425f}}
    .lead{{max-width:860px;font-size:1.08rem;color:#213246;margin:0}} .meta{{margin-top:16px;color:var(--muted);font-size:.96rem}} .meta strong{{color:var(--text)}}
    .summary-grid,.top-grid,.section-grid{{display:grid;gap:18px;margin-top:22px}} .summary-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}} .top-grid{{grid-template-columns:1.15fr .85fr}} .section-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}
    .card{{background:var(--panel-soft);border:1px solid rgba(255,255,255,.7);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:24px;backdrop-filter:blur(10px)}} .card.compact{{padding:20px}}
    .kicker{{font-size:.82rem;text-transform:uppercase;letter-spacing:.12em;color:var(--accent2);font-weight:800;margin-bottom:10px}} .summary-item strong{{display:block;font-size:1.08rem;margin-bottom:8px;letter-spacing:-.01em}} .summary-item p{{margin:0;color:#33465d}}
    .list{{margin:0;padding-left:22px}} .list li{{margin:0 0 12px}} .list li:last-child{{margin-bottom:0}}
    .source-block{{display:flex;flex-wrap:wrap;gap:10px}} .chip{{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;background:#fff;border:1px solid var(--line);color:#24415f;font-size:.93rem;box-shadow:0 8px 22px rgba(15,23,42,.05)}}
    .risk{{border:1px solid #fecdd3;background:linear-gradient(180deg,#fff8f8,#fff1f2)}} .risk h2{{color:var(--danger)}}
    .ptt-article{{padding:18px;border:1px solid var(--line);border-radius:16px;background:#fff;margin-bottom:16px}} .ptt-article:last-child{{margin-bottom:0}}
    .ptt-meta{{color:var(--muted);font-size:.94rem;margin-bottom:10px}} .mini-title{{font-size:.95rem;font-weight:800;margin:14px 0 8px;color:#28425f}}
    .footer{{margin-top:28px;padding:18px 22px;border-radius:18px;background:rgba(255,255,255,.74);border:1px solid var(--line);display:flex;flex-wrap:wrap;gap:12px 20px;color:var(--muted);font-size:.92rem}}
    code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#194170}}
    @media (max-width:900px){{.summary-grid,.top-grid,.section-grid{{grid-template-columns:1fr}}.hero{{padding:26px}}}}
    @media (max-width:640px){{.shell{{padding:18px 14px 56px}}.hero,.card{{padding:20px}}h1{{font-size:2rem}}.lead{{font-size:1rem}}}}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="eyebrow">
        <span class="pill">Midday Digest</span>
        <span class="pill">Asia/Taipei 13:50</span>
        <span class="pill">Traditional Chinese</span>
      </div>
      <h1>Yahoo Finance Digest</h1>
      <p class="lead">午盤不是全面風險退潮，而是<strong>台股電子修正、金融塑膠撐盤、國際市場重新交易「美伊停火 + 油價回落 + 科技反彈」</strong>。盤面最值得注意的是：台灣資金從權值半導體抽離後，仍在找金融、傳產與個別 AI／被動元件題材承接；美股端則由油價降溫與風險偏好回升帶動指數續彈。</p>
      <p class="meta"><strong>時間：</strong>{pretty}（Asia/Taipei）</p>
    </section>

    <section class="summary-grid">
      <article class="card summary-item compact">
        <div class="kicker">市場輪廓</div>
        <strong>全球 risk appetite 回溫，但台股是結構性輪動</strong>
        <p>美股由停火與油價回落推動續漲；台股卻是半導體回檔、金融與塑膠接棒，顯示午盤主軸是資金換手，不是同方向共振。</p>
      </article>
      <article class="card summary-item compact">
        <div class="kicker">台股焦點</div>
        <strong>外資空單高、台積電承壓，但指數跌深後有承接</strong>
        <p>早盤一度重挫逾 600 點，市場開始把焦點轉向金融、面板、MLCC 與個別 ASIC/AI 供應鏈。</p>
      </article>
      <article class="card summary-item compact">
        <div class="kicker">午後觀察</div>
        <strong>看電子是否止穩、傳產金融能否撐到收盤</strong>
        <p>若權值續弱、只靠題材股撐盤，收斂仍偏技術性；若電子跌幅再縮，才有機會把盤勢從防守轉回中性。</p>
      </article>
    </section>

    <section class="top-grid">
      <article class="card">
        <div class="kicker">Executive summary</div>
        <h2>重點摘要</h2>
        <ul class="list">
          <li><strong>全球市場：</strong>Yahoo Finance（Global）顯示美股主線重新回到停火與油價回落。S&amp;P 500、道瓊、Nasdaq 全數上揚，油價回到 80 美元附近，VIX 走低，代表短線風險情緒明顯修復。</li>
          <li><strong>台股盤中：</strong>Yahoo 台灣、CNA 與鉅亨共同指向同一件事：<strong>台積電與電子權值壓盤</strong>，但塑膠、金融與部分題材股接手，指數跌勢逐步收斂，屬於盤中換股而非單邊崩跌。</li>
          <li><strong>熱門題材：</strong>面板（群創）、MLCC 漲價、金融股撐盤、士電/AIDC、ASIC 與先進封裝消息持續吸睛；PTT 討論熱度則集中在<strong>分析師數據化、三星/Intel 製程話題、外資空單是否套利</strong>。</li>
          <li><strong>午後關鍵：</strong>如果台積電與電子股回穩，今天有機會從「重挫日」轉成「高檔震盪整理日」；若無法止穩，金融與傳產只能降低跌幅，難以逆轉結構壓力。</li>
        </ul>
      </article>
      <article class="card risk">
        <div class="kicker">Risk watch</div>
        <h2>風險／變數</h2>
        <ul class="list">
          <li><strong>電子權值壓力未解：</strong>費半前夜大跌後，台積電仍是最直接的指數風險來源。</li>
          <li><strong>外資空單訊號：</strong>若期貨避險/套利倉未明顯回補，市場對反彈延續度會保持保守。</li>
          <li><strong>全球風險偏好反覆：</strong>美伊停火若生變，油價與避險情緒可能快速反轉。</li>
          <li><strong>題材股過熱：</strong>面板、MLCC、個別 AI/ASIC 概念股若追價過急，容易在大盤不穩時先被獲利了結。</li>
        </ul>
      </article>
    </section>

    <section class="section-grid">
      <article class="card">
        <div class="kicker">Yahoo Finance (Global)</div>
        <h2>全球市場</h2>
        <ul class="list">
          <li>Yahoo Finance 首頁顯示主要美股指數全面走強：<strong>S&amp;P 500 +1.65%、Nasdaq +3.07%、道瓊 +0.92%</strong>，反映市場正在交易風險降溫與科技股反彈。</li>
          <li>首頁主軸新聞集中在<strong>美國與伊朗達成停火/重啟荷莫茲海峽安排</strong>，帶動市場對油供與通膨壓力的擔憂下降。</li>
          <li><strong>原油約 81.41 美元、VIX 16.13</strong>，代表能源與波動率都較前段時間舒緩，對股市風險資產估值有利。</li>
          <li>科技與成長題材仍是流量中心，Yahoo 首頁同時把 <strong>SpaceX、AI、Fed 新主席 Kevin Warsh 首次會議</strong> 放在核心版位，表示市場並未脫離成長敘事，只是短線先被總體利空緩解所放大。</li>
        </ul>
      </article>

      <article class="card">
        <div class="kicker">Yahoo Finance (台灣)</div>
        <h2>台灣市場</h2>
        <ul class="list">
          <li>Yahoo 台灣首頁與新聞頁午盤訊號很一致：<strong>台股早盤一度大跌逾 600 點、台積電盤中一度跌 50 元</strong>，但後續跌勢收斂，顯示低檔有承接。</li>
          <li>盤面焦點不是全面弱，而是<strong>金融股逆勢撐盤、塑膠與部分傳產補位</strong>；Yahoo 顯著新聞直接點到「台股跌金融股照漲、7 家金控大象跳舞」。</li>
          <li>個股與族群題材方面，<strong>群創一度漲 9%、MLCC 漲價三階段、ASIC/先進封裝、主動式 ETF 新募集</strong> 都是流量高點，代表資金仍在找電子內的次族群與非電子替代主線。</li>
          <li>Yahoo 新聞也把<strong>士電股東會、台電融資、台灣 GDP 樂觀預估</strong>放進盤中討論，說明今天不只是純技術面殺盤，還有產業與政策敘事在搶注意力。</li>
        </ul>
      </article>

      <article class="card">
        <div class="kicker">CNA 中央社｜股市</div>
        <h2>今日市場重點</h2>
        <ul class="list">
          <li>中央社盤中主線很清楚：<strong>費半重挫拖累台積電等電子股回檔</strong>，加權指數早盤最低下探 45159 點附近，但盤中由塑膠與金融接棒，跌勢收斂。</li>
          <li><strong>士電</strong>是今日企業面亮點之一，公司在股東會釋出 AIDC、台電建設、能源轉型、北美外銷等五大成長動能，全年營收與獲利力拚雙位數成長。</li>
          <li>政策與總體方面，CNA 同步提到<strong>台電 3000 億專案貸款、再生能源占比上升、經濟成長率上修接近 10%</strong>，這些訊息對電力、基建與景氣循環股形成一定支撐。</li>
          <li>整體來看，中央社給出的盤勢結論是：<strong>電子修正是真的，但台股並非全面失速，盤中正在尋找由非電子族群承接的平衡點。</strong></li>
        </ul>
      </article>

      <article class="card">
        <div class="kicker">鉅亨網</div>
        <h2>5 則最值得看</h2>
        <ul class="list">
          <li><strong>三星代工迎轉機：</strong>鉅亨頭條強調因台積電產能吃緊，Google、AMD 與比亞迪都被點名可能與三星深化合作，市場重新關注先進製程第二供應來源。</li>
          <li><strong>新 Fed 主席首秀：</strong>鉅亨把 Kevin Warsh 首次主持利率會議列為高關注事件，若語氣偏鷹，科技股去槓桿壓力可能放大。</li>
          <li><strong>士電/AIDC 題材延續：</strong>士電股東會釋出國內 AIDC 與外銷成長動能，呼應台灣盤中資金對電力基建與 AI 基礎設施的偏好。</li>
          <li><strong>運價與供應鏈風險仍在：</strong>即使停火讓油價回落，鉅亨仍強調伊朗戰事前的搶運與供應鏈緊張，代表全球製造與物流並未完全回到無風險狀態。</li>
          <li><strong>SpaceX 與 AI 熱度外溢：</strong>SpaceX IPO 後延伸到 ETF、選擇權與 AI 供應鏈新聞，說明市場人氣仍集中在高敘事成長資產。</li>
        </ul>
      </article>
    </section>

    <section class="card">
      <div class="kicker">PTT 股市版</div>
      <h2>PTT 股市版</h2>
      <div class="ptt-article">
        <h3>[心得] 我用 Fable 分析了哲哲六年半的發文</h3>
        <div class="ptt-meta">100 推｜ntutaiwanwin（wally）｜06/17 12:43</div>
        <div class="mini-title">文章內容重點</div>
        <ul class="list">
          <li>作者抓了分析師「哲哲」六年半、共 2953 則公開發文，配對大盤與關鍵詞後做量化回測。</li>
          <li>結論不是大家愛講的「反指標」，而是<strong>極度樂觀時後市仍偏強，真正有訊號的是極度恐慌時，通常代表跌勢未完。</strong></li>
          <li>更有意思的是「怎麼說」比「說什麼」重要：發文頻率越高但點名越窄，後市越弱；點名廣度越高，通常對應較健康的普漲行情。</li>
        </ul>
        <div class="mini-title">推文重點</div>
        <ul class="list">
          <li>多數推文把這篇當成有料的數據實驗，敲碗作者繼續分析其他分析師或後半段策略效益。</li>
          <li>也有人質疑是否只是替分析師做流量，但反對聲量明顯小於支持與玩梗。</li>
          <li>整體氣氛偏正面，版友接受「用資料看老師」這種二階觀察。</li>
        </ul>
        <div class="mini-title">重點摘要</div>
        <p>這篇爆紅不是因為哪檔股票，而是因為它把散戶熟悉的分析師話題做成量化研究。版上情緒顯示，市場在震盪時反而更愛這種「能把噪音做成訊號」的內容。</p>
      </div>

      <div class="ptt-article">
        <h3>[新聞] 世界最小電晶體！三星首次實現邏輯半導體垂直堆疊</h3>
        <div class="ptt-meta">81 推｜madeinheaven｜06/17 12:17</div>
        <div class="mini-title">文章內容重點</div>
        <ul class="list">
          <li>三星宣稱首次做到 42 奈米邏輯半導體 3D 垂直堆疊，將記憶體領域的垂直堆疊概念延伸到邏輯晶片。</li>
          <li>論文入選 2026 VLSI 最佳論文，核心賣點是突破平面微縮極限、提升 AI 與 HPC 晶片的面積效率與功耗表現。</li>
          <li>內文重點仍停留在技術展示與商業化前期，距離量產與搶單還有距離。</li>
        </ul>
        <div class="mini-title">推文重點</div>
        <ul class="list">
          <li>推文一半在玩「GG 崩了」梗，另一半則質疑實際量產性、散熱與商業價值。</li>
          <li>有版友提到這更像研究成果，不代表立刻能威脅台積電。</li>
          <li>整體情緒是<strong>有科技話題熱度，但市場不願直接買單成真競爭力。</strong></li>
        </ul>
        <div class="mini-title">重點摘要</div>
        <p>這篇反映的不是三星真要翻盤，而是市場對任何能挑戰台積電技術敘事的新聞都高度敏感。推文看起來熱鬧，實際態度偏保守、偏看戲。</p>
      </div>

      <div class="ptt-article">
        <h3>[新聞] 英特爾 18A-P 進風險試產！朝蘋果訂單邁進</h3>
        <div class="ptt-meta">81 推｜AnimalSpirit｜06/17 09:57</div>
        <div class="mini-title">文章內容重點</div>
        <ul class="list">
          <li>Intel 18A-P 進入風險試產，被視為爭取蘋果等大型客戶代工與先進封裝訂單的關鍵一步。</li>
          <li>報導核心在良率：若首月能接近 90%，才有機會真正吸引外部大客戶。</li>
          <li>文章也點出台積電在 Arm 生態、先進封裝與既有客戶信任上仍明顯領先。</li>
        </ul>
        <div class="mini-title">推文重點</div>
        <ul class="list">
          <li>多數推文對 Intel 保持懷疑，認為又是一次「故事先行、客戶未到」。</li>
          <li>也有人認為先進封裝可能比晶圓代工更有機會切入，這比製程節點本身更值得看。</li>
          <li>台積電「完了」類留言依舊很多，但明顯屬於版上日常反串。</li>
        </ul>
        <div class="mini-title">重點摘要</div>
        <p>Intel 18A-P 在 PTT 的解讀偏向「值得看，但先別信太多」。市場情緒不是認定 Intel 要翻身，而是把它當成可能影響台積電長線議價與封裝競爭的觀察點。</p>
      </div>

      <div class="ptt-article">
        <h3>[請益] 外資 7 萬口空單是在做期現套利嗎？</h3>
        <div class="ptt-meta">54 推｜Hodge｜06/17 13:15</div>
        <div class="mini-title">文章內容重點</div>
        <ul class="list">
          <li>原 PO 問的是：外資巨大空單若表面上看似逆風，是否其實在搭配現貨、正二、摩台或轉倉做套利/避險。</li>
        </ul>
        <div class="mini-title">推文重點</div>
        <ul class="list">
          <li>回覆多數認為不能只看表面空單，因為外資可能搭配現貨部位、正價差與次月轉倉。</li>
          <li>也有人直接認為就是被軋到，但更多版友傾向把它視為結算結構與策略性部位管理。</li>
        </ul>
        <div class="mini-title">重點摘要</div>
        <p>這串顯示午盤最真實的散戶問題不是「哪檔會漲」，而是「外資到底在幹嘛」。當市場震盪大、電子權值承壓時，結構性部位與衍生品解讀會明顯升溫。</p>
      </div>

      <div class="mini-title">熱門主題總結</div>
      <ul class="list">
        <li><strong>主題一｜用數據看市場話語權：</strong>「哲哲分析」爆紅，代表散戶不只想看老師喊單，還想看誰能把市場情緒做成可驗證的訊號。這和今天整體盤勢很搭：盤面雜訊大，大家更想找方法論。</li>
        <li><strong>主題二｜台積電挑戰者敘事持續吸睛：</strong>三星 3D 邏輯堆疊、Intel 18A-P 風險試產都被高熱度討論，但推文普遍認為離真正威脅台積電還有距離。也就是說，話題熱度高於資本市場的即時信任度。</li>
        <li><strong>主題三｜外資空單與盤面結構焦慮：</strong>外資部位、期現套利與轉倉成為午後熱門問題，代表投資人對今天這種「電子殺、非電撐」的盤面仍然不安心，會持續追問反彈是真是假。</li>
      </ul>
    </section>

    <section class="section-grid">
      <article class="card">
        <div class="kicker">Cross-market takeaways</div>
        <h2>跨市場觀察</h2>
        <ul class="list">
          <li><strong>全球與台股沒有同步強弱。</strong>美股是風險回補、科技反彈；台股則是電子修正後由金融、塑膠與個別題材撐場。</li>
          <li><strong>油價回落是今天全球市場最重要的背景板。</strong>它幫美股降壓，但台股還在消化前一晚費半重挫與台積電壓力，所以受益沒有完全傳導。</li>
          <li><strong>AI/半導體敘事仍是資金主軸，只是從大權值往細分族群擴散。</strong>從 Yahoo、鉅亨到 PTT 都能看到 ASIC、先進封裝、製程競爭、AIDC 與面板/MLCC 的討論升溫。</li>
        </ul>
      </article>
      <article class="card">
        <div class="kicker">Source links</div>
        <h2>來源連結</h2>
        <div class="source-block">
          <a class="chip" href="https://finance.yahoo.com/">finance.yahoo.com</a>
          <a class="chip" href="https://tw.stock.yahoo.com/">tw.stock.yahoo.com</a>
          <a class="chip" href="https://tw.stock.yahoo.com/news">tw.stock.yahoo.com/news</a>
          <a class="chip" href="https://feeds.feedburner.com/rsscna/finance">CNA 財經 RSS</a>
          <a class="chip" href="https://www.cnyes.com/">鉅亨網首頁</a>
          <a class="chip" href="https://news.cnyes.com/news/cat/headline">鉅亨頭條</a>
          <a class="chip" href="https://www.ptt.cc/bbs/Stock/index.html">PTT 股市版（以 helper script 取得）</a>
        </div>
      </article>
    </section>

    <div class="footer">
      <span>Model used: <code>openai-codex/gpt-5.4</code></span>
      <span>Generated at: <code>{pretty}</code></span>
      <span>Repository: <code>yahoo-finance-pages</code></span>
    </div>
  </main>
</body>
</html>
'''

out.write_text(html, encoding='utf-8')

# update index
index = repo / 'index.html'
files = []
for p in sorted(digests.glob('*.html'), reverse=True):
    name = p.stem
    m = re.match(r'(\d{{4}}-\d{{2}}-\d{{2}})-(\d{{4}})', name)
    if m:
        pretty_ts = f"{{m.group(1)}} {{m.group(2)[:2]}}:{{m.group(2)[2:]}} CST"
    else:
        pretty_ts = name
    files.append((p.name, pretty_ts))
latest_name, latest_pretty = files[0]
items = '\n'.join([f'<li><a href="digests/{{name}}">{{label}}</a></li>' for name, label in files])
index_html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Yahoo Finance Digests</title><style>:root{{--bg:#f3f6fb;--panel:#fff;--text:#132033;--muted:#607086;--line:#d8e1ec;--accent:#2563eb;--accent2:#0f766e;--shadow:0 18px 48px rgba(15,23,42,.08);--radius-xl:28px;--radius-lg:22px;--max:1100px}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--text);background:radial-gradient(circle at top left, rgba(37,99,235,.11), transparent 28%),radial-gradient(circle at top right, rgba(15,118,110,.08), transparent 26%),linear-gradient(180deg,#f7f9fc 0%,#eef3f8 100%);line-height:1.65}}a{{color:var(--accent);text-decoration:none}}a:hover{{text-decoration:underline}}.shell{{max-width:var(--max);margin:0 auto;padding:28px 18px 64px}}.hero,.card{{background:rgba(255,255,255,.82);border:1px solid rgba(255,255,255,.7);border-radius:var(--radius-xl);box-shadow:var(--shadow);backdrop-filter:blur(10px)}}.hero{{padding:34px}}.card{{padding:24px;border-radius:var(--radius-lg);margin-top:22px}}h1,h2{{margin:0 0 12px;line-height:1.15}}h1{{font-size:clamp(2rem,5vw,3.2rem);letter-spacing:-.03em}}h2{{font-size:1.35rem;letter-spacing:-.02em}}.muted{{color:var(--muted)}}.pill{{display:inline-block;padding:8px 14px;border-radius:999px;background:#eef5ff;border:1px solid #d7e4fb;color:#24415f;font-weight:700;font-size:.88rem;margin-bottom:16px}}.latest-link{{display:inline-flex;align-items:center;gap:8px;padding:12px 16px;border-radius:14px;background:#fff;border:1px solid var(--line);font-weight:700}}ul{{margin:0;padding-left:20px}}li{{margin:0 0 10px}}.history a{{font-weight:600}}</style></head><body><main class="shell"><section class="hero"><span class="pill">Yahoo Finance Digest Archive</span><h1>Yahoo Finance Digests</h1><p class="muted">集中整理每次排程產出的盤前、早盤、盤中、盤後市場摘要。最新一篇放最上面，底下保留完整歷史。</p></section><section class="card"><h2>最新 Digest</h2><p class="muted">{latest_pretty}</p><a class="latest-link" href="digests/{latest_name}">開啟最新摘要</a></section><section class="card history"><h2>歷史列表</h2><ul>{items}</ul></section></main></body></html>'''
index.write_text(index_html, encoding='utf-8')
print(out)
