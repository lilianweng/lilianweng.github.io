---
layout: page
title: Archive
subtitle: All blog posts chronologically
---

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}

{% for year_group in posts_by_year %}
## {{ year_group.name }}

{% for post in year_group.items %}
* **{{ post.date | date: "%B %-d" }}** - [{{ post.title }}]({{ post.url | relative_url }})
  {% if post.subtitle %}<br/>*{{ post.subtitle }}*{% endif %}
{% endfor %}

{% endfor %}

---

*Total posts: {{ site.posts.size }}* 