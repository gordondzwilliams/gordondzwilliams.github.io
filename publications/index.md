---
layout: single
title: Publications
permalink: /publications/
classes: wide
author_profile: true
---

<!-- Google Scholar link: update YOUR_GOOGLE_SCHOLAR_ID -->
<p style="font-size:1.05rem; margin-bottom:1rem;">
  You can also find my work on
  <a href="https://scholar.google.com/citations?user=YvgsRxsAAAAJ&hl=en" target="_blank" rel="noopener">
    Google Scholar
  </a>.
</p>

{% assign pubs = site.publications | sort:"year" | reverse %}
{% assign current_year = "" %}

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
