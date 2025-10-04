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
      <img src="/images/Teaching/GeoNC.jpg" alt="North Carolina field trip">
      <figcaption>Geology of North Carolina Field Trip</figcaption>
    </figure>

    <!-- duplicate/modify the figure blocks above for more photos -->
  </div> <!-- /.teaching-gallery -->

<!-- Unified Lightbox (replace previous lightbox block with this) -->
<style>
  #lightbox-overlay{display:none;position:fixed;z-index:9999;inset:0;background:rgba(0,0,0,0.85);align-items:center;justify-content:center;padding:24px;box-sizing:border-box}
  #lightbox-inner{max-width:98%;max-height:98%;display:flex;flex-direction:column;align-items:center;gap:8px}
  #lightbox-image{max-width:100%;max-height:80vh;border-radius:6px;box-shadow:0 8px 30px rgba(0,0,0,0.6)}
  #lightbox-caption{color:#eee;font-size:0.95rem;text-align:center;max-width:90%;margin-top:6px}
  #lightbox-close{position:absolute;top:12px;right:16px;background:rgba(255,255,255,0.06);color:#fff;border:none;padding:6px 10px;border-radius:6px;cursor:pointer;font-size:0.95rem;backdrop-filter:blur(2px)}
  #lightbox-close:hover{background:rgba(255,255,255,0.12)}
  @media (max-width:560px){#lightbox-image{max-height:70vh}#lightbox-caption{font-size:0.9rem}}
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
  // defensive DOM ready
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function() {
    const overlay = document.getElementById('lightbox-overlay');
    const overlayImg = document.getElementById('lightbox-image');
    const overlayCaption = document.getElementById('lightbox-caption');
    const closeBtn = document.getElementById('lightbox-close');

    if (!overlay || !overlayImg) {
      console.error('Lightbox: required elements missing');
      return;
    }

    // Open lightbox with given image element
    function openLightbox(imgEl) {
      const fullSrc = imgEl.getAttribute('data-full') || imgEl.src || imgEl.getAttribute('data-src');
      if (!fullSrc) {
        console.warn('Lightbox: no image source found for', imgEl);
        return;
      }
      overlayImg.src = fullSrc;
      overlayImg.alt = imgEl.alt || '';
      overlayCaption.textContent = imgEl.getAttribute('data-caption') || imgEl.alt || '';
      overlay.style.display = 'flex';
      overlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    // Close handler
    function closeLightbox() {
      overlay.style.display = 'none';
      overlay.setAttribute('aria-hidden', 'true');
      overlayImg.src = '';
      overlayCaption.textContent = '';
      document.body.style.overflow = '';
    }

    // Event delegation: catch clicks on images in these containers
    // selectors include project thumbnails, gallery images, teaching gallery
    const container = document; // delegate from document
    container.addEventListener('click', function(e) {
      const clickTarget = e.target;

      // If clicked element is an IMG inside one of our target selectors
      // We allow images inside:
      //  - .project-card__img
      //  - any img inside .gallery-grid
      //  - any img inside .teaching-gallery
      if (clickTarget && clickTarget.tagName === 'IMG') {
        const isProjectThumb = clickTarget.classList.contains('project-card__img');
        const inGalleryGrid = clickTarget.closest('.gallery-grid') !== null;
        const inTeaching = clickTarget.closest('.teaching-gallery') !== null;

        if (isProjectThumb || inGalleryGrid || inTeaching) {
          // Prevent the enclosing anchor from navigating when the IMG is clicked
          // Find nearest <a> ancestor and prevent its default navigation only for this event
          const anchor = clickTarget.closest('a');
          if (anchor) {
            e.preventDefault();
            // stop immediate propagation so other handlers don't override
            e.stopPropagation && e.stopPropagation();
          }

          // Open the lightbox
          openLightbox(clickTarget);
          return;
        }
      }

      // If user clicks a project-card anchor but not the image, allow navigation as normal
    }, true /* useCapture to be extra robust against other handlers */);

    // Close handlers
    closeBtn.addEventListener('click', closeLightbox);
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) closeLightbox();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && overlay.style.display === 'flex') closeLightbox();
    });

    // Helpful console message for debugging
    console.info('Lightbox: initialized (targets: .project-card__img, .gallery-grid img, .teaching-gallery img)');
  });
})();
</script>


</div> <!-- /.page-content -->
