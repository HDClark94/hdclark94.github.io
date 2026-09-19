---
layout: page
permalink: /ideas/
title: ideas
description: Working notes on questions I keep circling back to. Speculative by design, and revised as I read more.
nav: true
nav_order: 2
---

<div class="post">
  <ul class="post-list">
    {% assign sorted_ideas = site.ideas | sort: 'date' | reverse %}
    {% for idea in sorted_ideas %}
      <li>
        <h3>
          <a class="post-title" href="{{ idea.url | relative_url }}">{{ idea.title }}</a>
        </h3>
        <p>{{ idea.description }}</p>
        <p class="post-meta">{{ idea.date | date: '%B %-d, %Y' }}</p>
        {% if idea.tags.size > 0 %}
          <p class="post-tags">
            {% for tag in idea.tags %}
              <i class="fa-solid fa-hashtag fa-sm"></i> {{ tag }}&nbsp;
            {% endfor %}
          </p>
        {% endif %}
      </li>
    {% endfor %}
  </ul>
</div>
