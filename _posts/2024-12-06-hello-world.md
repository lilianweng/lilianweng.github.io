---
layout: post
title: Hello World - My First Blog Post
subtitle: Testing the blog setup and exploring features
tags: [introduction, blogging, tech]
comments: true
author: Omid Sardari
---

Welcome to my new blog! This is my first post to test out the Beautiful Jekyll setup and see how everything looks.

## Why I Started This Blog

I wanted a clean, minimal platform to share my thoughts on:
- **Programming and Development** - Code snippets, tutorials, and lessons learned
- **Technology Trends** - My take on what's happening in tech
- **Personal Projects** - Documenting my experiments and side projects

## Testing Code Highlighting

Let's see how code blocks look with syntax highlighting:

```python
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib

# Test the function
print(fibonacci(10))
# Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

And here's some JavaScript:

```javascript
// Simple theme toggle function
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
```

## Lists and Formatting

Here's what I'm planning to write about:

1. **Web Development**
   - React and modern JavaScript
   - Backend with Node.js and Python
   - DevOps and deployment strategies

2. **Machine Learning**
   - Data analysis with Python
   - Building and training models
   - Real-world ML applications

3. **Personal Growth**
   - Learning new technologies
   - Career insights
   - Book recommendations

### Quick Tips

{: .box-note}
**Note:** This blog is built with Jekyll and hosted on GitHub Pages. The source code is available on GitHub.

## What's Next?

I'm excited to start sharing more content. Some upcoming posts will include:

- Setting up a perfect development environment
- My favorite VS Code extensions for 2024
- Building a REST API with FastAPI
- Lessons learned from my latest side project

Thanks for reading, and welcome to my corner of the internet! 🚀

---

*Have thoughts or questions? Feel free to leave a comment below or reach out on GitHub.* 