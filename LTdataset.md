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
    height: 560px; width: 100%;
    border: 1px solid #ccc; border-radius: 4px;
    margin: 1em 0 0 0; background: #b8cfe0;
  }
  #map-controls {
    background: #f9f9f9; border: 1px solid #ccc; border-radius: 4px;
    padding: 9px 14px; margin: 6px 0 4px 0;
    font-size: 0.84em; color: #111;
    display: flex; flex-wrap: wrap; gap: 8px 0; align-items: flex-start;
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
  .bm-btn.active  { background: #333; color: #fff; border-color: #333; }
  .bm-btn:not(.active):hover { background: #eee; }
  #layer-section { flex: 1; min-width: 0; }
  #layer-section strong { color: #111; display: block; margin-bottom: 5px; }
  .layer-grid { display: flex; flex-wrap: wrap; gap: 4px 12px; }
  .layer-item {
    display: flex; align-items: center; gap: 6px;
    padding: 3px 7px; border-radius: 3px; cursor: pointer;
    user-select: none; transition: background 0.15s;
  }
  .layer-item:hover { background: #efefef; }
  .layer-item.off { opacity: 0.4; }
  .layer-item.off:hover { opacity: 0.65; }
  .layer-item input[type=checkbox] { cursor: pointer; margin: 0; }
  .layer-dot {
    width: 12px; height: 12px; border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.25); flex-shrink: 0;
  }
  .layer-item label { cursor: pointer; color: #111; white-space: nowrap; }
  #map-status { font-size: 0.79em; color: #777; margin: 3px 0 1.5em 0; }
  #map-status.err { color: #b00; font-weight: bold; }
  .lt-popup { max-height: 340px; overflow-y: auto; min-width: 230px; max-width: 360px; font-size: 0.81em; }
  .lt-popup h3 { margin: 0 0 6px 0; font-size: 1em; border-bottom: 1px solid #e0e0e0; padding-bottom: 4px; color: #111; }
  .lt-popup table { width: 100%; border-collapse: collapse; }
  .lt-popup tr:nth-child(even) { background: #f6f6f6; }
  .lt-popup td { padding: 2px 5px; vertical-align: top; color: #111; }
  .lt-popup td:first-child { font-weight: bold; color: #444; white-space: nowrap; padding-right: 8px; min-width: 85px; }
  .lt-popup .na { color: #bbb; font-style: italic; }
</style>

<div id="lt-map"></div>
<div id="map-controls">
  <div id="basemap-switcher">
    <strong>Basemap:</strong>
    <span class="bm-btn active" id="btn-satellite" onclick="ltMap.switchBasemap('satellite')">Satellite</span>
    <span class="bm-btn"        id="btn-light"     onclick="ltMap.switchBasemap('light')">Street Map</span>
  </div>
  <div id="layer-section">
    <strong>Toggle Sample Types:</strong>
    <div class="layer-grid" id="layer-grid">Loading…</div>
  </div>
</div>
<div id="map-status">Loading data…</div>

<script>
var ltMap = (function () {

  /* ── helpers ─────────────────────────────────────────────── */
  var statusEl = document.getElementById('map-status');
  function setStatus(msg, isErr) {
    statusEl.textContent = msg;
    statusEl.className   = isErr ? 'err' : '';
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  var SKIP = ['lat','latitude','long','longitude','lon','x','y'];
  function buildPopup(row) {
    var name = row['Sample ID']||row['Name']||row['Station']||'';
    var type = row['Type']||'';
    var html = '<div class="lt-popup"><h3>'+esc(name||type||'Sample')+'</h3><table>';
    for (var c in row) {
      if (SKIP.indexOf(c.toLowerCase()) !== -1) continue;
      var v = row[c], empty = (!v || String(v).toLowerCase()==='na' || String(v).toLowerCase()==='nd');
      html += '<tr><td>'+esc(c)+'</td>'+(empty?'<td class="na">—</td>':'<td>'+esc(String(v))+'</td>')+'</tr>';
    }
    return html+'</table></div>';
  }

  function findCol(headers, cands) {
    for (var i=0;i<cands.length;i++)
      for (var j=0;j<headers.length;j++)
        if (headers[j] && headers[j].trim().toLowerCase()===cands[i].toLowerCase()) return headers[j];
    return null;
  }

  /* ── colors ──────────────────────────────────────────────── */
  var PALETTE = {
    'Brine':'#e63946','Marginal Brine':'#ff6b6b',
    'Stream':'#2a9d8f','River':'#48cae4','Spring':'#52b788',
    'Thermal Spring':'#f4a261','Geothermal':'#fb8500',
    'Lake':'#457b9d','Underground':'#8338ec',
    'Seep':'#6d6875','Rain':'#80b918'
  };
  function col(t){ return PALETTE[(t||'').trim()]||'#888888'; }

  /* ── map + basemaps ──────────────────────────────────────── */
  var tiles = {
    satellite: L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      { attribution:'Tiles &copy; Esri', maxZoom:19 }
    ),
    light: L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
      { attribution:'&copy; OpenStreetMap &copy; CARTO', subdomains:'abcd', maxZoom:19 }
    )
  };
  var curBase = 'satellite';
  var map = L.map('lt-map', { center:[-23,-67], zoom:6 });
  tiles.satellite.addTo(map);

  var groups  = {};   // type → LayerGroup
  var visible = {};   // type → bool

  /* ── basemap switch ──────────────────────────────────────── */
  function switchBasemap(name) {
    if (name === curBase) return;
    map.removeLayer(tiles[curBase]);
    tiles[name].addTo(map);
    /* re-add sample layers on top */
    for (var t in groups) { if (visible[t]) { map.removeLayer(groups[t]); groups[t].addTo(map); } }
    curBase = name;
    document.getElementById('btn-satellite').classList.toggle('active', name==='satellite');
    document.getElementById('btn-light').classList.toggle('active', name==='light');
  }

  /* ── load CSV with native fetch ──────────────────────────── */
  var CSV_URL = 'https://gordondzwilliams.github.io/files/data/LT/Supplement_LiTriangleDataset.csv';

  fetch(CSV_URL)
    .then(function(resp) {
      if (!resp.ok) throw new Error('HTTP ' + resp.status + ' fetching ' + CSV_URL);
      return resp.text();
    })
    .then(function(text) {
      var result = Papa.parse(text, { header:true, skipEmptyLines:true });
      if (!result.data || !result.data.length) throw new Error('CSV parsed but contains no rows.');
      processData(result.data);
    })
    .catch(function(err) {
      setStatus('ERROR loading data: ' + err.message, true);
    });

  /* ── process rows ────────────────────────────────────────── */
  var TYPE_ORDER = ['Brine','Marginal Brine','Stream','River','Spring',
                    'Thermal Spring','Geothermal','Lake','Underground','Seep','Rain'];

  function processData(data) {
    var headers = Object.keys(data[0]);
    var latCol  = findCol(headers, ['Lat','Latitude','LAT','LATITUDE']);
    var lonCol  = findCol(headers, ['Long','Longitude','LON','LONG','LONGITUDE','Lon']);
    var typeCol = findCol(headers, ['Type','TYPE','type','Sample Type']);

    if (!latCol || !lonCol) {
      setStatus('ERROR: No Lat/Lon columns found. Columns: ' + headers.join(', '), true);
      return;
    }

    var plotted=0, skipped=0, bounds=[];
    data.forEach(function(row) {
      var lat=parseFloat(row[latCol]), lon=parseFloat(row[lonCol]);
      if (isNaN(lat)||isNaN(lon)) { skipped++; return; }
      var type = typeCol ? (row[typeCol]||'Unknown').trim() : 'Unknown';
      if (!groups[type]) { groups[type]=L.layerGroup().addTo(map); visible[type]=true; }
      L.circleMarker([lat,lon], {
        radius:6, fillColor:col(type), color:'#fff', weight:1.2, opacity:1, fillOpacity:0.87
      }).bindPopup(buildPopup(row), {maxWidth:380,maxHeight:420}).addTo(groups[type]);
      bounds.push([lat,lon]);
      plotted++;
    });

    if (bounds.length) map.fitBounds(bounds, {padding:[25,25]});
    buildPanel();
    var msg = plotted+' samples plotted'+(skipped?' ('+skipped+' skipped — no coordinates)':'')
              +'. Click any point for full data.';
    setStatus(msg, false);
  }

  /* ── toggle panel ────────────────────────────────────────── */
  function buildPanel() {
    var grid = document.getElementById('layer-grid');
    grid.innerHTML = '';
    var types = Object.keys(groups).sort(function(a,b){
      var ia=TYPE_ORDER.indexOf(a)||999, ib=TYPE_ORDER.indexOf(b)||999;
      return ia!==ib ? ia-ib : a.localeCompare(b);
    });
    types.forEach(function(type) {
      var id    = 'lyr-'+type.replace(/[^a-zA-Z0-9]/g,'-');
      var count = groups[type].getLayers().length;
      var item  = document.createElement('div');
      item.className = 'layer-item';

      var chk = document.createElement('input');
      chk.type='checkbox'; chk.id=id; chk.checked=true;
      chk.addEventListener('change', (function(t,el){
        return function(){
          if (this.checked) { groups[t].addTo(map); visible[t]=true;  el.classList.remove('off'); }
          else              { map.removeLayer(groups[t]); visible[t]=false; el.classList.add('off'); }
        };
      })(type, item));

      var dot = document.createElement('div');
      dot.className='layer-dot'; dot.style.background=col(type);

      var lbl = document.createElement('label');
      lbl.htmlFor=id; lbl.textContent=type+' ('+count+')';

      item.appendChild(chk); item.appendChild(dot); item.appendChild(lbl);
      grid.appendChild(item);
    });
  }

  return { switchBasemap: switchBasemap };
})();
</script>
