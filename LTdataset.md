---
layout: single
title: "Lithium Triangle Brine and Water Dataset"
permalink: /LTdataset/
author_profile: false
---

<p>
Lithium Triangle Brine and Water Dataset. Information on data compilation is available in the README.
&nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.xlsx">[Download Excel]</a>
&nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.csv">[Download CSV]</a>
&nbsp;<a href="/files/data/LT/LiTriangleDataset_README.md">[Download README]</a>
</p>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

<style>
  #lt-map {
    height: 580px; width: 100%;
    border: 1px solid #ccc; border-radius: 4px;
    margin: 1em 0 0 0; background: #b8cfe0;
  }
  #map-controls {
    background: #f9f9f9;
    border: 1px solid #ccc; border-radius: 4px;
    padding: 9px 14px; margin: 6px 0 4px 0;
    font-size: 0.84em; color: #111;
    display: flex; flex-wrap: wrap; gap: 8px 0;
    align-items: flex-start;
  }
  #basemap-switcher {
    display: flex; align-items: center; gap: 8px;
    padding-right: 16px; margin-right: 16px;
    border-right: 1px solid #ddd; flex-shrink: 0;
  }
  #basemap-switcher strong { color: #111; white-space: nowrap; }
  .bm-btn {
    padding: 3px 10px; border-radius: 3px; cursor: pointer;
    border: 1px solid #bbb; background: #fff;
    font-size: 0.84em; color: #111;
    transition: background 0.15s, color 0.15s; user-select: none;
  }
  .bm-btn.active { background: #333; color: #fff; border-color: #333; }
  .bm-btn:not(.active):hover { background: #eee; }
  #layer-section { flex: 1; }
  #layer-section strong { color: #111; display: block; margin-bottom: 5px; }
  .layer-grid { display: flex; flex-wrap: wrap; gap: 4px 12px; }
  .layer-item {
    display: flex; align-items: center; gap: 6px;
    padding: 3px 7px; border-radius: 3px; cursor: pointer;
    user-select: none; transition: background 0.15s;
  }
  .layer-item:hover { background: #efefef; }
  .layer-item.hidden { opacity: 0.45; }
  .layer-item.hidden:hover { opacity: 0.65; background: #efefef; }
  .layer-item input[type=checkbox] { cursor: pointer; margin: 0; accent-color: #333; }
  .layer-dot {
    width: 12px; height: 12px; border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.25); flex-shrink: 0;
  }
  .layer-item label { cursor: pointer; color: #111; white-space: nowrap; }
  #map-status { font-size: 0.79em; color: #888; margin: 2px 0 1.5em 0; }
  #map-status.error { color: #c0392b; font-weight: bold; }
  .lt-popup {
    max-height: 340px; overflow-y: auto;
    min-width: 230px; max-width: 360px; font-size: 0.81em;
  }
  .lt-popup h3 {
    margin: 0 0 6px 0; font-size: 1em;
    border-bottom: 1px solid #e0e0e0; padding-bottom: 4px; color: #111;
  }
  .lt-popup table { width: 100%; border-collapse: collapse; }
  .lt-popup tr:nth-child(even) { background: #f6f6f6; }
  .lt-popup td { padding: 2px 5px; vertical-align: top; color: #111; }
  .lt-popup td:first-child {
    font-weight: bold; color: #444;
    white-space: nowrap; padding-right: 8px; min-width: 85px;
  }
  .lt-popup .na { color: #bbb; font-style: italic; }
</style>

<div id="lt-map"></div>

<div id="map-controls">
  <div id="basemap-switcher">
    <strong>Basemap:</strong>
    <span class="bm-btn active" id="btn-satellite" onclick="ltSwitchBasemap('satellite')">Satellite</span>
    <span class="bm-btn" id="btn-light" onclick="ltSwitchBasemap('light')">Street Map</span>
  </div>
  <div id="layer-section">
    <strong>Toggle Sample Types:</strong>
    <div class="layer-grid" id="layer-grid">Loading…</div>
  </div>
</div>

<div id="map-status">Loading data…</div>

<script>
(function () {

  var CSV_URL = '/files/data/LT/Supplement_LiTriangleDataset.csv';
  var TIMEOUT_MS = 15000; // 15 seconds before showing a helpful error

  var statusEl = document.getElementById('map-status');
  function setStatus(msg, isError) {
    statusEl.textContent = msg;
    statusEl.className = isError ? 'error' : '';
  }

  /* ── Timeout watchdog — catches silent 404s ── */
  var loadTimer = setTimeout(function () {
    setStatus(
      'ERROR: Could not load the data file at ' + CSV_URL +
      '. Please make sure Supplement_LiTriangleDataset.csv has been uploaded to /files/data/LT/ in your GitHub repo.',
      true
    );
  }, TIMEOUT_MS);

  /* ── Colors ── */
  var PALETTE = {
    'Brine':          '#e63946',
    'Marginal Brine': '#ff6b6b',
    'Stream':         '#2a9d8f',
    'River':          '#48cae4',
    'Spring':         '#52b788',
    'Thermal Spring': '#f4a261',
    'Geothermal':     '#fb8500',
    'Lake':           '#457b9d',
    'Underground':    '#8338ec',
    'Seep':           '#6d6875',
    'Rain':           '#80b918'
  };
  function typeColor(t) { return PALETTE[(t||'').trim()] || '#888888'; }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  var SKIP_COLS = ['lat','latitude','long','longitude','lon','x','y'];

  function buildPopup(row) {
    var name = row['Sample ID']||row['Name']||row['Station']||'';
    var type = row['Type']||'';
    var html = '<div class="lt-popup"><h3>'+esc(name||type||'Sample')+'</h3><table>';
    for (var c in row) {
      if (SKIP_COLS.indexOf(c.toLowerCase()) !== -1) continue;
      var v = row[c];
      var empty = (v===null||v===undefined||v===''||
                   String(v).toLowerCase()==='na'||
                   String(v).toLowerCase()==='nd');
      html += '<tr><td>'+esc(c)+'</td>';
      html += empty ? '<td class="na">—</td>' : '<td>'+esc(String(v))+'</td>';
      html += '</tr>';
    }
    return html + '</table></div>';
  }

  function findCol(headers, candidates) {
    for (var i=0;i<candidates.length;i++)
      for (var j=0;j<headers.length;j++)
        if (headers[j] && headers[j].trim().toLowerCase()===candidates[i].toLowerCase())
          return headers[j];
    return null;
  }

  /* ── Basemap layers ── */
  var tileLayers = {
    satellite: L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Esri, Maxar, Earthstar Geographics',
        maxZoom: 19
      }
    ),
    light: L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: 'abcd', maxZoom: 19
      }
    )
  };
  var currentBasemap = 'satellite';

  var map = L.map('lt-map', { center: [-23, -67], zoom: 6 });
  tileLayers.satellite.addTo(map);

  var layerGroups  = {};
  var layerVisible = {};

  window.ltSwitchBasemap = function(name) {
    if (name === currentBasemap) return;
    map.removeLayer(tileLayers[currentBasemap]);
    tileLayers[name].addTo(map);
    for (var t in layerGroups) {
      if (layerVisible[t]) {
        map.removeLayer(layerGroups[t]);
        layerGroups[t].addTo(map);
      }
    }
    currentBasemap = name;
    document.getElementById('btn-satellite').classList.toggle('active', name==='satellite');
    document.getElementById('btn-light').classList.toggle('active', name==='light');
  };

  /* ── Fetch CSV via XMLHttpRequest first to catch 404s clearly ── */
  var xhr = new XMLHttpRequest();
  xhr.open('GET', CSV_URL, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState !== 4) return;
    clearTimeout(loadTimer);
    if (xhr.status === 404 || xhr.status === 0) {
      setStatus(
        'ERROR: Data file not found at ' + CSV_URL +
        '. Please upload Supplement_LiTriangleDataset.csv to /files/data/LT/ in your GitHub repo.',
        true
      );
      return;
    }
    if (xhr.status < 200 || xhr.status >= 300) {
      setStatus('ERROR: Could not load CSV (HTTP ' + xhr.status + ').', true);
      return;
    }
    /* File loaded — parse it */
    var results = Papa.parse(xhr.responseText, {
      header: true,
      skipEmptyLines: true
    });
    processData(results.data);
  };
  xhr.onerror = function() {
    clearTimeout(loadTimer);
    setStatus('ERROR: Network error loading ' + CSV_URL + '. Check the file exists in your repo.', true);
  };
  xhr.send();

  /* ── Process parsed rows ── */
  function processData(data) {
    if (!data || !data.length) {
      setStatus('ERROR: CSV file is empty or could not be parsed.', true);
      return;
    }

    var headers = Object.keys(data[0]);
    var latCol  = findCol(headers, ['Lat','Latitude','LAT','LATITUDE']);
    var lonCol  = findCol(headers, ['Long','Longitude','LON','LONG','LONGITUDE','Lon']);
    var typeCol = findCol(headers, ['Type','TYPE','type','Sample Type']);

    if (!latCol || !lonCol) {
      setStatus('ERROR: Could not find Lat/Lon columns. Columns found: ' + headers.join(', '), true);
      return;
    }

    var plotted=0, skipped=0, bounds=[];

    data.forEach(function(row) {
      var lat = parseFloat(row[latCol]);
      var lon = parseFloat(row[lonCol]);
      if (isNaN(lat) || isNaN(lon)) { skipped++; return; }
      var type = typeCol ? (row[typeCol]||'Unknown').trim() : 'Unknown';

      if (!layerGroups[type]) {
        layerGroups[type]  = L.layerGroup().addTo(map);
        layerVisible[type] = true;
      }

      L.circleMarker([lat, lon], {
        radius: 6, fillColor: typeColor(type),
        color: '#fff', weight: 1.2,
        opacity: 1, fillOpacity: 0.87
      })
      .bindPopup(buildPopup(row), { maxWidth: 380, maxHeight: 420 })
      .addTo(layerGroups[type]);

      bounds.push([lat, lon]);
      plotted++;
    });

    if (bounds.length) map.fitBounds(bounds, { padding: [25, 25] });
    buildLayerPanel();

    var msg = plotted + ' samples plotted';
    if (skipped) msg += ' (' + skipped + ' skipped — no coordinates)';
    msg += '. Click any point for full data.';
    setStatus(msg, false);
  }

  /* ── Toggle panel ── */
  var TYPE_ORDER = ['Brine','Marginal Brine','Stream','River','Spring',
                    'Thermal Spring','Geothermal','Lake','Underground','Seep','Rain'];

  function buildLayerPanel() {
    var grid = document.getElementById('layer-grid');
    grid.innerHTML = '';
    var types = Object.keys(layerGroups).slice().sort(function(a,b){
      var ia=TYPE_ORDER.indexOf(a), ib=TYPE_ORDER.indexOf(b);
      if(ia===-1) ia=999; if(ib===-1) ib=999;
      return ia!==ib ? ia-ib : a.localeCompare(b);
    });
    types.forEach(function(type){ grid.appendChild(makeToggleItem(type)); });
  }

  function makeToggleItem(type) {
    var color  = typeColor(type);
    var count  = layerGroups[type].getLayers().length;
    var safeId = 'chk-' + type.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9-]/g,'');

    var item = document.createElement('div');
    item.className = 'layer-item';
    item.id = 'item-' + safeId;

    var chk = document.createElement('input');
    chk.type = 'checkbox'; chk.id = safeId; chk.checked = true;

    chk.addEventListener('change', (function(t, el) {
      return function() {
        if (this.checked) {
          layerGroups[t].addTo(map);
          layerVisible[t] = true;
          el.classList.remove('hidden');
        } else {
          if (map.hasLayer(layerGroups[t])) map.removeLayer(layerGroups[t]);
          layerVisible[t] = false;
          el.classList.add('hidden');
        }
      };
    })(type, item));

    var dot = document.createElement('div');
    dot.className = 'layer-dot'; dot.style.background = color;

    var lbl = document.createElement('label');
    lbl.htmlFor = safeId;
    lbl.textContent = type + ' (' + count + ')';

    item.appendChild(chk); item.appendChild(dot); item.appendChild(lbl);
    return item;
  }

})();
</script>
