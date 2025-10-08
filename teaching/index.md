---
layout: default
title: Teaching
permalink: /teaching/
---

<style>
.page-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 28px 20px 20px; /* added top padding to match Research page */
  box-sizing: border-box;
  line-height: 1.5;
}

/* Optional: consistent spacing for headings & paragraphs */
.page-content h1,
.page-content h2,
.page-content h3 {
  margin-top: 1.25rem;
  margin-bottom: 0.6rem;
}

/* Teaching gallery grid */
.teaching-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 1.5rem 0 2rem;
}
.teaching-gallery figure {
  margin: 0;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
}
.teaching-gallery img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  cursor: zoom-in;
}
.teaching-gallery figcaption {
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
  color: #333;
  line-height: 1.3;
  text-align: center;
}

/* Lightbox overlay */
.lightbox {
  display: none;
  position: fixed;
  z-index: 9999;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.85);
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.lightbox[aria-hidden="false"] {
  display: flex;
}
.lightbox .lightbox-inner {
  position: relative;
  max-width: 95%;
  max-height: 95%;
  text-align: center;
}
.lightbox img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  display: block;
  margin: 0 auto;
}
.lightbox .caption {
  color: #f5f5f5;
  font-size: 1rem;
  margin-top: 0.75rem;
  line-height: 1.4;
}
.lightbox .close-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #222;
  color: #fff;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
</style>

<div class="page-content">

  <h1>Teaching</h1>

  <p>
    My applied research translates directly into my teaching, and I enjoy taking students into the field to explore the geology and environmental systems they first encounter in the classroom. I have extensive experience as a teaching assistant, leading both short and multi-day field trips in places like Ireland and North Carolina, where students engage with topics covering geology, mineral deposits, water quality, and field methods.
  </p>

  <!-- Teaching gallery -->
  <div class="teaching-gallery">
    <figure>
      <img src="/images/Teaching/GeoIrelandFolds.JPEG" alt="Field trip in Ireland - folded outcrop">
      <figcaption>Geology of Ireland Field Trip</figcaption>
    </figure>

    <figure>
      <img src="/images/Teaching/GeoNC.jpg" alt="North Carolina field trip">
      <figcaption>Geology of North Carolina Field Trip</figcaption>
    </figure>
  </div>

  <!-- Lightbox -->
  <div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-label="Image preview">
    <div class="lightbox-inner">
      <button class="close-btn" id="lightbox-close" aria-label="Close image">✕</button>
      <img src="" alt="" id="lightbox-img">
      <div class="caption" id="lightbox-caption"></div>
    </div>
  </div>

</div>

<script>
(function() {
  const thumbs = document.querySelectorAll('.teaching-gallery img');
  const lightbox = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightbox-img');
  const lbCaption = document.getElementById('lightbox-caption');
  const lbClose = document.getElementById('lightbox-close');

  if (!thumbs.length || !lightbox) return;

  thumbs.forEach(img => {
    img.setAttribute('tabindex', '0');

    img.addEventListener('click', () => openLightbox(img));
    img.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openLightbox(img);
      }
    });
  });

  function openLightbox(imgEl) {
    lbImg.src = imgEl.src;
    lbImg.alt = imgEl.alt || '';
    const caption = imgEl.closest('figure')?.querySelector('figcaption')?.innerText || '';
    lbCaption.textContent = caption;
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    lbClose.focus();
  }

  function closeLightbox() {
    lightbox.setAttribute('aria-hidden', 'true');
    lbImg.src = '';
    lbCaption.textContent = '';
    document.body.style.overflow = '';
  }

  lbClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', e => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && lightbox.getAttribute('aria-hidden') === 'false') {
      closeLightbox();
    }
  });
})();
</script>
