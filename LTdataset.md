---
layout: single
title: "Lithium Triangle Brine and Water Dataset"
permalink: /LTdataset/
author_profile: false
---

<style>
/* Add spacing so content isn’t flush with screen edges */
.page-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 22px;               /* larger padding so text breathes */
  box-sizing: border-box;
  background: #f6f7f9;         /* pale grey background */
  border: 1px solid #e6e8eb;   /* subtle border */
  border-radius: 8px;          /* soft corners */
}

/* Optional: nicer typography spacing for headings & paragraphs */
.page-content h1,
.page-content h2,
.page-content h3 {
  margin-top: 1.25rem;
  margin-bottom: 0.6rem;
}

/* Simple, theme-friendly project grid */
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin: 1.5rem 0;
}
.project-card {
  display: block;
  background: #fff;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,.08);
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: transform .08s ease, box-shadow .2s ease;
}
.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,.12);
}
.project-card__img {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
  background: #f4f4f4;
}
.project-card__body {
  padding: .85rem 1rem 1rem;
}
.project-card__title {
  margin: 0 0 .25rem;
  font-size: 1.05rem;
  font-weight: 700;
}
.project-card__desc {
  margin: 0;
  color: #444;
  font-size: .95rem;
  line-height: 1.35;
}

/* Make sure long code/links wrap inside the container */
.page-content p, .page-content a {
  word-break: break-word;
}

  #lt-map {
    height: 580px; width: 100%;
    border: 1px solid #ccc; border-radius: 4px;
    margin: 1em 0 0 0; background: #d4e6f1;
  }
  #layer-panel {
    background: #fff;
    border: 1px solid #ccc; border-radius: 4px;
    padding: 10px 14px; margin: 6px 0 4px 0;
    font-size: 0.84em; color: #333;
  }
  #layer-panel h4 {
    margin: 0 0 8px 0; font-size: 0.9em;
    font-weight: bold; display: flex;
    align-items: center; gap: 10px;
  }
  #layer-panel h4 span { font-weight: normal; color: #888; font-size: 0.88em; }
  .layer-grid { display: flex; flex-wrap: wrap; gap: 5px 14px; }
  .layer-item {
    display: flex; align-items: center; gap: 7px;
    cursor: pointer; user-select: none;
    padding: 3px 6px; border-radius: 3px;
    transition: background 0.15s;
  }
  .layer-item:hover { background: #f5f5f5; }
  .layer-item input[type=checkbox] { cursor: pointer; margin: 0; }
  .layer-dot {
    width: 13px; height: 13px; border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.2); flex-shrink: 0;
    transition: opacity 0.2s;
  }
  .layer-item.hidden .layer-dot { opacity: 0.25; }
  .layer-item.hidden label { color: #bbb; }
  label { cursor: pointer; }
  .salar-box {
    width: 18px; height: 10px; border-radius: 2px;
    background: rgba(100,160,220,0.3);
    border: 1.5px solid rgba(50,90,160,0.7); flex-shrink: 0;
  }
  #map-status { font-size: 0.8em; color: #999; margin: 2px 0 1.2em 0; }
  .lt-popup {
    max-height: 340px; overflow-y: auto;
    min-width: 230px; max-width: 360px; font-size: 0.81em;
  }
  .lt-popup h3 {
    margin: 0 0 7px 0; font-size: 1em;
    border-bottom: 1px solid #e5e5e5; padding-bottom: 4px;
  }
  .lt-popup table { width: 100%; border-collapse: collapse; }
  .lt-popup tr:nth-child(even) { background: #f7f7f7; }
  .lt-popup td { padding: 2px 5px; vertical-align: top; }
  .lt-popup td:first-child {
    font-weight: bold; color: #555;
    white-space: nowrap; padding-right: 8px; min-width: 85px;
  }
  .lt-popup .na { color: #ccc; font-style: italic; }
</style>

<p>
Lithium Triangle Brine and Water Dataset. Information on data compilation is available in the README.
&nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.xlsx">[Download Excel]</a>
&nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.csv">[Download CSV]</a>
&nbsp;<a href="/files/data/LT/LiTriangleDataset_README.md">[Download README]</a>
</p>

<!-- ═══════════════════════════════════════════ LEAFLET MAP ═══ -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

<div id="lt-map"></div>
<div id="layer-panel">
  <h4>Toggle Sample Types <span>— click checkbox to show/hide a layer</span></h4>
  <div class="layer-grid" id="layer-grid">Loading…</div>
</div>
<div id="map-status">Loading data…</div>

<script>
(function () {

  var PALETTE = {
    'Brine':          '#e63946',
    'Marginal Brine': '#c1121f',
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
    var html = '<div class="lt-popup"><h3>' + esc(name || type || 'Sample') + '</h3><table>';
    for (var c in row) {
      if (SKIP_COLS.indexOf(c.toLowerCase()) !== -1) continue;
      var v = row[c];
      var empty = (v===null||v===undefined||v===''||
                   String(v).toLowerCase()==='na'||
                   String(v).toLowerCase()==='nd');
      html += '<tr><td>' + esc(c) + '</td>';
      html += empty ? '<td class="na">—</td>' : '<td>' + esc(String(v)) + '</td>';
      html += '</tr>';
    }
    html += '</table></div>';
    return html;
  }

  function findCol(headers, candidates) {
    for (var i=0;i<candidates.length;i++)
      for (var j=0;j<headers.length;j++)
        if (headers[j] && headers[j].trim().toLowerCase()===candidates[i].toLowerCase())
          return headers[j];
    return null;
  }

  var map = L.map('lt-map', { center: [-23, -67], zoom: 6 });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd', maxZoom: 19
  }).addTo(map);

  var layerGroups = {};
  var layerVisible = {};

  /* ── Salar polygon layer ─────────────────────────────────────────────────
     TO ACTIVATE after converting USGS .gdb to GeoJSON (see ArcGIS Pro
     instructions at the bottom of this page):
       1. Upload salars.geojson to /files/data/LT/salars.geojson in your repo
       2. Delete the slash-asterisk comment markers below (lines starting with
          slash-asterisk and ending with asterisk-slash)
  ─────────────────────────────────────────────────────────────────────── */
  /*
  var salarGroup = L.layerGroup().addTo(map);
  fetch('/files/data/LT/salars.geojson')
    .then(function(r){ return r.json(); })
    .then(function(gj){
      L.geoJSON(gj, {
        style: {
          color:'rgba(50,90,160,0.75)', weight:1.5,
          fillColor:'rgba(100,160,220,0.28)', fillOpacity:0.35
        },
        onEachFeature: function(f, layer){
          var n = f.properties &&
            (f.properties.Salar_Name||f.properties.NAME||f.properties.name||'Salar');
          if(n) layer.bindTooltip(n,{sticky:true});
        }
      }).addTo(salarGroup);
      addSalarToggle(salarGroup);
    })
    .catch(function(e){ console.warn('salars.geojson not yet uploaded:',e); });
  */

  Papa.parse('/files/data/LT/Supplement_LiTriangleDataset.csv', {
    download: true, header: true, skipEmptyLines: true,
    complete: function(res) {
      var data = res.data;
      if (!data.length) {
        document.getElementById('map-status').textContent = 'No data in CSV.';
        return;
      }
      var headers = Object.keys(data[0]);
      var latCol  = findCol(headers, ['Lat','Latitude','LAT','LATITUDE']);
      var lonCol  = findCol(headers, ['Long','Longitude','LON','LONG','LONGITUDE','Lon']);
      var typeCol = findCol(headers, ['Type','TYPE','type','Sample Type']);

      if (!latCol || !lonCol) {
        document.getElementById('map-status').textContent =
          'ERROR: Could not find Lat/Lon columns. Found: ' + headers.join(', ');
        return;
      }

      var plotted=0, skipped=0, bounds=[];
      data.forEach(function(row) {
        var lat=parseFloat(row[latCol]), lon=parseFloat(row[lonCol]);
        if (isNaN(lat)||isNaN(lon)) { skipped++; return; }
        var type = typeCol ? (row[typeCol]||'Unknown').trim() : 'Unknown';

        if (!layerGroups[type]) {
          layerGroups[type] = L.layerGroup().addTo(map);
          layerVisible[type] = true;
        }
        L.circleMarker([lat,lon], {
          radius:6, fillColor:typeColor(type), color:'#fff',
          weight:1.2, opacity:1, fillOpacity:0.87
        })
        .bindPopup(buildPopup(row), {maxWidth:380, maxHeight:400})
        .addTo(layerGroups[type]);

        bounds.push([lat,lon]);
        plotted++;
      });

      if (bounds.length) map.fitBounds(bounds, {padding:[25,25]});
      buildLayerPanel();

      var msg = plotted + ' samples plotted';
      if (skipped) msg += ' (' + skipped + ' skipped — no coordinates)';
      msg += '. Click any point for full data.';
      document.getElementById('map-status').textContent = msg;
    },
    error: function(e) {
      document.getElementById('map-status').textContent = 'CSV error: ' + (e.message||e);
    }
  });

  var TYPE_ORDER = ['Brine','Marginal Brine','Stream','River','Spring',
                    'Thermal Spring','Geothermal','Lake','Underground','Seep','Rain'];

  function buildLayerPanel() {
    var grid = document.getElementById('layer-grid');
    grid.innerHTML = '';
    var types = Object.keys(layerGroups);
    types.sort(function(a,b){
      var ia=TYPE_ORDER.indexOf(a), ib=TYPE_ORDER.indexOf(b);
      if(ia===-1) ia=999; if(ib===-1) ib=999;
      return ia!==ib ? ia-ib : a.localeCompare(b);
    });
    types.forEach(function(type){ grid.appendChild(makeToggleItem(type)); });
  }

  function makeToggleItem(type) {
    var color = typeColor(type);
    var id = 'chk-' + type.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9-]/g,'');
    var count = layerGroups[type].getLayers().length;
    var item = document.createElement('div');
    item.className = 'layer-item';
    item.id = 'item-' + id;
    var chk = document.createElement('input');
    chk.type='checkbox'; chk.id=id; chk.checked=true;
    chk.addEventListener('change', (function(t, el){
      return function(){
        if(this.checked){ layerGroups[t].addTo(map); el.classList.remove('hidden'); }
        else { map.removeLayer(layerGroups[t]); el.classList.add('hidden'); }
      };
    })(type, item));
    var dot = document.createElement('div');
    dot.className='layer-dot'; dot.style.background=color;
    var lbl = document.createElement('label');
    lbl.htmlFor=id; lbl.textContent=type+' ('+count+')';
    item.appendChild(chk); item.appendChild(dot); item.appendChild(lbl);
    return item;
  }

  function addSalarToggle(sLayer) {
    var grid = document.getElementById('layer-grid');
    var item = document.createElement('div');
    item.className='layer-item';
    item.style.cssText='border-left:2px solid #ccc;padding-left:10px;margin-left:4px;';
    var chk=document.createElement('input');
    chk.type='checkbox'; chk.checked=true; chk.id='chk-salars';
    chk.addEventListener('change',function(){
      if(this.checked) sLayer.addTo(map); else map.removeLayer(sLayer);
    });
    var box=document.createElement('div'); box.className='salar-box';
    var lbl=document.createElement('label');
    lbl.htmlFor='chk-salars'; lbl.textContent='Salar outlines (USGS)';
    item.appendChild(chk); item.appendChild(box); item.appendChild(lbl);
    grid.appendChild(item);
  }

})();
</script>
