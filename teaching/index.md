---
layout: default
title: Teaching
permalink: /teaching/
---

<style>
.page-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
  line-height: 1.5;
}

.page-content h1,
.page-content h2,
.page-content h3 {
  margin-top: 1.25rem;
  margin-bottom: 0.6rem;
}

/* Layout: text left, photos right */
.content-row {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  margin: 1rem 0 1.5rem;
}

/* Text area */
.content-row .text {
  flex: 1 1 0%;
  min-width: 0;
}

/* Photos on the right */
.photos-column {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: stretch;
}

/* Photo styling */
.photos-column figure {
  margin: 0;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}

.photos-column img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  cursor: zoom-in;
}

.photos-column figcaption {
  padding: 0.5rem;
  font-size: 0.9rem;
  color: #333;
  text-align: center;
  line-height: 1.2;
}

/* Responsive layout: stack photos below text on small screens */
@media (max-width: 880px) {
  .content-row {
    flex-direction: column;
  }
  .photos-column {
    width: 100%;
    flex-direction: column;
    align-items: center;
  }
  .photos-column figure {
    width: 90%;
    max-width: 400px;
  }
}

/* Make sure long links wrap */
.page-content p, .page-content a {
  word-break: break-word;
}
</style>

<div class="page-content">
<p>
  
</p>
  <h1>Teaching</h1>

  <div class="content-row">
    <div class="text">
      <p>
        My applied research translates directly into my teaching, and I enjoy taking students into the field to explore the geology and environmental systems they first encounter in the classroom. I have extensive experience as a teaching assistant and co-leading both short and multi-day field trips in places like Ireland and North Carolina, where students engage with topics covering geology, mineral deposits, water quality, and field methods.
      </p>

    </div>

    <!-- Photos -->
    <aside class="photos-column" aria-label="Teaching photos">
      <figure>
        <img src="/images/Teaching/GeoIrelandFolds.JPEG" alt="Field trip in Ireland - folded outcrop">
        <figcaption>Geology of Ireland field trip</figcaption>
      </figure>

      <figure>
        <img src="/images/Teaching/GeoNC.jpg" alt="North Carolina field trip - students at outcrop">
        <figcaption>Geology of North Carolina field trip</figcaption>
      </figure>
    </aside>
  </div>

  <!-- Lightbox overlay -->
  <div class="lightbox" id="lightbox" role="dialog" aria-hidden="true" aria-label="Image preview">
    <button id="lightbox-close" aria-label="Close image" style="position:absolute;top:18px;right:20px;z-index:10001;background:transparent;border:none;color:#fff;font-size:1.6rem;cursor:pointer;">✕</button>
    <img src="" alt="">
  </div>

</div>

<style>
.lightbox {
  display: none;
  position: fixed;
  z-index: 10000;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.85);
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.lightbox img {
  max-width: 100%;
  max-height: 95vh;
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
</style>

<script>
(function() {
  const photos = document.querySelectorAll('.photos-column img');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = lightbox.querySelector('img');
  const closeBtn = document.getElementById('lightbox-close');

  function openLightbox(src, alt) {
    lightboxImg.src = src;
    lightboxImg.alt = alt || '';
    lightbox.style.display = 'flex';
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.style.display = 'none';
    lightboxImg.src = '';
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  photos.forEach(img => {
    img.addEventListener('click', () => openLightbox(img.src, img.alt));
    img.setAttribute('tabindex', '0');
    img.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') openLightbox(img.src, img.alt);
    });
  });

  closeBtn.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', e => {
    if (e.target === lightbox || e.target === lightboxImg) closeLightbox();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeLightbox();
  });
})();
</script>
