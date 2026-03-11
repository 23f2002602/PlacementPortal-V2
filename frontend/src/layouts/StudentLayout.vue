<template>
  <div class="student-shell">
    <nav class="student-sidebar shadow-lg">
      <div class="sidebar-header p-4">
        <h4 class="text-royal fw-bold mb-0">Student <span class="text-white">Portal</span></h4>
      </div>
      
      <div class="nav-menu px-3 mt-3">
        <router-link to="/student" class="nav-item" exact>
          <i class="bi bi-house-door me-2"></i> Home
        </router-link>
        <router-link to="/student/drives" class="nav-item">
          <i class="bi bi-briefcase me-2"></i> Drives
        </router-link> 
        <router-link to="/student/applications" class="nav-item">
          <i class="bi bi-file-earmark-text me-2"></i> My Apps
        </router-link>
        <router-link to="/student/profile" class="nav-item">
          <i class="bi bi-person me-2"></i> Profile
        </router-link>
      </div>

      <div class="sidebar-footer p-4 mt-auto">
        <button @click="logout" class="btn-logout w-100">
          <i class="bi bi-box-arrow-right me-2"></i> Logout
        </button>
      </div>
    </nav>

    <main class="content-body">
      <header class="top-bar px-4 py-3">
        <span class="text-muted-light small">Welcome back, Student</span>
      </header>
      <div class="page-container">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('ppa_token');
      localStorage.removeItem('ppa_role');
      localStorage.removeItem('ppa_name');
      localStorage.removeItem('ppa_user_id');
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.student-shell { 
  display: flex;
  background-color: #121212; /* Dark Charcoal background */
  min-height: 100vh; 
}

.student-sidebar { 
  width: 260px;
  background-color: #181818; 
  border-right: 1px solid #2c2c2c;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.content-body { 
  margin-left: 260px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-bar {
  background: #121212;
  border-bottom: 1px solid #2c2c2c;
}

.page-container {
  padding: 2rem;
}

.text-royal { color: #7c4dff; } /* Royal Indigo */
.text-muted-light { color: #a0a0a0; }

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: #a0a0a0;
  text-decoration: none;
  font-weight: 500;
  border-radius: 10px;
  margin-bottom: 6px;
  transition: 0.2s;
}

.nav-item:hover, .router-link-active { 
  background-color: rgba(124, 77, 255, 0.1);
  color: #7c4dff; 
}

.btn-logout {
  background: transparent;
  border: 1px solid #f44336;
  color: #f44336;
  border-radius: 8px;
  padding: 10px;
  font-weight: 600;
  cursor: pointer;
}
</style>