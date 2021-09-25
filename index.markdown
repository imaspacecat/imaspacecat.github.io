---
title: Home
layout: default
---

Welcome to the Home page! Here you will find all our latest posts and updates.

<ul>
  {% for post in site.posts %}
    <li>      
        <a href="{{ post.url }}">{{ post.title }}</a>
        <ul>
          <li> {{ post.description }} </li>
        </ul>
    </li>
  {% endfor %}
</ul>
