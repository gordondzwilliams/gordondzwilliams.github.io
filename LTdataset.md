---
layout: single
title: 
permalink: /LTdataset/
author_profile: false
---

<style>
.page__content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
  background: #f6f7f9;
  border: 1px solid #e6e8eb;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

#layer-panel,
#layer-panel .layer-item,
#layer-panel .layer-item label {
  color: #000 !important;
}

#lt-map {
  height: 580px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-top: 1rem;
  background: #d4e6f1;
}

#layer-panel {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px 14px;
  margin: 6px 0 4px 0;
  font-size: 0.84em;
}

#layer-panel h4 {
  margin: 0 0 8px 0;
  font-size: 0.9em;
  font-weight: bold;
  color: #000;
}

.layer-grid { display: flex; flex-wrap: wrap; gap: 5px 14px; }

.layer-item {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 3px 6px;
  border-radius: 3px;
}

.layer-dot {
  width: 13px;
  height: 13px;
  border-radius: 50%;
  border: 1px solid rgba(0,0,0,0.2);
}

#map-status { font-size: 0.8em; color: #999; margin: 2px 0 1.2em 0; }

/* Popup */
.lt-popup {
  max-height: 320px;
  overflow-y: auto;
  min-width: 220px;
  max-width: 340px;
  font-size: 0.82em;
}
.lt-popup h3 {
  margin: 0 0 7px 0;
  font-size: 1em;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 4px;
  color: #111;
}
.lt-popup table { width: 100%; border-collapse: collapse; }
.lt-popup tr:nth-child(even) { background: #f5f5f5; }
.lt-popup td { padding: 2px 5px; vertical-align: top; color: #111; }
.lt-popup td:first-child {
  font-weight: bold;
  color: #444;
  white-space: nowrap;
  padding-right: 8px;
  min-width: 80px;
}
.lt-popup .na { color: #ccc; font-style: italic; }
</style>

<div class="page__content">
  <h1>Lithium Triangle Brine and Water Dataset</h1>

  <p>
    Lithium Triangle Brine and Water Dataset. Information on data compilation is available in the README.
    &nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.xlsx">[Download Excel]</a>
    &nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.csv">[Download CSV]</a>
    &nbsp;<a href="/files/data/LT/LiTriangleDataset_README.md">[Download README]</a>
  </p>

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

  <div id="lt-map"></div>

  <div id="layer-panel">
    <h4>Toggle Sample Types</h4>
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

  function findCol(headers, candidates) {
    for (var i=0;i<candidates.length;i++)
      for (var j=0;j<headers.length;j++)
        if (headers[j] && headers[j].trim().toLowerCase()===candidates[i].toLowerCase())
          return headers[j];
    return null;
  }

  var SKIP = ['lat','latitude','long','longitude','lon','x','y'];

  function buildPopup(row) {
    var name = row['Sample ID'] || row['Name'] || row['Station'] || '';
    var type = row['Type'] || '';
    var html = '<div class="lt-popup"><h3>' + esc(name || type || 'Sample') + '</h3><table>';
    for (var c in row) {
      if (SKIP.indexOf(c.toLowerCase()) !== -1) continue;
      var v = row[c];
      var empty = (v === null || v === undefined || v === '' ||
                   String(v).toLowerCase() === 'na' ||
                   String(v).toLowerCase() === 'nd');
      html += '<tr><td>' + esc(c) + '</td>';
      html += empty ? '<td class="na">—</td>' : '<td>' + esc(String(v)) + '</td>';
      html += '</tr>';
    }
    html += '</table></div>';
    return html;
  }

  var map = L.map('lt-map', { center: [-23, -67], zoom: 6 });

  L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    { attribution: 'Tiles &copy; Esri — Esri, Maxar, Earthstar Geographics', maxZoom: 19 }
  ).addTo(map);

  L.tileLayer(
    'https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    { attribution: 'Esri', pane: 'overlayPane' }
  ).addTo(map);

  var layerGroups = {};

  Papa.parse('/files/data/LT/Supplement_LiTriangleDataset.csv', {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: function(res) {
      var data    = res.data;
      var headers = Object.keys(data[0]);
      var latCol  = findCol(headers, ['Lat','Latitude']);
      var lonCol  = findCol(headers, ['Long','Longitude']);
      var typeCol = findCol(headers, ['Type','Sample Type']);
      var bounds  = [];

      data.forEach(function(row) {
        var lat = parseFloat(row[latCol]);
        var lon = parseFloat(row[lonCol]);
        if (isNaN(lat) || isNaN(lon)) return;

        var type = typeCol ? (row[typeCol] || 'Unknown').trim() : 'Unknown';
        if (!layerGroups[type]) {
          layerGroups[type] = L.layerGroup().addTo(map);
        }

        L.circleMarker([lat, lon], {
          radius: 6,
          fillColor: typeColor(type),
          color: '#fff',
          weight: 1.2,
          fillOpacity: 0.87
        })
        .bindPopup(buildPopup(row), { maxWidth: 360, maxHeight: 400 })
        .addTo(layerGroups[type]);

        bounds.push([lat, lon]);
      });

      if (bounds.length) map.fitBounds(bounds, { padding: [25, 25] });
      buildLayerPanel();

      document.getElementById('map-status').textContent =
        Object.keys(layerGroups).length + ' sample types loaded. Click any point for full data.';
    }
  });

  var TYPE_ORDER = ['Brine','Marginal Brine','Stream','River','Spring',
                    'Thermal Spring','Geothermal','Lake','Underground','Seep','Rain'];

  function buildLayerPanel() {
    var grid = document.getElementById('layer-grid');
    grid.innerHTML = '';
    var types = Object.keys(layerGroups).sort(function(a,b) {
      var ia = TYPE_ORDER.indexOf(a), ib = TYPE_ORDER.indexOf(b);
      if (ia === -1) ia = 999;
      if (ib === -1) ib = 999;
      return ia !== ib ? ia - ib : a.localeCompare(b);
    });
    types.forEach(function(type) { grid.appendChild(makeToggleItem(type)); });
  }

  function makeToggleItem(type) {
    var id    = 'chk-' + type.replace(/[^a-zA-Z0-9]/g, '-');
    var count = layerGroups[type].getLayers().length;
    var item  = document.createElement('div');
    item.className = 'layer-item';

    var chk = document.createElement('input');
    chk.type = 'checkbox'; chk.id = id; chk.checked = true;
    chk.addEventListener('change', function() {
      if (this.checked) layerGroups[type].addTo(map);
      else              map.removeLayer(layerGroups[type]);
    });

    var dot = document.createElement('div');
    dot.className = 'layer-dot';
    dot.style.background = typeColor(type);

    var lbl = document.createElement('label');
    lbl.htmlFor = id;
    lbl.textContent = type + ' (' + count + ')';

    item.appendChild(chk);
    item.appendChild(dot);
    item.appendChild(lbl);
    return item;
  }

})();
</script>

  <p>Of the selectable sample types, most brines and some lakes are considered terminal to a closed basin. See the dataset to distinguish between inflows and terminal samples.</p>

</div>
