---
layout: default
title:  Water Quality Impacts of Hrad-Rock Lithium Mining
excerpt: Hard-Rock Lithium Deposits and Water Geochemistry
image: /images/HallmanBeam1.jpg
order: 9
---
<style>
/* Page container so content isn't flush against the window */
.page-content {
  max-width: 980px;    /* readable column width */
  margin: 0 auto;      /* center on larger screens */
  padding: 28px 20px;  /* breathing room on mobile & desktop */
  box-sizing: border-box;
}

/* Optional: nicer typography spacing for headings & paragraphs */
.page-content h1,
.page-content h2,
.page-content h3 {
  margin-top: 1.25rem;
  margin-bottom: 0.6rem;
}

/* Gallery grid: responsive 1-3 columns */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 1.25rem 0 2rem;
}

/* Figure styling */
.gallery-grid figure {
  margin: 0;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
}

.gallery-grid img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

/* Caption styling */
.gallery-grid figcaption {
  padding: 0.5rem 0.75rem;
  font-size: 0.92rem;
  color: #333;
  line-height: 1.3;
}

/* Make sure long code/links wrap inside the container */
.page-content p, .page-content a {
  word-break: break-word;
}
</style>

<div class="page-content">

  <!-- Use HTML headings inside an HTML wrapper so they render correctly -->
  <h1>Hard-Rock Lithium Deposits and Water-Quality</h1>
<p>
Hard-rock lithium deposits, known as Lithium-Cesium-Tantalum (LCT) pegmatites, are currently the most important global source of lithium. These pegmatites represent the highly fractionated endmembers of granitic magmas and are enriched in “incompatible” elements such as lithium.
</p>
<p>
In North Carolina, the Carolina Tin-Spodumene Belt (TSB) is just outside of Charlotte, NC and hosts one of the largest LCT pegmatite resources. From the 1950s through the late 1980s, the TSB was among the world’s most productive lithium mining regions. Although mining has since ceased, legacy open-pit operations remain which have since filled with water forming pit lakes.
</p>
<p>
My work investigates water quality across the TSB, with a focus on developing geochemical tracers to distinguish natural processes from mining-related impacts. Our research so far indicates that low-abundance phosphate minerals in the LCT pegmatites may play an important role in regulating water chemistry during mining. We also found that lithium, rubidium, and cesium concentrations are consistently elevated in both groundwater and surface waters throughout the TSB, reflecting both the natural and mining related influence of these pegmatites on nearby water resources. Check out our <a href="https://www.sciencedirect.com/science/article/pii/S0048969724074382" target="_blank" rel="noopener">Science of the Total Environment</a> article that discusses some of our early results.
</p>

 

  <h2>Photos from the Field</h2>
  <p>click to expand</p>

  <!-- Responsive gallery: add as many <figure> blocks as you want -->
  <div class="gallery-grid">

    <figure>
      <img src="/images/HallmanBeam1.jpg" alt="Blue glow on Salar de Uyuni">
      <figcaption>Aerial Image of the Hallman-Beam Mine & Pit Lake</figcaption>
    </figure>
    
    <figure>
      <img src="/images/TSB/KMM_Pit_High.jpg" alt="Blue glow on Salar de Uyuni">
      <figcaption>Kings Mountain Mine Pit Lake </figcaption>
    </figure>
    
    <figure>
      <img src="/images/TSB/TSB_SamplingG.jpg" alt="Blue glow on Salar de Uyuni">
      <figcaption>Water Sampling in the TSB</figcaption>
    </figure>
    
    <figure>
      <img src="/images/TSB/TSB_SamplingM.jpg" alt="Blue glow on Salar de Uyuni">
      <figcaption>Water Sampling in the TSB</figcaption>
    </figure>
        
    <figure>
      <img src="/images/TSB/KMM_PegSmithsonian.jpg" alt="Blue glow on Salar de Uyuni">
      <figcaption>Spodumene pegamtite from the TSB in the Smithsonian National Museaum of Natural History. The pegmatite is intruded into a granite.</figcaption>
    </figure>
    

  </div> <!-- /.gallery-grid -->

  <!-- Lightbox overlay element -->
  <div class="lightbox" id="lightbox">
    <img src="" alt="Full size image">
  </div>

</div> <!-- /.page-content -->

<style>
/* Lightbox overlay */
.lightbox {
  display: none;
  position: fixed;
  z-index: 9999;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.85);
  justify-content: center;
  align-items: center;
}
.lightbox img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
</style>

<script>
document.querySelectorAll('.gallery-grid img').forEach(img => {
  img.addEventListener('click', () => {
    const lightbox = document.getElementById('lightbox');
    lightbox.style.display = 'flex';
    lightbox.querySelector('img').src = img.src;
  });
});

document.getElementById('lightbox').addEventListener('click', () => {
  document.getElementById('lightbox').style.display = 'none';
});
</script>

