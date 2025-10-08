---
layout: default
title: Teaching
permalink: /teaching/
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
  <p>  
    
  </p>
  <h1>Teaching</h1>
  <p>
    My applied research translates directly into my teaching, and I enjoy taking students into the field to explore the geology and environmental systems they first encounter in the classroom. I have extensive experience as a teaching assistant, leading both short and multi-day field trips in places like Ireland and North Carolina, where students engage with topics covering geology, mineral deposits, water quality, and field methods.
  </p>

 <!-- Teaching gallery -->
<style>
/* Teaching gallery grid */
.teaching-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); /* 2–3 per row depending on width */
  gap: 16px;
  margin: 1.5rem 0;
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
  height: 180px; /* adjust for smaller thumbnails */
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
</style>

<div class="teaching-gallery">
  <figure>
    <img src="/images/Teaching/GeoIrelandFolds.JPEG" alt="Field trip, sampling outcrop">
    <figcaption>Geology of Ireland Field Trip</figcaption>
  </figure>

  <figure>
    <img src="/images/Teaching/GeoNC.jpg" alt="North Carolina field trip">
    <figcaption>Geology of North Carolina Field Trip</figcaption>
  </figure>

  <!-- Add more photos below in the same <figure> format -->
</div> <!-- /.teaching-gallery -->


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



