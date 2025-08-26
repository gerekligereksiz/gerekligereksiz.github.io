---
title: 'Anasayfa'
date: 2025-08-26
type: landing
sidebar:
  title: Hızlı Menü
  text: "Kısa açıklama."
  sticky: false
  links:
    - label: Blog
      url: /blog/
    - label: Hakkımda
      url: /authors/admin/
sections:
  - block: collection
    id: posts
    content:
      title: Son yazılar
      subtitle: ''
      text: 'Aşağıdaki son blog yazılarıma göz atın!'
      # Choose how many pages you would like to display (0 = all pages)
      count: 10
      # Filter on criteria
      filters:
        # The folders to display content from
        folders:
          - blog
        author: ""
        category: ""
        tag: ""
        publication_type: ""
        featured_only: false
        exclude_featured: false
        exclude_future: false
        exclude_past: false
      # Choose how many pages you would like to offset by
      # Useful if you wish to show the first item in the Featured widget
      offset: 0
      # Field to sort by, such as Date or Title
      sort_by: 'Date'
      sort_ascending: false
    design:
      # Choose a listing view
      view: card
      spacing:
        padding: ['1rem', 0, 0, 0]
  - block: markdown
    content:
      text: |
        <div class="text-center">
          <a href="/blog/" style="text-decoration: none;" class="inline-block px-4 py-2 rounded-md bg-primary-700 text-white hover:bg-primary-800 dark:bg-primary-500 dark:hover:bg-primary-400">Tümünü gör</a>
        </div>
    design:
      spacing:
        padding: [0, 0, 0, 0]
---
