---
layout: single
title: Publications (DEBUG)
permalink: /publications/
classes: wide
author_profile: true
---

<!-- VERY VISIBLE DEBUG BANNER - remove after testing -->
<div style="background:#b20000;color:#fff;padding:18px;border-radius:6px;margin-bottom:18px;font-size:1.15rem;">
  DEBUG: If you see this banner, the `publications/index.md` file is being used. If you do NOT see this banner, a different file is rendering / caching is happening.
</div>

<!-- Google Scholar link -->
<p style="font-size:1.05rem; margin-bottom:1rem;">
  You can also find my work on
  <a href="https://scholar.google.com/citations?user=YvgsRxsAAAAJ&hl=en" target="_blank" rel="noopener">Google Scholar</a>.
</p>

<!-- Publication collection check -->
<p style="color:#555;margin-bottom:1rem;">
  Debug: publications found = <strong>{{ site.publications | size }}</strong>
</p>

{%- comment -%}
Uncomment the block below to print raw data about the first publication (handy to inspect whether `pdf` exists).
Be careful — this prints raw Liquid/Jekyll output.
{%- endcomment -%}

{%- comment -%}
{% if site.publications and site.publications.size > 0 %}
  <h4>First publication (raw):</h4>
  <pre style="background:#f5f5f5;padding:10px;border-radius:6px">{{ site.publications | first | inspect }}</pre>
{% endif %}
{%- endcomment -%}

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
