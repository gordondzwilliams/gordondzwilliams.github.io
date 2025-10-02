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
}
</style>

<div class="page-content">
  ## Research
  <!-- ✍️ Edit this intro text anytime -->

  <p>
    My research broadly focusses on the geochemistry and environmental impacts of lithium deposits and mining them. This includes work in (1) the Carolina Tin-Spodumene Belt of North Carolina which hosts hard-rock lithium deposits, where I investigate the natural and mining related water-quality impacts to streams and groundwater throughout a legacy mining region, and (2) the Salar de Uyuni in Bolivia which is the largest salt flat in the world and hosts a massive lithium brine resource that is currently under development where I investigate the geochemistry and geochemical evolution of brines and the potential water-quality impacts of mining them.
  </p>

  <p>Please click the images below for more information on each project!</p>

  <style>
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
  </style>

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
  </div>
</div>
