/* ==========================================================================
   ASTRAL GLOBAL JAVASCRIPT - Main Utilities, Navigation & Utilities
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Highlight Active Nav Item
  const currentPath = window.location.pathname;
  const navItems = document.querySelectorAll(".portal-nav-links .nav-item, .sidebar-item");
  
  navItems.forEach(item => {
    const link = item.querySelector("a");
    if (link) {
      const href = link.getAttribute("href");
      if (currentPath === href || (href !== "/" && currentPath.includes(href))) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    }
  });

  // 2. Set Current Date Display (e.g. August 11, 2026 Monday)
  const dateElement = document.getElementById("current-date-display");
  if (dateElement) {
    const today = new Date(2026, 7, 11);
    const dateStr = today.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    const dayStr = today.toLocaleDateString('en-US', { weekday: 'long' });
    dateElement.innerHTML = `<div>${dateStr}</div><div style="font-size: 0.75rem; color: #64748B; font-weight: 400; text-align: right;">${dayStr}</div>`;
  }

  // 3. User Profile Information Population
  const userStr = localStorage.getItem("astral_user") || localStorage.getItem("astra_user");
  if (userStr) {
    try {
      const user = JSON.parse(userStr);
      const nameElems = document.querySelectorAll(".user-name-target");
      nameElems.forEach(el => el.textContent = user.name || "Vikramaditya Rao");
      const roleElems = document.querySelectorAll(".user-role-target");
      roleElems.forEach(el => el.textContent = user.role || "Executive Manager");
    } catch (e) {
      console.warn("User parse fallback");
    }
  }

  // 4. Logout Action
  const logoutBtns = document.querySelectorAll(".logout-trigger");
  logoutBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("astral_token");
      localStorage.removeItem("astral_user");
      localStorage.removeItem("astra_token");
      localStorage.removeItem("astra_user");
      window.location.href = "/login";
    });
  });

  // 5. Mobile Navbar Toggle
  const menuToggleBtn = document.getElementById("mobile-menu-toggle");
  const portalNavMenu = document.getElementById("portal-nav-menu") || document.querySelector(".portal-nav-links") || document.querySelector(".sidebar");
  if (menuToggleBtn && portalNavMenu) {
    menuToggleBtn.addEventListener("click", () => {
      portalNavMenu.classList.toggle("mobile-open");
    });
  }
});

// Helper API Fetcher
async function apiFetch(endpoint, options = {}) {
  try {
    const response = await fetch(endpoint, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    return null;
  }
}
