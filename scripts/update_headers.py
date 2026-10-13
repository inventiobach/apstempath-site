import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    ("index.html", "home"),
    ("g7-roadmap/index.html", "roadmap"),
    ("ap-simulator/index.html", "sim"),
    ("calculator/index.html", "sim"),
    ("scholarship-simulator/index.html", "sim"),
    ("results/index.html", "results"),
    ("pricing/index.html", "pricing"),
    ("about/index.html", "pricing"),
    ("contact/index.html", "contact"),
    ("ap-computer-science-a/index.html", "ap"),
    ("ap-statistics/index.html", "ap"),
    ("ap-calculus-bc/index.html", "ap"),
    ("ap-physics-c/index.html", "ap"),
    ("success/index.html", "none"),
]

def build_header_nav_list(active_key):
    a_home = ' active' if active_key == 'home' else ''
    a_road = ' active' if active_key == 'roadmap' else ''
    a_sim  = ' active' if active_key == 'sim' else ''
    a_res  = ' active' if active_key == 'results' else ''
    a_gui  = ' active' if active_key == 'guides' else ''
    a_ap   = ' active' if active_key == 'ap' else ''
    a_pri  = ' active' if active_key == 'pricing' else ''

    return f"""<header class="site-header">
<div class="container nav-container">
<a class="site-logo" href="/">
<span class="logo-accent">AP</span> STEM PATH
      </a>
<button aria-label="Toggle navigation" class="nav-menu-toggle">☰ Menu</button>
<nav class="main-nav">
<ul class="nav-list">
<li><a class="nav-item{a_home}" href="/">Home</a></li>
<li><a class="nav-item{a_road}" href="/g7-roadmap/">学年別ロードマップ</a></li>
<li class="dropdown">
<a class="nav-item dropdown-toggle{a_sim}" href="/ap-simulator/">ロードマップ診断 ▾</a>
<ul class="dropdown-menu">
<li><a href="/ap-simulator/">10秒 ロードマップ診断</a></li>
<li><a href="/calculator/">AP単位認定シミュレーター</a></li>
<li><a href="/scholarship-simulator/">奨学金＆自己負担シミュレーター</a></li>
</ul>
</li>
<li><a class="nav-item{a_res}" href="/results/">実績・推移</a></li>
<li><a class="nav-item{a_gui}" href="/guides/">専門コラム</a></li>
<li class="dropdown">
<a class="nav-item dropdown-toggle{a_ap}" href="#">AP 専科 ▾</a>
<ul class="dropdown-menu">
<li><a href="/ap-computer-science-a/">AP CS A (Java)</a></li>
<li><a href="/ap-statistics/">AP Statistics (統計)</a></li>
<li><a href="/ap-calculus-bc/">AP Calculus BC (微積分)</a></li>
<li><a href="/ap-physics-c/">AP Physics C (物理)</a></li>
</ul>
</li>
<li class="dropdown">
<a class="nav-item dropdown-toggle{a_pri}" href="/pricing/">料金案内 ▾</a>
<ul class="dropdown-menu">
<li><a href="/pricing/">料金案内</a></li>
<li><a href="/about/">代表講師</a></li>
</ul>
</li>
<li><a class="nav-item cta-nav-item" href="/contact/">無料相談</a></li>
</ul>
</nav>
</div>
</header>"""

def build_header_nav_menu(active_key):
    a_sim = ' class="active"' if active_key == 'sim' else ''
    return f"""<header class="site-header">
    <div class="nav-container">
      <a href="/" class="nav-brand"><span>AP</span> STEM PATH</a>
      <ul class="nav-menu">
        <li><a href="/">Home</a></li>
        <li><a href="/g7-roadmap/">学年別ロードマップ</a></li>
        <li class="dropdown">
          <a href="/ap-simulator/"{a_sim}>ロードマップ診断 &#9662;</a>
          <div class="dropdown-content">
            <a href="/ap-simulator/">10秒 ロードマップ診断</a>
            <a href="/calculator/">AP単位認定シミュレーター</a>
            <a href="/scholarship-simulator/">奨学金＆自己負担シミュレーター</a>
          </div>
        </li>
        <li><a href="/results/">実績・推移</a></li>
        <li><a href="/guides/">専門コラム</a></li>
        <li class="dropdown">
          <a href="#">AP 専科 &#9662;</a>
          <div class="dropdown-content">
            <a href="/ap-computer-science-a/">AP CS A (Java)</a>
            <a href="/ap-statistics/">AP Statistics (統計)</a>
            <a href="/ap-calculus-bc/">AP Calculus BC (微積分)</a>
            <a href="/ap-physics-c/">AP Physics C (物理)</a>
          </div>
        </li>
        <li class="dropdown">
          <a href="/pricing/">料金案内 &#9662;</a>
          <div class="dropdown-content">
            <a href="/pricing/">料金案内</a>
            <a href="/about/">代表講師</a>
          </div>
        </li>
        <li><a href="/contact/" class="btn-cta-nav">無料相談</a></li>
      </ul>
    </div>
  </header>"""

def main():
    for rel_path, active_key in PAGES:
        fp = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(fp):
            print(f"⚠️ Not found: {rel_path}")
            continue
        with open(fp, "r", encoding="utf-8") as f:
            txt = f.read()

        if "nav-menu" in txt and "dropdown-content" in txt:
            new_header = build_header_nav_menu(active_key)
            # Also make dropdown-content align left: 0 so middle dropdowns align cleanly
            txt = re.sub(r'(\.dropdown-content\s*\{[\s\S]*?)right:\s*0;', r'\1left: 0;', txt)
        else:
            new_header = build_header_nav_list(active_key)
            txt = re.sub(r'(\.dropdown-menu\s*\{[\s\S]*?)right:\s*0;', r'\1left: 0;', txt)

        txt_updated, count = re.subn(r'<header class="site-header">[\s\S]*?</header>', new_header, txt, count=1)
        # Update footer link label for guides
        txt_updated = txt_updated.replace('AP STEM Guides (学習ガイド)', '専門コラム')
        txt_updated = txt_updated.replace('AP専門コラム・学習ガイド', '専門コラム')

        if count > 0:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(txt_updated)
            print(f"✅ Updated header & footer in: {rel_path}")
        else:
            print(f"ℹ️ No site-header found in: {rel_path}")

if __name__ == "__main__":
    main()
