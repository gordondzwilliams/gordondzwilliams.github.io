---
layout: page
title: Publications
permalink: /publications/
---

<style>
  .pub-wrapper { max-width: 900px; margin: 0 auto; padding: 0 1rem; }
  .pub-year { margin-top: 2rem; margin-bottom: 0.5rem; font-weight: bold; }
  .pub-list { margin-top: 0; padding-left: 1.2rem; }
  .pub-list li { margin: 0.4rem 0; }
</style>

<div class="pub-wrapper">
{% assign pubs = site.publications | sort:"year" | reverse %}
{% assign current_year = "" %}

{% for p in pubs %}
  {% assign y = p.year | default: 'No year' %}
  {% if y != current_year %}
    {% if forloop.index != 1 %}
</ul>
    {% endif %}
<h2 class="pub-year">{{ y }}</h2>
<ul class="pub-list">
    {% assign current_year = y %}
  {% endif %}

<li>
  {% if p.doi %}
    <a href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">{{ p.title }}</a>
  {% elsif p.url %}
    <a href="{{ p.url }}" target="_blank" rel="noopener">{{ p.title }}</a>
  {% else %}
    {{ p.title }}
  {% endif %}
  {% if p.authors %} — {{ p.authors | join: ", " }}{% endif %}
  {% if p.journal %} — <em>{{ p.journal }}</em>{% endif %}
  {% if p.year %} ({{ p.year }}){% endif %}
</li>
{% endfor %}
</ul>
</div>
