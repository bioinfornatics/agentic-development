"""Opt-in browser verification; not imported by unittest discovery.

Serve generated artifacts only. This script never installs browser dependencies.
Evidence must use a new output directory. No production or deployment mutations.
"""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
parser = argparse.ArgumentParser(description="Explicitly run local bilingual browser journeys; requires existing Playwright and Chromium.")
parser.add_argument('--base-url', required=True)
parser.add_argument('--evidence-dir', type=Path, required=True)
args = parser.parse_args()
base = args.base_url
if not base.startswith(('http://127.0.0.1:', 'http://localhost:')) or not base.endswith('/'):
    parser.error('Use a loopback preview URL ending in /; no production probes.')
args.evidence_dir.mkdir(parents=True, exist_ok=False)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]; failed=[]; switches=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('response',lambda r: failed.append([r.url,r.status]) if r.status>=400 else None)
    for locale,name in [('en','English'),('fr','Français')]:
        for route in ['', 'getting-started/', 'cycle/', 'integrations/', 'contributing/']:
            page.goto(base+locale+'/'+route,wait_until='networkidle')
            summary=page.locator('.language-selector summary')
            assert summary.is_visible() and name in summary.inner_text(), 'active label'
            summary.focus(); page.keyboard.press('Enter')
            assert page.locator('.language-selector').evaluate('(el)=>el.open'), 'enter opens'
            other='fr' if locale=='en' else 'en'
            link=page.locator('.language-selector a[hreflang='+other+']')
            assert link.is_visible(), 'choice visible'
            link.click(); page.wait_for_url(base+other+'/'+route); page.wait_for_load_state('networkidle')
            switches.append(locale+'/'+route+' -> '+other+'/'+route)
    page.goto(base+'en/cycle/',wait_until='networkidle')
    page.locator('.language-selector summary').focus(); page.keyboard.press('Space')
    assert page.locator('.language-selector').evaluate('(el)=>el.open'), 'space opens'
    page.keyboard.press('ArrowDown')
    assert page.locator('.language-selector a[hreflang=en]').evaluate('(el)=>el===document.activeElement'), 'first arrow'
    page.keyboard.press('ArrowDown'); page.keyboard.press('Enter')
    page.wait_for_url(base+'fr/cycle/'); page.wait_for_load_state('networkidle')
    page.locator('.language-selector summary').focus();page.keyboard.press('Enter');page.keyboard.press('Escape')
    assert not page.locator('.language-selector').evaluate('(el)=>el.open'), 'escape closes'
    assert page.locator('.language-selector summary').evaluate('(el)=>el===document.activeElement'), 'escape focus'
    page.locator('.language-selector summary').click()
    page.screenshot(path=str(args.evidence_dir / 'desktop.png'),full_page=True)
    page.mouse.click(30, 400)
    assert not page.locator('.language-selector').evaluate('(el)=>el.open'), 'outside closes'
    for width in (320,390,768):
        page.set_viewport_size({'width':width,'height':844})
        page.goto(base+'fr/contributing/',wait_until='networkidle')
        summary=page.locator('.language-selector summary')
        assert summary.is_visible() and 'Français' in summary.inner_text(), 'mobile label'
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'overflow'
        summary.click()
        box=page.locator('.language-selector nav').bounding_box()
        assert box['x']>=0 and box['x']+box['width']<=width, ('dropdown bounds',width,box)
        if width==390:page.screenshot(path=str(args.evidence_dir / 'mobile.png'),full_page=True)
        page.locator('.language-selector a[hreflang=en]').click();page.wait_for_url(base+'en/contributing/');page.wait_for_load_state('networkidle')
    page.goto(base,wait_until='networkidle'); page.wait_for_url(base+'en/')
    nojs=browser.new_context(java_script_enabled=False)
    plain=nojs.new_page(); plain.goto(base+'fr/integrations/')
    plain.locator('.language-selector summary').click()
    plain.locator('.language-selector a[hreflang=en]').click()
    plain.wait_for_url(base+'en/integrations/')
    assert not errors and not failed,(errors,failed)
    (args.evidence_dir / 'browser.json').write_text(json.dumps({'browser_version':browser.version,'switches':switches,'keyboard':'Enter/Space/ArrowDown/Enter/Escape PASS; focus return PASS','mobile_widths':[320,390,768],'overflow':False,'root':'en/ PASS','no_js_switch':'fr/integrations -> en/integrations PASS','pageerrors':errors,'http_errors':failed},indent=2))
    browser.close()
print('Browser PASS: 10 page-equivalent switches; keyboard; mobile320/390/768; no-JS links; root; no observed errors.')
