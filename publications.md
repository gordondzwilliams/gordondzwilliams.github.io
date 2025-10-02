---
layout: page
title: Publications
permalink: /publications/
---

<style>
  /* Optional: lightweight styling */
  .pub-year { margin-top: 1.5rem; margin-bottom: 0.25rem; }
  .pub-list { margin-top: 0; }
  .pub-list li { margin: 0.25rem 0; }
</style>

{% comment %}
We sort all publications by year (descending), then emit a <h2> each time
the year changes, followed by that year's <ul>.
This automatically creates new year headings as new items appear.
{% endcomment %}

{% assign pubs = site.publications | sort:"year" | reverse %}
{% assign current_year = "" %}

{% for p in pubs %}
  {% assign y = p.year | default: 'No year' %}
  {% if y != current_year %}
    {% if forloop.index != 1 %}</ul>{% endif %}
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
  </li>
{% endfor %}
</ul>
