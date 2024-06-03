var themeIcon = $('#themeIcon');
function setTheme(theme) {
    if (theme === 'dark') {
        $('html').attr('data-bs-theme', 'dark');
        $('#themeIcon').attr('class', 'bi-moon-stars-fill');
    } else if (theme === 'light') {
        $('html').attr('data-bs-theme', 'light');
        $('#themeIcon').attr('class', 'bi-brightness-high-fill');
    }
    localStorage.setItem('theme', theme);
}

var siteTheme = (localStorage.getItem('theme') != null)
    ? localStorage.getItem('theme')
    : 'light';
setTheme(siteTheme);