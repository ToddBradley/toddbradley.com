---
layout: page
title: Downloads Directory
permalink: /downloads/
---

Here are files I think somebody might want to download someday.

<ul>
  {% for file in site.static_files %}
    {% if file.path contains '/assets/downloads/' %}
      <li>
        <a href="{{ file.path | relative_url }}" download>
          {{ file.name }}
        </a>
        <small>({{ file.extname | upcase | remove: '.' }})</small>
      </li>
    {% endif %}
  {% endfor %}
</ul>
