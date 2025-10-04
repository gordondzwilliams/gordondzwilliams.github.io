---
layout: default
title: Research
permalink: /research/
---

<style>
/* Add spacing so content isn’t flush with screen edges */
.page-content {
  max-width: 900px;   /* keeps text in a nice readable width */
  margin: 0 auto;     /* centers the content */
  padding: 0 20px;    /* adds space on left/right */
  box-sizing: border-box;
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

/* Teaching gallery: reuse responsive grid but smaller thumbnails */
.teaching-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 1.25rem 0 2rem;
}
.teaching-gallery figure {
  margin: 0;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
}
.teaching-gallery img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}
.teaching-gallery figcaption {
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
  <h2>Research</h2>
  
  <!-- ✍️ Edit this intro text anytime -->
  <p>
   My research broadly focuses on the geochemistry and environmental impacts of lithium deposits and mining them. Lithium is currently produced from two main deposit types (1) Lithium-Cesium-Tantalum (LCT) pegmatites which are hard-rock deposits and (2) closed-basin brines which are hypersaline waters. My work encompasses both including project site at (1) the Carolina Tin-Spodumene Belt of North Carolina which hosts LCT-pegmatite deposits, where I investigate the natural and mining related water-quality impacts to streams and groundwater throughout a legacy mining region, and (2) the Salar de Uyuni in Bolivia which is the largest salt flat in the world and hosts a massive lithium brine resource that is currently under development where I investigate the geochemistry and geochemical evolution of brines and the potential water-quality impacts of mining them.
  </p>

  <p>Please click the images below for more information on each project!</p>

  <div class="project-grid">
    {% assign projs = site.projects | sort: "order" | reverse %}
    {% for p in projs %}
    <a class="project-card" href="{{ p.url | relative_url }}">
      {% if p.image %}
        <img class="project-card__img" src="{{ p.image | relative_url }}" alt="{{ p.title }} cover">
      {% else %}
        <div class="project-card__img" aria-hidden="true"></div>
      {% endif %}
      <div class="project-card__body">
        <h3 class="project-card__title">{{ p.title }}</h3>
        {% if p.excerpt %}
          <p class="project-card__desc">{{ p.excerpt }}</p>
        {% elsif p.description %}
          <p class="project-card__desc">{{ p.description }}</p>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div> <!-- /.project-grid -->

  <!-- ===== Teaching section (placed BELOW the project gallery) ===== -->
  <h2>Teaching</h2>
  <p>
    My applied research translates directly into my teaching, and I enjoy taking students into the field to explore the geology and environmental systems they first encounter in the classroom. I have extensive experience as a teaching assistant, leading both short and multi-day field trips in Ireland and North Carolina, where students engage with topics covering geology, mineral deposits, water quality, and field methods.
  </p>

  <!-- Teaching photo gallery: add/remove <figure> blocks and update image src/captions -->
  <div class="teaching-gallery">

    <figure>
      <img src="/images/Teaching/GeoIrelandFolds.JPEG" alt="Field trip, sampling outcrop">
      <figcaption>Geology of Ireland Field Trip</figcaption>
    </figure>

    <figure>
      <img src="/images/Teaching/GeoNC.jpg" alt="Ireland field trip">
      <figcaption>Geology of North Carolina Field Trip</figcaption>
    </figure>


    <!-- duplicate/modify the figure blocks above for more photos -->
  </div> <!-- /.teaching-gallery -->

<!-- Lightbox overlay (place this just before the final </div> <!-- /.page-content --> ) -->
<style>
/* Lightbox overlay */
#lightbox-overlay {
  display: none;
  position: fixed;
  z-index: 9999;
  inset: 0; /* top:0; right:0; bottom:0; left:0 */
  background: rgba(0,0,0,0.85);
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
}

/* Container for image + caption */
#lightbox-inner {
  max-width: 98%;
  max-height: 98%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

#lightbox-inner img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 6px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
}

/* Caption */
#lightbox-caption {
  color: #eee;
  font-size: 0.95rem;
  text-align: center;
  max-width: 90%;
}

/* Close button */
#lightbox-close {
  position: absolute;
  top: 12px;
  right: 16px;
  background: rgba(255,255,255,0.06);
  color: #fff;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  backdrop-filter: blur(2px);
}
#lightbox-close:hover { background: rgba(255,255,255,0.12); }

/* Small screens tweak */
@media (max-width: 560px) {
  #lightbox-inner img { max-height: 70vh; }
  #lightbox-caption { font-size: 0.9rem; }
}
</style>

<div id="lightbox-overlay" aria-hidden="true" role="dialog" aria-modal="true">
  <button id="lightbox-close" aria-label="Close image">✕</button>
  <div id="lightbox-inner">
    <img id="lightbox-image" src="" alt="">
    <div id="lightbox-caption"></div>
  </div>
</div>

<script>
(function() {
  const overlay = document.getElementById('lightbox-overlay');
  const overlayImg = document.getElementById('lightbox-image');
  const overlayCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.getElementById('lightbox-close');

  // Target project thumbnails, the gallery-grid, and the teaching-gallery
  const selectors = '.project-card__img, .gallery-grid img, .teaching-gallery img';
  document.querySelectorAll(selectors).forEach(img => {
    // show zoom cursor
    img.style.cursor = 'zoom-in';

    img.addEventListener('click', function(e) {
      // Prevent navigation if image is inside an <a>
      if (e && e.preventDefault) e.preventDefault();

      // Prefer a data-full attribute for full-size image, otherwise use image src
      const fullSrc = img.getAttribute('data-full') || img.src || img.getAttribute('data-src');
      if (!fullSrc) return;

      overlayImg.src = fullSrc;
      overlayImg.alt = img.alt || '';

      // Prefer explicit caption stored in data-caption, otherwise fall back to alt text
      const caption = img.getAttribute('data-caption') || img.alt || '';
      overlayCaption.textContent = caption;

      overlay.style.display = 'flex';
      overlay.setAttribute('aria-hidden', 'false');

      // lock page scroll while lightbox open
      document.body.style.overflow = 'hidden';
    });
  });

  function closeLightbox() {
    overlay.style.display = 'none';
    overlay.setAttribute('aria-hidden', 'true');
    overlayImg.src = '';
    overlayCaption.textContent = '';
    document.body.style.overflow = '';
  }

  // Close handlers
  closeBtn.addEventListener('click', closeLightbox);
  overlay.addEventListener('click', function(e) {
    // Close only when clicking the backdrop (not the inner image)
    if (e.target === overlay) closeLightbox();
  });

  // ESC key closes
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && overlay.style.display === 'flex') {
      closeLightbox();
    }
  });
})();
</script>

</div> <!-- /.page-content -->
