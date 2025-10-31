const API_BASE = "http://localhost:5000/api";

// Check if user is logged in
async function checkAuth(redirectToLogin = true) {
  try {
    const response = await fetch(`${API_BASE}/session`, {
      credentials: "include",
    });
    const data = await response.json();

    if (!data.logged_in && redirectToLogin) {
      window.location.href = "login.html";
      return null;
    }

    return data.logged_in ? data : null;
  } catch (error) {
    console.error("Auth check failed:", error);
    if (redirectToLogin) {
      window.location.href = "login.html";
    }
    return null;
  }
}

// Login function
async function login(email, password) {
  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      return { success: true, customer: data.customer };
    } else {
      return { success: false, error: data.error };
    }
  } catch (error) {
    console.error("Login failed:", error);
    return { success: false, error: "Connection error" };
  }
}

// Logout function
async function logout() {
  try {
    await fetch(`${API_BASE}/logout`, {
      method: "POST",
      credentials: "include",
    });
    window.location.href = "login.html";
  } catch (error) {
    console.error("Logout failed:", error);
  }
}

// Get current user info
async function getCurrentUser() {
  try {
    const response = await fetch(`${API_BASE}/session`, {
      credentials: "include",
    });
    const data = await response.json();
    return data.logged_in ? data : null;
  } catch (error) {
    console.error("Error getting user:", error);
    return null;
  }
}

// Make functions available globally
window.authHelper = {
  checkAuth,
  login,
  logout,
  getCurrentUser,
  API_BASE,
};
