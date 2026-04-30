#!/usr/bin/env node
/**
 * Verify every URL in the catalog by loading it in headless Chrome via
 * Puppeteer. Catches what a HEAD request cannot:
 *   - soft 404s (page returns 200 but title says "Page not found")
 *   - redirects to login / auth pages
 *   - JS-rendered "this page no longer exists" banners
 *   - sites that block non-browser User-Agents but pass real browsers
 *
 * Usage:
 *   node .github/scripts/verify_urls_puppeteer.js          # all URLs
 *   node .github/scripts/verify_urls_puppeteer.js --report report.json
 *   node .github/scripts/verify_urls_puppeteer.js --concurrency 8
 *
 * Exits non-zero only on infrastructure failures; URL findings are
 * written to the report file. Read the report to triage.
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..', '..');
const SRC = path.join(ROOT, 'patterns-src');

const SOFT_404_PATTERNS = [
  /\bpage not found\b/i,
  /\b404\b.*not found/i,
  /\bnot found\b.*\b404\b/i,
  /this page (does not exist|no longer exists|is unavailable|could not be found)/i,
  /sorry, (we|that|the page)/i,
  /the requested url .* was not found/i,
  /you can try the homepage/i,
];

const AUTH_REDIRECT_HOSTS = [
  '/login',
  '/sign-in',
  '/signin',
  '/auth/',
  '/oauth',
];


function collectUrls() {
  const urls = new Map(); // url -> [locations]
  const add = (url, location) => {
    if (typeof url !== 'string' || !url.startsWith('http')) return;
    if (!urls.has(url)) urls.set(url, []);
    urls.get(url).push(location);
  };

  for (const file of fs.readdirSync(SRC).filter((f) => f.endsWith('.json'))) {
    const data = JSON.parse(fs.readFileSync(path.join(SRC, file), 'utf8'));
    for (const p of data.patterns || []) {
      const base = `${file}::${p.id}`;
      for (const k of p.known_uses || []) {
        if (k.url) add(k.url, `${base} known_uses(${k.system || ''})`);
      }
      for (const r of p.references || []) {
        if (r.url) add(r.url, `${base} references(${r.title || r.type || ''})`);
      }
      for (const rel of p.related || []) {
        if (rel.url) add(rel.url, `${base} related(${rel.pattern || ''})`);
      }
    }
  }

  for (const extra of ['framework-coverage.json', 'recipes.json']) {
    const fp = path.join(ROOT, extra);
    if (!fs.existsSync(fp)) continue;
    const data = JSON.parse(fs.readFileSync(fp, 'utf8'));
    if (Array.isArray(data.frameworks)) {
      for (const fw of data.frameworks) {
        if (fw.url) add(fw.url, `framework-coverage::${fw.id}`);
      }
    }
  }
  return urls;
}


async function probe(browser, url) {
  const page = await browser.newPage();
  await page.setUserAgent(
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  );
  await page.setViewport({ width: 1280, height: 800 });
  page.setDefaultNavigationTimeout(25000);

  let resp;
  try {
    resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
  } catch (err) {
    await page.close().catch(() => {});
    return { verdict: 'load_failed', error: err.message };
  }

  const status = resp ? resp.status() : 0;
  const finalUrl = page.url();
  let title = '';
  let bodyText = '';
  try {
    title = await page.title();
    bodyText = (await page.evaluate(() => document.body ? document.body.innerText : '')).slice(0, 4000);
  } catch (_) {}
  await page.close().catch(() => {});

  const result = { status, finalUrl, title: title.slice(0, 200) };

  if (status >= 400 && status !== 403 && status !== 429) {
    result.verdict = 'http_error';
    return result;
  }

  for (const host of AUTH_REDIRECT_HOSTS) {
    if (finalUrl.toLowerCase().includes(host) && !url.toLowerCase().includes(host)) {
      result.verdict = 'auth_redirect';
      return result;
    }
  }

  const haystack = `${title}\n${bodyText}`;
  for (const re of SOFT_404_PATTERNS) {
    if (re.test(haystack)) {
      result.verdict = 'soft_404';
      result.matched = re.toString();
      return result;
    }
  }

  result.verdict = 'ok';
  return result;
}


async function main() {
  const args = process.argv.slice(2);
  const reportArg = args.indexOf('--report');
  const reportPath = reportArg >= 0 ? args[reportArg + 1] : path.join(ROOT, 'url-verify-report.json');
  const concArg = args.indexOf('--concurrency');
  const concurrency = concArg >= 0 ? parseInt(args[concArg + 1], 10) : 6;

  const urls = collectUrls();
  const list = Array.from(urls.keys()).sort();
  console.error(`probing ${list.length} unique URLs with concurrency=${concurrency}`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const findings = [];
  const okCount = { value: 0 };
  let i = 0;
  const workers = Array.from({ length: concurrency }, async () => {
    while (true) {
      const idx = i++;
      if (idx >= list.length) return;
      const url = list[idx];
      const t0 = Date.now();
      const res = await probe(browser, url);
      const ms = Date.now() - t0;
      const locations = urls.get(url);
      if (res.verdict === 'ok') {
        okCount.value++;
        process.stderr.write(`  ${(idx+1).toString().padStart(4)}/${list.length}  ok    ${ms}ms  ${url}\n`);
      } else {
        findings.push({ url, locations, ...res });
        process.stderr.write(`  ${(idx+1).toString().padStart(4)}/${list.length}  ${res.verdict.padEnd(13)} ${ms}ms  ${url}\n`);
      }
    }
  });
  await Promise.all(workers);
  await browser.close();

  const report = {
    total: list.length,
    ok: okCount.value,
    findings_count: findings.length,
    by_verdict: findings.reduce((acc, f) => { acc[f.verdict] = (acc[f.verdict] || 0) + 1; return acc; }, {}),
    findings,
  };
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');

  console.error(`\n${list.length} probed, ${okCount.value} ok, ${findings.length} findings`);
  console.error('by verdict:', report.by_verdict);
  console.error(`report: ${reportPath}`);

  process.exit(0);
}


main().catch((err) => {
  console.error('fatal:', err);
  process.exit(2);
});
