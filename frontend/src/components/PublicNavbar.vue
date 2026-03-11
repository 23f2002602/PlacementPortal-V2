<template>
  <nav class="glass-nav">
    <div class="container d-flex justify-content-between align-items-center">
      <router-link class="brand-link" to="/">
        <span class="brand-accent">P</span>lacement <span class="brand-accent">P</span>ortal
      </router-link>
      
      <div class="nav-links d-none d-lg-flex gap-4">
        <router-link to="/login" class="nav-item-link">Login</router-link>
        <router-link to="/register/student" class="nav-item-link">Student Portal</router-link>
        <router-link to="/register/company" class="nav-item-link company-btn">Partner With Us</router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.glass-nav {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  padding: 20px 0;
  background: rgba(2, 6, 23, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.brand-link {
  font-size: 1.6rem;
  font-weight: 800;
  color: white;
  text-decoration: none;
  letter-spacing: -0.02em;
}

.brand-accent {
  color: #6366f1;
}

.nav-item-link {
  color: #94a3b8;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
  padding: 8px 0;
}

.nav-item-link:hover {
  color: white;
}

.company-btn {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white !important;
  padding: 8px 20px !important;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.company-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}
</style>
