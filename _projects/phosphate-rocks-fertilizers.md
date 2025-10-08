---
layout: default
title:  Phosphate Rocks and Fertilizers
excerpt: Phosphate Rocks and Fertilizers
image: /images/phos/GHfertilizer.jpg
order: 11
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
  <h1>Phosphate Rocks and Fertilizers</h1>
<p>
Phosphorous is among the most important elements for modern agriculture, and phosphate rocks are the primary source of phosphorous for fertilizers. Phosphate rock deposits are found throughout the world, having formed through sedimentary and magmatic processes.  
</p>
<p>
I collaborate on a variety of projects related to:  
</p>
<p>
1. Understanding the depositional environments of phosphorites and their enrichment in elements other than phosphorous**, including redox-sensitive elements (like uranium or cadmium) and rare earth elements. To do this, we use uranium, strontium, and lead isotopes along with rare earth element profiles to reconstruct the environmental conditions of marine phosphorite deposit formation [\[1\]](https://doi.org/10.1016/j.chemgeo.2023.121715), [\[2\]](https://doi.org/10.1016/j.chemgeo.2024.122214).  
</p>
<p>
2. Tracing the impacts of phosphate rock mining, processing, and fertilizer use on agricultural systems.** During the processing of phosphate rocks to fertilizers, many trace elements and radionuclides naturally enriched in the rocks are transferred into fertilizer products [\[3\]](https://doi.org/10.1021/acs.estlett.4c00170), [\[4\]](https://doi.org/10.1016/j.scitotenv.2022.157971). Our field studies show that long-term fertilizer application can enrich trace elements and radionuclides in agricultural topsoils and groundwater, and that isotopic fingerprints of strontium provide powerful tracers for identifying fertilizer-derived contaminants in the environment [\[3\]](https://doi.org/10.1021/acs.estlett.4c00170), [\[5\]](https://doi.org/10.1016/j.jhazmat.2025.140033), [\[6\]](https://doi.org/10.1016/j.scitotenv.2023.167863).  
</p>

 

  <h2>Photos from the Field</h2>
  <p>click to expand</p>

  <!-- Responsive gallery: add as many <figure> blocks as you want -->
  <div class="gallery-grid">


    

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

