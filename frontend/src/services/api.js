const BASE_URL = process.env.NODE_ENV === 'production' 
? 'https://mellow-nurturing-production.up.railway.app/docs'
: 'http://localhost:8000';

export async function registerUser(data) {
  const res = await fetch(`${BASE_URL}/api/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Registration failed");
  return await res.json();
}

export async function loginUser(credentials) {
  const res = await fetch("http://localhost:8000/api/users/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials)
  });

  if (!res.ok) throw new Error("Login failed");

  const data = await res.json(); 
  return data.access_token;
}

export async function getProfile() {
  const token = localStorage.getItem("token");
  const res = await fetch("http://localhost:8000/api/users/profile", {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!res.ok) {
    if (res.status === 401) {
      throw new Error("Unauthorized");
    }
    throw new Error("Failed to fetch profile");
  }

  return await res.json();
}

export async function getModules() {
  const res = await fetch(`${BASE_URL}/api/modules`);
  return await res.json();
}

export async function completeLesson(lessonData) {
  const token = localStorage.getItem("token");
  const res = await fetch("http://localhost:8000/api/progress/complete-lesson", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(lessonData),
  });

  if (!res.ok) {
    throw new Error("Failed to complete lesson");
  }

  return await res.json();
}

export async function getUserProgress(userEmail) {
  const token = localStorage.getItem("token");
  const res = await fetch(`${BASE_URL}/api/progress/${userEmail}`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!res.ok) {
    throw new Error("Failed to fetch progress");
  }

  return await res.json();
}

export async function getRecentActivities() {
  const token = localStorage.getItem("token");
  const res = await fetch(`${BASE_URL}/api/activities/recent`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!res.ok) {
    throw new Error("Failed to fetch recent activities");
  }

  return await res.json();
}