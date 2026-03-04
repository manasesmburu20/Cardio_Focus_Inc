// Authentication check - Include this in all protected pages
(function() {
    const isAuthenticated = sessionStorage.getItem('authenticated');
    
    // If not authenticated and not on login page, redirect to login
    if (!isAuthenticated && !window.location.pathname.includes('login.html')) {
        window.location.href = 'login.html';
    }
})();

// Logout function
function logout() {
    sessionStorage.removeItem('authenticated');
    sessionStorage.removeItem('username');
    window.location.href = 'login.html';
}
