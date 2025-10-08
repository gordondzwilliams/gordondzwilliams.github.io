---
layout: single
title: Publications
permalink: /publications/
classes: wide
author_profile: true
---

<style>
/* small callout style for the Scholar link */
.pub-callout {
  border-left: 4px solid #2a6f9e;
  background: #f5f9fc;
  padding: 10px 14px;
  margin-bottom: 1rem;
  border-radius: 4px;
  color: #0b3b57;
}
.pub-callout a { font-weight: 600; color: #0b3b57; text-decoration: underline; }
.pub-empty { color: #666; font-size: 0.95rem; margin-bottom: 1rem; }
</style>

<div class="pub-callout" role="note" aria-label="Google Scholar">
  You can also find my work on
  <a href="https://scholar.google.com/citations?user=YvgsRxsAAAAJ&hl=en" target="_blank" rel="noopener">
    Google Scholar
  </a>.
</div>

{%- comment -%}
Optional debug: to see whether the publications collection is being read,
you can temporarily uncomment the block below. It will output the number
of items in site.publications.
{%- endcomment -%}

{%- comment -%}
<p class="pub-empty">Debug: Publications found: {{ site.publications | size }}</p>
{%- endcomment -%}

{% assign pubs = site.publications | sort:"year" | reverse %}
{% assign current_year = "" %}

{% if pubs == empty %}
  <p class="pub-empty">No publications found in the `site.publications` collection. Make sure your `_publications/` folder exists and files are committed.</p>
{% endif %}

{% for p in pubs %}
  {% assign y = p.year | default: 'No year' %}
  {% if y != current_year %}
    {% if forloop.index != 1 %}
</ul>
    {% endif %}
### {{ y }}
<ul>
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
  {% if p.pdf %}
    &nbsp; <a href="{{ p.pdf | relative_url }}" target="_blank" rel="noopener">[PDF]</a>
  {% endif %}
</li>
{% endfor %}
</ul>
