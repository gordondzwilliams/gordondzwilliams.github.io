---
layout: default
title: "Lithium Triangle Brine and Water Dataset"
permalink: /LTdataset/
---

<p>Lithium Triangle Brine and Water Dataset. Information on data compilation is available in the README tab of the Excel sheet.
&nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.xlsx">[Download Excel]</a>
&nbsp;<a href="/files/data/LT/Supplement_LiTriangleDataset.csv">[Download CSV]</a></p>

<!-- ═══════════════════════════════════════════════════════════
     LEAFLET INTERACTIVE MAP
     Dependencies loaded from CDN — no install required
     ═══════════════════════════════════════════════════════════ -->

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

<style>
  #lt-map {
    height: 580px;
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin: 1em 0 0.5em 0;
    background: #d4e6f1;
  }
  #map-legend {
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px 14px;
    margin-bottom: 0.5em;
    display: flex;
    flex-wrap: wrap;
    gap: 5px 16px;
    font-size: 0.84em;
    color: #333;
  }
  #map-legend h4 {
    width: 100%;
    margin: 0 0 5px 0;
    font-size: 0.88em;
    font-weight: bold;
  }
  .legend-item { display: flex; align-items: center; gap: 6px; }
  .legend-dot { width: 12px; height: 12px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.25); flex-shrink: 0; }
  .legend-salar-box { width: 18px; height: 10px; background: rgba(100,160,220,0.35); border: 1.5px solid rgba(60,100,160,0.7); flex-shrink: 0; }
  #map-status { font-size: 0.82em; color: #888; margin-bottom: 1.5em; }

  /* Popup */
  .lt-popup { max-height: 320px; overflow-y: auto; min-width: 220px; max-width: 340px; font-size: 0.82em; }
  .lt-popup h3 { margin: 0 0 7px 0; font-size: 1em; border-bottom: 1px solid #e0e0e0; padding-bottom: 4px; }
  .lt-popup table { width: 100%; border-collapse: collapse; }
  .lt-popup tr:nth-child(even) { background: #f6f6f6; }
  .lt-popup td { padding: 2px 5px; vertical-align: top; }
  .lt-popup td:first-child { font-weight: bold; color: #555; white-space: nowrap; padding-right: 8px; min-width: 80px; }
  .lt-popup .na-val { color: #ccc; font-style: italic; }
</style>

<div id="lt-map"></div>
<div id="map-legend"><h4>Loading…</h4></div>
<div id="map-status">Loading sample data…</div>

<script>
(function () {

  /* ── Colorblind-friendlier type palette ── */
  var PALETTE = [
    '#e63946','#2a9d8f','#f4a261','#457b9d','#8338ec',
    '#06d6a0','#fb8500','#e76f51','#118ab2','#6d6875',
    '#588157','#d62828'
  ];
  var colorMap = {}, ci = 0;

  function typeColor(t) {
    var k = (t || 'Unknown').trim();
    if (!colorMap[k]) { colorMap[k] = PALETTE[ci % PALETTE.length]; ci++; }
    return colorMap[k];
  }

  function circleMarker(ll, type) {
    return L.circleMarker(ll, {
      radius: 7,
      fillColor: typeColor(type),
      color: '#fff',
      weight: 1.2,
      opacity: 1,
      fillOpacity: 0.88
    });
  }

  /* ── HTML escaping ── */
  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  /* ── Build popup from row object ── */
  var SKIP = ['lat','latitude','long','longitude','lon','x','y'];

  function popup(row) {
    var name = row['Sample ID']||row['Sample_ID']||row['SampleID']||row['Name']||row['Station']||row['Site']||'';
    var type = row['Type']||row['TYPE']||'';
    var title = name || type || 'Sample';
    var html = '<div class="lt-popup"><h3>' + esc(title) + '</h3><table>';
    for (var c in row) {
      if (SKIP.indexOf(c.toLowerCase()) !== -1) continue;
      var v = row[c];
      var empty = (v===null||v===undefined||v===''||v==='NA'||v==='N/A'||v==='nd'||v==='ND');
      html += '<tr><td>' + esc(c) + '</td>';
      html += empty ? '<td class="na-val">—</td>' : '<td>' + esc(String(v)) + '</td>';
      html += '</tr>';
    }
    html += '</table></div>';
    return html;
  }

  /* ── Column finder (case-insensitive) ── */
  function findCol(headers, candidates) {
    for (var i=0;i<candidates.length;i++)
      for (var j=0;j<headers.length;j++)
        if (headers[j].trim().toLowerCase()===candidates[i].toLowerCase()) return headers[j];
    return null;
  }

  /* ── Init map ── */
  var map = L.map('lt-map', { center: [-23, -67], zoom: 6 });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd', maxZoom: 19
  }).addTo(map);

  /* ── Salar polygon layer ──────────────────────────────────────────────────
     TO ACTIVATE:
     1. Convert USGS .gdb to GeoJSON (see instructions below the map).
     2. Upload the file to: /files/data/LT/salars.geojson
     3. Remove the /* and the closing asterisk-slash to uncomment this block.
     ──────────────────────────────────────────────────────────────────────── */
  /*
  fetch('/files/data/LT/salars.geojson')
    .then(r => r.json())
    .then(geojson => {
      L.geoJSON(geojson, {
        style: {
          color: 'rgba(50,90,150,0.75)',
          weight: 1.5,
          fillColor: 'rgba(100,160,220,0.3)',
          fillOpacity: 0.35
        },
        onEachFeature: function(f, layer) {
          var n = f.properties && (f.properties.Salar_Name || f.properties.NAME || f.properties.name || 'Salar');
          if (n) layer.bindTooltip(n, {sticky:true});
        }
      }).addTo(map);
    })
    .catch(e => console.warn('salars.geojson not found:', e));
  */

  /* ── Load CSV ── */
  Papa.parse('/files/data/LT/Supplement_LiTriangleDataset.csv', {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: function(res) {
      var data = res.data;
      if (!data.length) { document.getElementById('map-status').textContent='No data in CSV.'; return; }

      var headers = Object.keys(data[0]);
      var latCol = findCol(headers, ['Lat','Latitude','LAT','LATITUDE']);
      var lonCol = findCol(headers, ['Long','Longitude','LON','LONG','LONGITUDE','Lon']);
      var typeCol = findCol(headers, ['Type','TYPE','type','Sample Type','SampleType']);

      if (!latCol || !lonCol) {
        document.getElementById('map-status').textContent =
          'ERROR: Could not detect Lat/Lon columns. Columns found: ' + headers.join(', ');
        return;
      }

      var plotted=0, skipped=0, bounds=[];
      data.forEach(function(row) {
        var lat=parseFloat(row[latCol]), lon=parseFloat(row[lonCol]);
        if (isNaN(lat)||isNaN(lon)) { skipped++; return; }
        var type = typeCol ? (row[typeCol]||'Unknown') : 'Unknown';
        circleMarker([lat,lon], type)
          .bindPopup(popup(row), {maxWidth:360, maxHeight:400})
          .addTo(map);
        bounds.push([lat,lon]);
        plotted++;
      });

      if (bounds.length) map.fitBounds(bounds, {padding:[30,30]});

      /* Legend */
      var leg = document.getElementById('map-legend');
      var html = '<h4>Sample Type</h4>';
      for (var t in colorMap) {
        html += '<div class="legend-item"><div class="legend-dot" style="background:'+colorMap[t]+'"></div><span>'+esc(t)+'</span></div>';
      }
      /* Uncomment when salar layer is active:
      html += '<div class="legend-item"><div class="legend-salar-box"></div><span>Salar outline (USGS)</span></div>';
      */
      leg.innerHTML = html;

      document.getElementById('map-status').textContent =
        plotted + ' samples plotted' + (skipped ? ' (' + skipped + ' skipped — no coordinates)' : '') + '. Click any point for full data.';
    },
    error: function(e) {
      document.getElementById('map-status').textContent = 'CSV load error: ' + (e.message||e);
    }
  });

})();
</script>
