<template>
<div class="landing-page">
  <PublicNavbar />
  <main class="hero-section">
    <div class="container text-center">
      <div class="badge-pill mb-4">Empowering the Next Generation</div>
      <h1 class="hero-title mb-4">Bridging the Gap Between <br> <span class="gradient-text">Talent and Opportunity</span></h1>
      <p class="hero-subtitle mb-5">
        The ultimate platform for streamlined placements, connecting India's top students <br> 
        with leading global recruitment partners.
      </p>
      <div class="hero-actions d-flex gap-3 justify-content-center">
        <router-link to="/register/student" class="btn-primary-lg">Get Started as Student</router-link>
        <router-link to="/login" class="btn-outline-lg">Login to Portal</router-link>
      </div>
    </div>
    
    <!-- Floating background elements -->
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
  background: #020617;
  color: white;
  min-height: 100vh;
  overflow: hidden;
  position: relative;
}

.hero-section {
  padding: 180px 0 100px;
  position: relative;
  z-index: 2;
}

.badge-pill {
  display: inline-block;
  padding: 8px 20px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 100px;
  color: #818cf8;
  font-weight: 600;
  font-size: 0.9rem;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.04em;
}

.gradient-text {
  background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #94a3b8;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.btn-primary-lg {
  padding: 16px 32px;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 700;
  transition: all 0.2s;
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
}

.btn-primary-lg:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 30px -5px rgba(99, 102, 241, 0.5);
}

.btn-outline-lg {
  padding: 16px 32px;
  background: transparent;
  color: white;
  border: 2px solid #1e293b;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 700;
  transition: all 0.2s;
}

.btn-outline-lg:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: #334155;
}

/* Background effects */
.orb {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
  z-index: 1;
}

.orb-1 {
  top: -200px;
  left: -200px;
  background: #6366f1;
}

.orb-2 {
  bottom: -200px;
  right: -200px;
  background: #a855f7;
}
</style>