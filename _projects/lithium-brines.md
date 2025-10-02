---
layout: default
title: Lithium Brine Geochemistry
excerpt: Lithium Brine Geochemistry
image: /images/SDU_BlueGlow.jpg
order: 10
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
  <h1>Lithium Brine Geochemistry</h1>

  <h2>Overview</h2>
  <p>
    Lithium brines are among the most important global sources of lithium, accounting for roughly 40% of global production. These hypersaline brines (commonly ~200–300 g/kg TDS) form as the concentrated residues of inflow waters that have evaporated in closed basins. Over geologic time, they accumulate relatively high lithium concentrations (typically ~100–1000 mg/kg Li). Such deposits are typically restricted to high-altitude, arid regions, most notably the central Andes in the Lithium Triangle (spanning parts of Bolivia, Chile, and Argentina) and the Tibetan Plateau.
  </p>

  <p>
    My research focuses on the <strong>Salar de Uyuni</strong> in Bolivia, the world’s largest salt flat (~10,000 km²) and the largest known lithium brine resource. Lithium production here remains in pilot stages, with sequential evaporation ponds and a pilot lithium carbonate facility currently operating. We have sampled and analyzed natural brines, evaporation-pond brines, and process wastewaters, tracing the evolution of brine chemistry through the entire industrial sequence. From this work, we showed that evaporating brines at the Salar de Uyuni behave uniquely: as they concentrate, they become increasingly acidic and enriched in conservative elements such as arsenic and boron (see our <a href="https://doi.org/10.1021/acs.estlett.4c01124" target="_blank" rel="noopener">Environmental Science &amp; Technology Letters</a> article).
  </p>

  <p>
    To explain the observed pH decrease in the evaporation ponds, we applied a suite of geochemical tools, including boron isotopes (δ<sup>11</sup>B), geochemical modeling, and elemental analyses. Our results demonstrate that pH decline is controlled by boron speciation, which governs brine alkalinity and therefore controls brine pH. Extending this work, we compiled a large dataset of global lithium-rich brines and showed that the same process occurs throughout the Lithium Triangle and in Tibetan Plateau brines as well (see our <a href="https://doi.org/10.1126/sciadv.adw3268" target="_blank" rel="noopener">Science Advances</a> article).
  </p>

  <h2>Photos from the Field</h2>

  <!-- Responsive gallery: add as many <figure> blocks as you want -->
  <div class="gallery-grid">

    <figure>
      <img src="/images/SDU/SDU_BlueGlow.jpg" alt="Blue glow on Salar de Uyuni">
      <figcaption>Salar de Uyuni.</figcaption>
    </figure>

    <figure>
      <img src="/images/SDU/BlackWhiteSalar.jpg" alt="Evaporation ponds at Salar de Uyuni">
      <figcaption>Extracting shallow brine samples from beneath the salt crust.</figcaption>
    </figure>

    <figure>
      <img src="/images/SDU/SamplingDissolutionPit.jpeg" alt="Field team sampling brines">
      <figcaption>Sampling a natural dissolution pit in the salt crust.</figcaption>
    </figure>
    
    <figure>
      <img src="/images/SDU/SamplingEvapPond.jpeg" alt="Field team sampling brines">
      <figcaption>Sampling an industrial evaporation pond.</figcaption>
    </figure>
    
    <figure>
      <img src="/images/SDU/BikeSampling.jpg" alt="Field team sampling brines">
      <figcaption>Biking out to collect samples in the mud.</figcaption>
    </figure>

    <figure>
      <img src="/images/SDU/Llamas.jpg" alt="Field team sampling brines">
      <figcaption>Llamas</figcaption>
    </figure>
    
    <figure>
      <img src="/images/SDU/Incahuasi.jpg" alt="Field team sampling brines">
      <figcaption>View from Incahuasi "Island"</figcaption>
    </figure>
        
    <figure>
      <img src="/images/SDU/EveningHorizon.jpg" alt="Field team sampling brines">
      <figcaption>Salar de Uyuni</figcaption>
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

