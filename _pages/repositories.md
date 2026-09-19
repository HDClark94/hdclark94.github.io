---
layout: page
permalink: /repositories/
title: repositories
description: Code from my research, and the labs I work with.
nav: true
nav_order: 3
---

## GitHub users

{% if site.data.repositories.github_users %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-stretch">
  {% for user in site.data.repositories.github_users %}
    <div class="repo p-2">
      {% include repository/repo_user.liquid username=user %}
    </div>
  {% endfor %}
</div>

{% endif %}

## Repositories

{% if site.data.repositories.github_repos %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-stretch">
  {% for repo in site.data.repositories.github_repos %}
    <div class="repo p-2">
      {% include repository/repo.liquid repository=repo %}
    </div>
  {% endfor %}
</div>

{% endif %}
