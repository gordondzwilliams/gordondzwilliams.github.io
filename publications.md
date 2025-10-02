---
layout: page
title: Publications
permalink: /publications/
---

{% assign pubs = site.publications | sort:"year" | reverse %}
<ul>
  {% for p in pubs %}
    <li>
      <a href="{{ p.url }}">{{ p.title }}</a>
      {% if p.authors %} — {{ p.authors | join: ", " }}{% endif %}
      {% if p.year %} ({{ p.year }}){% endif %}
    </li>
  {% endfor %}
</ul>
