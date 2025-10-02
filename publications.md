---
layout: page
title: Publications
permalink: /publications/
---

{% assign pubs = site.publications | sort:"year" | reverse %}
<ul>
{% for p in pubs %}
  <li>
    {% if p.doi %}
      <a href="{{ p.url | default: 'https://doi.org/' | append: p.doi }}" target="_blank" rel="noopener">
        {{ p.title }}
      </a>
    {% else %}
      <a href="{{ p.url | default: p.url }}">{{ p.title }}</a>
    {% endif %}
    {% if p.authors %} — {{ p.authors | join: ", " }}{% endif %}
    {% if p.journal %} — <em>{{ p.journal }}</em>{% endif %}
    {% if p.year %} ({{ p.year }}){% endif %}
  </li>
{% endfor %}

</ul>
