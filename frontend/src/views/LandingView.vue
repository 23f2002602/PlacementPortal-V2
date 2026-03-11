<template>
<div class="landing-page">
  <PublicNavbar />
  <main class="hero-section">
    <div class="container text-center">
      <div class="badge-pill mb-4">Empowering the Next Generation</div>
      <h1 class="hero-title mb-4">Your Gateway to Success</h1>
      <p class="hero-subtitle mb-5">
        Connecting talented students with great career opportunities.
      </p>
      <div class="hero-actions d-flex gap-3 justify-content-center">
        <router-link to="/register/student" class="btn-primary-lg">Get Started as Student</router-link>
        <router-link to="/login" class="btn-outline-lg">Login to Portal</router-link>
      </div>
    </div>
    
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
  </main>
</div>
</template>

<script>
import PublicNavbar from '@/components/PublicNavbar.vue'

export default {
  components: {
    PublicNavbar
  }
}
</script>

<style scoped>
.landing-page {
  background: var(--bg-dark); /* Updated for uniformity */
  color: var(--text-main);
  min-height: 100vh;
  overflow-y: auto; 
}
.hero-section { padding: 140px 0 80px; flex-grow: 1; display: flex; align-items: center; position: relative; z-index: 2; }
.hero-title { font-size: clamp(2.5rem, 6vw, 4rem); font-weight: 800; }
.hero-subtitle { color: var(--text-muted); font-size: 1.2rem; max-width: 600px; margin: 0 auto; }

.btn-primary-lg {
  padding: 14px 28px;
  background: var(--primary-gradient); /* Updated for uniformity */
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 700;
}
.btn-outline-lg {
  padding: 14px 28px;
  border: 2px solid var(--border-color); /* Updated for uniformity */
  color: white;
  text-decoration: none;
  border-radius: 10px;
}
.orb-1 { position: absolute; top: -100px; left: -100px; width: 500px; height: 500px; border-radius: 50%; filter: blur(120px); opacity: 0.15; background: var(--primary-indigo); }
</style>