// Theme toggle logic
document.addEventListener('DOMContentLoaded', function () {
    // Get the current theme from localStorage or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';

    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Create and add the theme toggle button to the navbar
    const navbar = document.querySelector('.navbar-nav');
    if (navbar) {
        const themeToggle = document.createElement('li');
        themeToggle.innerHTML = `
      <a href="#" class="theme-toggle" id="theme-toggle" title="Toggle dark/light mode">
        ${currentTheme === 'light' ? '🌙' : '☀️'}
      </a>
    `;
        navbar.appendChild(themeToggle);

        // Add event listener to the toggle button
        const toggle = document.getElementById('theme-toggle');
        toggle.addEventListener('click', function (e) {
            e.preventDefault();

            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            // Update the theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            // Update button text
            toggle.textContent = newTheme === 'light' ? '🌙' : '☀️';
            toggle.title = `Switch to ${newTheme === 'light' ? 'dark' : 'light'} mode`;
        });
    }

    // Also check for system preference on first visit
    if (!localStorage.getItem('theme')) {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            const toggle = document.getElementById('theme-toggle');
            if (toggle) {
                toggle.textContent = '☀️';
                toggle.title = 'Switch to light mode';
            }
        }
    }
}); 