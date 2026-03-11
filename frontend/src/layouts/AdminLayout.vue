<template>
  <div class="admin-shell">
    <nav class="sidebar">
      <div class="sidebar-header p-4">
        <h4 class="fw-bold text-royal mb-0">Placement <span class="text-white">Hub</span></h4>
      </div>
      <div class="sidebar-menu px-3">
        <router-link to="/admin" class="nav-item">
          <i class="bi bi-grid-1x2 me-2"></i> Dashboard
        </router-link>
        <router-link to="/admin/students" class="nav-item">
          <i class="bi bi-people me-2"></i> Students
        </router-link>
        <router-link to="/admin/companies" class="nav-item">
          <i class="bi bi-building-check me-2"></i> Partners
        </router-link>
        <router-link to="/admin/drives" class="nav-item">
          <i class="bi bi-briefcase me-2"></i> Drives
        </router-link>
      </div>
    </nav>
    
    <div class="main-content">
      <header class="top-nav px-4 py-3">
        <span class="fw-bold text-white">System Administration</span>
        <button @click="logout" class="logout-btn">Logout</button>
      </header>
      
      <div class="page-body">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    }
  }
}
</script>

<style scoped>
/* UPDATED: Dark Charcoal background for the administrative side */
.admin-shell {
  display: flex;
  min-height: 100vh;
  background-color: #121212; 
}

/* UPDATED: Sidebar styling with panel-dark background */
.sidebar {
  width: 260px;
  background: #181818;
  border-right: 1px solid #2c2c2c;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.main-content {
  margin-left: 260px;
  flex: 1;
}

.sidebar-header h4 { font-size: 1.25rem; }

/* UPDATED: Navigation items with Royal Indigo hover states */
.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: #888;
  text-decoration: none;
  border-radius: 10px;
  margin-bottom: 6px;
  transition: all 0.2s;
}

.nav-item:hover, .router-link-active {
  background-color: rgba(124, 77, 255, 0.1);
  color: #7c4dff;
}

/* UPDATED: Top navigation with charcoal background and subtle border */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #121212;
  border-bottom: 1px solid #2c2c2c;
}

.logout-btn {
  background: transparent;
  border: 1px solid #f44336;
  color: #f44336;
  padding: 6px 16px;
  border-radius: 8px;
  font-weight: 600;
  transition: 0.2s;
}

.logout-btn:hover {
  background: rgba(244, 67, 54, 0.1);
}

.text-royal { color: #7c4dff; }
.page-body { padding: 2rem; }
</style>