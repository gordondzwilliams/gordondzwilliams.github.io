---
layout: page
title: CV
permalink: /cv/
---

<script>
(function () {
  var pdf = "{{ '/files/Williams_Gordon_CV.pdf' | relative_url }}";
  // Open PDF in a new tab
  try { window.open(pdf, '_blank', 'noopener'); } catch (e) {}
  // Then return the user to the previous page, or home if no history
  if (window.history.length > 1) {
    window.history.back();
  } else {
    window.location.href = "{{ '/' | relative_url }}";
  }
})();
</script>

<noscript>
  <p>
    JavaScript is off. Open my CV here:
    <a href="{{ '/files/Williams_Gordon_CV.pdf' | relative_url }}" target="_blank" rel="noopener">Download CV (PDF)</a>
  </p>
</noscript>
