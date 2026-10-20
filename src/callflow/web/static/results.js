/* Result view of one callflow run: hero with stats, dashboard tiles, accessible tabs and item cards.
   Exposes window.CallflowResults.render(container, run, result). All data goes through textContent. */
(function () {
  'use strict';

  // Inbox order and titles mirror src/callflow/route.py (Inbox, INBOX_ORDER).
  const INBOXES = [
    ['do_not_do', 'Nie robić (zakazy i odrzucone prośby)'],
    ['tickets', 'Zgłoszenia błędów (dla zespołu technicznego)'],
    ['config_changes', 'Zmiany konfiguracji agenta'],
    ['tasks', 'Zadania zespołu'],
    ['backlog', 'Backlog produktu (prośby o funkcje)'],
    ['waiting_on_client', 'Czekamy na klienta'],
    ['risks', 'Ryzyka klienta (notatka do CRM)'],
    ['on_hold', 'Wstrzymane: nie wracać bez sygnału klienta'],
    ['no_action', 'Informacje i sprawy bez działania'],
  ];
  const KIND_LABELS = {
    bug: 'błąd', config_change: 'zmiana konfiguracji', task: 'zadanie', feature_request: 'prośba o funkcję',
    feedback: 'opinia', risk: 'ryzyko', info: 'informacja',
  };
  const STATE_LABELS = {
    do_now: 'zrobić teraz', scheduled: 'zaplanowane', waiting_on_client: 'czeka na klienta',
    on_hold: 'wstrzymane', do_not_do: 'nie robić', no_action: 'bez działania',
  };
  const NOTICE = 'Nic nie zostało wysłane ani zmienione. Każde działanie zewnętrzne czeka na zatwierdzenie.';

  /* ---------- DOM helpers ---------- */

  function el(tag, props, children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(props || {})) {
      if (value == null || value === false) continue;
      if (key === 'class') node.className = value;
      else if (key === 'text') node.textContent = value;
      else if (key.startsWith('on')) node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value === true ? '' : String(value));
    }
    for (const child of [].concat(children == null ? [] : children)) {
      if (child != null && child !== false) node.append(child instanceof Node ? child : String(child));
    }
    return node;
  }

  const classes = (...names) => names.filter(Boolean).join(' ');
  const shortTitle = (title) => title.split(/ \(|:/)[0];
  const padId = (prefix, index) => prefix + String(index + 1).padStart(2, '0');
  const fold = (text) => String(text || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  function formatDate(iso, withWeekday) {
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    if (!match) return iso || '';
    const date = new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    if (withWeekday) options.weekday = 'short';
    return date.toLocaleDateString('pl-PL', options);
  }

  function formatDuration(seconds) {
    if (typeof seconds !== 'number') return null;
    const total = Math.round(seconds);
    return total < 60 ? `${total} s` : `${Math.floor(total / 60)} min ${String(total % 60).padStart(2, '0')} s`;
  }

  /* ---------- Navigation between tabs and cards ---------- */

  function activate(ctx, key, focusTab) {
    for (const [tabKey, entry] of ctx.tabs) {
      const selected = tabKey === key;
      entry.tab.setAttribute('aria-selected', String(selected));
      entry.tab.tabIndex = selected ? 0 : -1;
      entry.panel.hidden = !selected;
    }
    const entry = ctx.tabs.get(key);
    if (!entry) return;
    keepTabVisible(entry.tab);
    if (focusTab) entry.tab.focus({ preventScroll: true });
  }

  // Scrolls only the horizontally scrolling tab row, never the page.
  function keepTabVisible(tab) {
    const row = tab.parentElement;
    if (tab.offsetLeft < row.scrollLeft) row.scrollLeft = tab.offsetLeft;
    else if (tab.offsetLeft + tab.offsetWidth > row.scrollLeft + row.clientWidth) {
      row.scrollLeft = tab.offsetLeft + tab.offsetWidth - row.clientWidth;
    }
  }

  function onTabKey(ctx, event) {
    const keys = [...ctx.tabs.keys()].filter((key) => !ctx.tabs.get(key).tab.hidden);
    const current = keys.indexOf(event.target.dataset.key);
    const moves = { ArrowRight: current + 1, ArrowLeft: current - 1, Home: 0, End: keys.length - 1 };
    if (current < 0 || !(event.key in moves)) return;
    event.preventDefault();
    activate(ctx, keys[(moves[event.key] + keys.length) % keys.length], true);
  }

  function showSection(ctx, key) {
    activate(ctx, key, true);
    ctx.tabsBar.scrollIntoView({ block: 'start' });
  }

  function jumpTo(ctx, id) {
    const target = ctx.cards.get(id);
    if (!target) return;
    activate(ctx, target.tabKey);
    const search = ctx.tabs.get(target.tabKey).search;
    if (target.card.hidden && search) {
      search.value = '';
      search.dispatchEvent(new Event('input'));
    }
    target.card.scrollIntoView({ block: 'start' });
    target.card.focus({ preventScroll: true });
    target.card.classList.remove('rv-flash');
    void target.card.offsetWidth; // restart the highlight animation
    target.card.classList.add('rv-flash');
    clearTimeout(target.flashTimer);
    target.flashTimer = setTimeout(() => target.card.classList.remove('rv-flash'), 2000);
  }

  function refLink(ctx, id) {
    if (!ctx.cards.has(id)) return el('span', { class: 'rv-ref rv-ref--missing', title: 'Brak takiej pozycji', text: id });
    const label = ctx.titles.get(id);
    return el('button', {
      type: 'button', class: 'rv-ref', title: label ? `${id} · ${label}` : id,
      onclick: () => jumpTo(ctx, id), text: id,
    });
  }

  function refList(ctx, ids) {
    const wrap = el('span', { class: 'rv-refs' });
    ids.forEach((id) => wrap.append(refLink(ctx, id)));
    return wrap;
  }

  /* ---------- Building blocks ---------- */

  function facts(rows) {
    const present = rows.filter(([, value]) => value != null && value !== '' && !(Array.isArray(value) && !value.length));
    if (!present.length) return null;
    return el('dl', { class: 'rv-facts' }, present.flatMap(([label, value]) => [
      el('dt', { text: label }),
      el('dd', null, Array.isArray(value) ? (value.length > 1 ? el('ul', null, value.map((v) => el('li', { text: v }))) : value[0]) : value),
    ]));
  }

  function evidenceList(checks, fallback) {
    // Quotes come from the verification step; evidence without a check is shown as unverified.
    const rows = checks || (fallback || []).map((ev) => ({ speaker: ev.speaker, quote: ev.quote, line: null, verified: false }));
    const list = el('ul', { class: 'rv-quotes', 'aria-label': 'Cytaty z rozmowy' });
    if (!rows.length) list.append(el('li', { class: 'rv-quote rv-quote--bad', text: '⚠️ brak cytatu' }));
    for (const check of rows) {
      const where = check.line != null ? `l. ${check.line}` : 'brak w transkrypcji';
      const mark = check.verified ? '✅ zweryfikowany' : '⚠️ niezweryfikowany';
      list.append(el('li', { class: classes('rv-quote', !check.verified && 'rv-quote--bad') }, [
        el('span', { class: 'rv-quote-meta' }, [el('strong', { text: check.speaker }), ` · ${where} · ${mark}`]),
        el('blockquote', { text: `„${check.quote}”` }),
      ]));
    }
    return list;
  }

  function cardHead(id, title, extra) {
    return el('h3', { class: 'rv-card-title' }, [el('span', { class: 'rv-id', text: id }), ' · ', title, extra]);
  }

  function itemCard(ctx, item) {
    const doNot = item.state === 'do_not_do';
    const due = [item.due_date && formatDate(item.due_date, true), item.due_text && `(„${item.due_text}”)`].filter(Boolean).join(' ');
    const card = el('article', {
      class: classes('rv-card', doNot && 'rv-card--danger', item.needs_review && 'rv-card--review'), tabindex: '-1',
    }, [
      cardHead(item.id, item.title),
      el('div', { class: 'badges rv-badges' }, [
        el('span', { class: 'badge rv-kind', title: item.kind, text: KIND_LABELS[item.kind] || item.kind }),
        el('span', { class: `badge rv-state rv-state--${item.state}`, title: item.state, text: STATE_LABELS[item.state] || item.state }),
        item.needs_review && el('span', { class: 'badge rv-review', text: '⚠️ do sprawdzenia' }),
      ]),
      item.details && el('p', { class: 'rv-details', text: item.details }),
      facts([
        ['Właściciel', item.owner],
        ['Termin', due],
        ['Warunek', item.condition],
        ['Zatwierdza', item.approval_by],
        ['Wersja ostateczna', item.final_value],
        ['Zastępuje', item.superseded || []],
        ['Ograniczenia', item.constraints || []],
        ['Zależy od', item.depends_on && item.depends_on.length ? refList(ctx, item.depends_on) : null],
      ]),
      evidenceList(ctx.quotes[item.id], item.evidence),
    ]);
    card.dataset.search = fold(`${item.id} ${item.title} ${item.details}`);
    ctx.cards.get(item.id).card = card;
    return card;
  }

  function guardrailCard(ctx, guardrail, index) {
    const id = padId('G', index);
    const card = el('article', { class: 'rv-card rv-card--guard', tabindex: '-1' }, [
      cardHead(id, guardrail.rule),
      facts([['Obowiązuje do', guardrail.until], ['Zdejmuje', guardrail.approval_by]]),
      evidenceList(ctx.quotes[id], guardrail.evidence),
    ]);
    ctx.cards.get(id).card = card;
    return card;
  }

  function draftCard(ctx, draft, index) {
    const id = padId('D', index);
    const body = el('pre', { class: 'rv-draft-body', tabindex: '0', 'aria-label': `Treść szkicu ${id}`, text: draft.body });
    const status = el('span', { class: 'rv-copy-status', role: 'status' });
    const card = el('article', { class: 'rv-card rv-card--draft', tabindex: '-1' }, [
      el('p', { class: 'rv-draft-label', text: 'szkic — nie wysłano' }),
      cardHead(id, draft.subject),
      facts([
        ['Do', draft.to],
        ['Wysłać', draft.send_when],
        ['Dotyczy', draft.related_items && draft.related_items.length ? refList(ctx, draft.related_items) : null],
      ]),
      body,
      el('div', { class: 'rv-card-actions' }, [
        el('button', { type: 'button', class: 'btn btn-secondary btn-sm', onclick: () => copyDraft(body, status), text: 'Kopiuj treść' }),
        status,
      ]),
    ]);
    ctx.cards.get(id).card = card;
    return card;
  }

  async function copyDraft(body, status) {
    try {
      await navigator.clipboard.writeText(body.textContent);
      status.textContent = 'Skopiowano do schowka.';
    } catch (error) {
      const range = document.createRange();
      range.selectNodeContents(body);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      body.focus();
      status.textContent = 'Treść zaznaczona: naciśnij Ctrl+C (Cmd+C), aby skopiować.';
    }
    clearTimeout(status.timer);
    status.timer = setTimeout(() => { status.textContent = ''; }, 5000);
  }

  function emptyNote(text) {
    return el('p', { class: 'rv-empty', text });
  }

  function panelHead(title, lead) {
    return [el('h2', { class: 'rv-panel-title', text: title }), lead && el('p', { class: 'rv-lead', text: lead })];
  }

  /* ---------- Panels ---------- */

  function summaryPanel(result) {
    const participants = result.participants || [];
    const assumptions = result.assumptions || [];
    return [
      ...panelHead('Podsumowanie rozmowy'),
      el('p', { class: 'rv-summary', text: result.summary_text || 'Brak podsumowania.' }),
      participants.length && el('div', { class: 'rv-block' }, [
        el('h3', { class: 'rv-block-title', text: 'Uczestnicy' }),
        el('ul', { class: 'rv-chips' }, participants.map((name) => el('li', { text: name }))),
      ]),
      assumptions.length && el('div', { class: 'rv-block' }, [
        el('h3', { class: 'rv-block-title', text: 'Założenia przyjęte przy analizie' }),
        el('ol', { class: 'rv-assumptions' }, assumptions.map((text) => el('li', { text }))),
      ]),
    ];
  }

  function guardrailsPanel(ctx, guardrails) {
    return [
      ...panelHead('Zabezpieczenia', 'Zakazy i blokady z rozmowy. Sprawdź je przed każdym działaniem na koncie klienta.'),
      guardrails.length
        ? el('div', { class: 'rv-cards' }, guardrails.map((g, i) => guardrailCard(ctx, g, i)))
        : emptyNote('W rozmowie nie padły żadne zakazy ani blokady.'),
    ];
  }

  function calendarPanel(ctx, calendar) {
    const entries = calendar.slice().sort((a, b) => String(a.date).localeCompare(String(b.date)));
    const rows = entries.map((entry) => {
      const item = ctx.items.get(entry.item);
      const meta = item ? [STATE_LABELS[item.state] || item.state, item.owner].filter(Boolean).join(' · ') : '';
      return el('li', null, [
        el('time', { datetime: entry.date, text: formatDate(entry.date, true) }),
        el('div', null, [
          refLink(ctx, entry.item), ' ',
          el('span', { class: 'rv-timeline-title', text: item ? item.title : 'nieznana pozycja' }),
          meta && el('span', { class: 'rv-timeline-meta', text: meta }),
        ]),
      ]);
    });
    return [
      ...panelHead('Terminy', 'Kalendarz i przypomnienia. Wpisy trafią do kalendarza dopiero po zatwierdzeniu.'),
      rows.length ? el('ol', { class: 'rv-timeline' }, rows) : emptyNote('Brak pozycji z konkretną datą.'),
    ];
  }

  function inboxPanel(ctx, key, title, inbox) {
    const items = inbox.items || [];
    const cards = items.map((item) => itemCard(ctx, item));
    const count = el('p', { class: 'rv-filter-count', 'aria-live': 'polite' });
    const empty = emptyNote('Żadna pozycja nie pasuje do wyszukiwania.');
    empty.hidden = true;
    const search = el('input', {
      type: 'search', id: `rv-search-${key}`, class: 'rv-search-input', placeholder: 'Tytuł lub opis…', autocomplete: 'off',
      oninput: () => {
        const query = fold(search.value.trim());
        let shown = 0;
        cards.forEach((card) => { card.hidden = !card.dataset.search.includes(query); shown += card.hidden ? 0 : 1; });
        empty.hidden = shown > 0;
        count.textContent = query ? `Pokazano ${shown} z ${cards.length}` : '';
      },
    });
    ctx.tabs.get(key).search = search;
    return [
      ...panelHead(title),
      el('p', { class: 'rv-target' }, ['System docelowy: ', el('strong', { text: inbox.target || '—' })]),
      items.length > 1 && el('div', { class: 'rv-search' }, [
        el('label', { for: search.id, text: 'Szukaj w tej sekcji' }), search, count,
      ]),
      el('div', { class: 'rv-cards' }, cards),
      empty,
    ];
  }

  function draftsPanel(ctx, drafts) {
    return [
      ...panelHead('Szkice wiadomości', 'Gotowe do przejrzenia. Żaden szkic nie jest wysyłany automatycznie.'),
      drafts.length
        ? el('div', { class: 'rv-cards' }, drafts.map((d, i) => draftCard(ctx, d, i)))
        : emptyNote('Rozmowa nie wymaga wiadomości do klienta.'),
    ];
  }

  function issuesPanel(ctx, issues) {
    return [
      ...panelHead('Ostrzeżenia walidacji', 'Pozycje z ostrzeżeniem mają oznaczenie „do sprawdzenia”. Zweryfikuj je przed działaniem.'),
      el('ul', { class: 'rv-issues' }, issues.map((issue) => el('li', null, [refLink(ctx, issue.id), ' ', issue.message]))),
    ];
  }

  /* ---------- Hero and dashboard ---------- */

  function hero(run, outbox) {
    const summary = run.summary || {};
    const verified = summary.quotes_verified;
    const total = summary.quotes_total;
    // Example runs make no model call, so they have no cost and no model time: those chips are hidden.
    const live = run.mode !== 'example';
    const duration = formatDuration(summary.duration_s != null ? summary.duration_s : live ? run.elapsed_s : null);
    const cost = typeof summary.cost_usd === 'number' ? `$${summary.cost_usd.toFixed(2)}` : null;
    const stats = [
      ['Pozycje', summary.items],
      ['Zabezpieczenia', summary.guardrails],
      ['Szkice', summary.drafts],
      ['Cytaty', total != null ? `${verified}/${total}` : null, verified < total],
      ['Ostrzeżenia', summary.issues, summary.issues > 0],
      ['Czas', duration],
      ['Koszt', cost],
    ].filter(([, value]) => value != null);
    const date = outbox.meeting_date || summary.meeting_date;
    const files = run.files || {};
    return el('header', { class: 'hero rv-hero' }, el('div', { class: 'wrap' }, [
      el('p', { class: 'rv-eyebrow', text: run.mode === 'example' ? 'Wynik analizy · zapisany przykład' : 'Wynik analizy' }),
      el('h1', { id: 'rv-title', tabindex: '-1', text: outbox.client || summary.client || 'Klient nieznany' }),
      el('p', { class: 'meta' }, [
        'Spotkanie: ', el('strong', { text: date ? formatDate(date, true) : 'data nieznana' }),
        ' · źródło: ', el('code', { text: run.source_name || '—' }),
      ]),
      el('ul', { class: 'stats', 'aria-label': 'Statystyki' }, stats.map(([label, value, warn]) =>
        el('li', { class: warn ? 'stat-warn' : null }, [`${label}: `, el('strong', { text: String(value) })]))),
      el('p', { class: 'notice', role: 'note', text: NOTICE }),
      ...(run.warnings || []).map((text) => el('p', { class: 'note-warn', role: 'note', text: `⚠️ ${text}` })),
      run.files && el('div', { class: 'rv-files' }, [
        files.report_html && el('a', { class: 'btn btn-light', href: files.report_html, target: '_blank', rel: 'noopener', text: 'Otwórz raport HTML' }),
        files.report_md && el('a', { class: 'btn btn-ghost rv-btn-dark', href: files.report_md, download: 'report.md', text: 'Pobierz report.md' }),
        files.outbox && el('a', { class: 'btn btn-ghost rv-btn-dark', href: files.outbox, download: 'outbox.json', text: 'Pobierz outbox.json' }),
      ]),
    ]));
  }

  function dashboard(ctx, tiles) {
    return el('nav', { class: 'rv-dashboard', 'aria-label': 'Przegląd wyniku' }, el('ul', null, tiles.map((tile) =>
      el('li', null, el('button', {
        type: 'button', class: classes('rv-tile', tile.danger && 'rv-tile--danger', !tile.count && 'rv-tile--zero'),
        onclick: () => showSection(ctx, tile.key),
      }, [
        el('span', { class: 'rv-tile-count', text: String(tile.count) }),
        el('span', { class: 'rv-tile-label', text: tile.label }),
      ])))));
  }

  /* ---------- Entry point ---------- */

  function render(container, run, result) {
    run = run || {};
    result = result || {};
    const outbox = result.outbox || {};
    const inboxes = outbox.inboxes || {};
    const guardrails = outbox.guardrails || [];
    const drafts = outbox.drafts || [];
    const calendar = outbox.calendar || [];
    const issues = outbox.issues || [];
    const known = new Set(INBOXES.map(([name]) => name));
    const inboxList = INBOXES.concat(Object.keys(inboxes).filter((name) => !known.has(name)).map((name) => [name, name]))
      .filter(([name]) => inboxes[name] && (inboxes[name].items || []).length);

    const ctx = { tabs: new Map(), cards: new Map(), items: new Map(), titles: new Map(), quotes: result.quotes || {} };
    // Register every card target first, so references can link forward (A02 depends on A05).
    for (const [name] of inboxList) {
      for (const item of inboxes[name].items) {
        ctx.items.set(item.id, item);
        ctx.titles.set(item.id, item.title);
        ctx.cards.set(item.id, { tabKey: `inbox-${name}` });
      }
    }
    guardrails.forEach((g, i) => { ctx.cards.set(padId('G', i), { tabKey: 'guardrails' }); ctx.titles.set(padId('G', i), g.rule); });
    drafts.forEach((d, i) => { ctx.cards.set(padId('D', i), { tabKey: 'drafts' }); ctx.titles.set(padId('D', i), d.subject); });

    const sections = [
      { key: 'summary', label: 'Podsumowanie', build: () => summaryPanel(result) },
      { key: 'guardrails', label: 'Zabezpieczenia', count: guardrails.length, build: () => guardrailsPanel(ctx, guardrails) },
      { key: 'calendar', label: 'Terminy', count: calendar.length, build: () => calendarPanel(ctx, calendar) },
      ...inboxList.map(([name, title]) => ({
        key: `inbox-${name}`, label: shortTitle(title), count: inboxes[name].items.length, danger: name === 'do_not_do',
        build: () => inboxPanel(ctx, `inbox-${name}`, title, inboxes[name]),
      })),
      { key: 'drafts', label: 'Szkice', count: drafts.length, build: () => draftsPanel(ctx, drafts) },
      issues.length && { key: 'issues', label: 'Ostrzeżenia', count: issues.length, danger: true, build: () => issuesPanel(ctx, issues) },
    ].filter(Boolean);

    const tablist = el('div', { class: 'rv-tabs', role: 'tablist', 'aria-label': 'Sekcje wyniku', onkeydown: (e) => onTabKey(ctx, e) });
    const panels = el('div', { class: 'rv-panels' });
    for (const section of sections) {
      const tab = el('button', {
        type: 'button', role: 'tab', id: `rv-tab-${section.key}`, 'aria-controls': `rv-panel-${section.key}`,
        class: classes('rv-tab', section.danger && 'rv-tab--danger'), 'data-key': section.key,
        onclick: () => activate(ctx, section.key),
      }, [section.label, section.count != null && el('span', { class: 'rv-tab-count', text: String(section.count) })]);
      const panel = el('section', {
        role: 'tabpanel', id: `rv-panel-${section.key}`, 'aria-labelledby': tab.id, tabindex: '0', class: 'rv-panel',
      });
      tablist.append(tab);
      panels.append(panel);
      ctx.tabs.set(section.key, { tab, panel });
    }
    // Panels are built after all tabs exist: inbox panels register their search input on the tab entry.
    for (const section of sections) {
      for (const child of [].concat(section.build())) if (child) ctx.tabs.get(section.key).panel.append(child);
    }
    ctx.tabsBar = el('div', { class: 'rv-tabs-bar' }, tablist);

    const tiles = sections.filter((s) => s.key !== 'summary' && s.key !== 'issues')
      .map((s) => ({ key: s.key, label: s.label, count: s.count, danger: s.danger && s.count > 0 }));
    container.replaceChildren(el('div', { class: 'rv' }, [
      hero(run, outbox),
      el('div', { class: 'wrap rv-body' }, [dashboard(ctx, tiles), ctx.tabsBar, panels]),
    ]));
    activate(ctx, 'summary');
  }

  window.CallflowResults = { render };
})();
