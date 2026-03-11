<template>
  <div class="admin-dashboard">
    <div class="header-section mb-5">
      <h1 class="fw-bold text-royal display-5">Admin Overview</h1>
      <p class="text-muted-light">Track institutional placement progress and management.</p>
    </div>
    
    <div class="row g-4 mb-5">
      <div v-for="(stat, key) in primaryStats" :key="key" class="col-md-3">
        <div class="card border-0 shadow-lg h-100 stat-card" :class="stat.customClass">
          <div class="card-body p-4 text-white">
            <h6 class="text-uppercase small fw-bold opacity-75 mb-3">{{ stat.label }}</h6>
            <h2 class="display-5 fw-bold mb-0">{{ stat.value }}</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-md-6">
        <div class="card border-0 shadow-lg h-100 detail-card">
          <div class="card-body p-4">
            <div class="d-flex align-items-center mb-4">
              <div class="icon-box bg-royal-soft text-royal me-3">
                <i class="bi bi-building"></i>
              </div>
              <h5 class="card-title fw-bold mb-0 text-white">Company Pipeline</h5>
            </div>
            <div class="list-group list-group-flush">
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0 border-dark-muted">
                <span class="text-muted-light">Approved Partners</span>
                <span class="badge bg-success rounded-pill px-3">{{ stats.approved_companies }}</span>
              </div>
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0 border-dark-muted">
                <span class="text-muted-light">Pending Review</span>
                <span class="badge bg-warning text-dark rounded-pill px-3">{{ stats.pending_companies }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card border-0 shadow-lg h-100 detail-card">
          <div class="card-body p-4">
            <div class="d-flex align-items-center mb-4">
              <div class="icon-box bg-royal-soft text-royal me-3">
                <i class="bi bi-briefcase"></i>
              </div>
              <h5 class="card-title fw-bold mb-0 text-white">Placement Progress</h5>
            </div>
            <div class="list-group list-group-flush">
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0 border-dark-muted">
                <span class="text-muted-light">Total Job Applications</span>
                <span class="badge bg-royal rounded-pill px-3">{{ stats.total_applications }}</span>
              </div>
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0 border-dark-muted">
                <span class="text-muted-light">Confirmed Selections</span>
                <span class="badge bg-success rounded-pill px-3">{{ stats.selected_count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import API from "../../utils/api.js"

export default {
  data() {
    return {
      stats: {
        total_students: 0,
        total_companies: 0,
        approved_companies: 0,
        pending_companies: 0,
        total_drives: 0,
        approved_drives: 0,
        pending_drives: 0,
        total_applications: 0,
        selected_count: 0
      }
    }
  },
  computed: {
    primaryStats() {
      return [
        { label: 'Total Students', value: this.stats.total_students, customClass: 'bg-royal-grad' },
        { label: 'Selections', value: this.stats.selected_count, customClass: 'bg-success-dark' },
        { label: 'Total Companies', value: this.stats.total_companies, customClass: 'bg-card-dark' },
        { label: 'Active Drives', value: this.stats.total_drives, customClass: 'bg-info-dark' }
      ]
    }
  },
  async mounted() {
    const res = await API.get("/admin/dashboard")
    this.stats = res.data
  }
}
</script>

<style scoped>
/* UPDATED: Dashboard background changed to charcoal */
.admin-dashboard {
  background-color: #121212;
  color: #ffffff;
}

.text-royal { color: #7c4dff !important; }
.text-muted-light { color: #a0a0a0; }

/* UPDATED: Royal Indigo gradient for primary stat cards */
.bg-royal-grad { background: linear-gradient(135deg, #7c4dff, #6200ea) !important; }
.bg-card-dark { background-color: #1e1e1e !important; border: 1px solid #2c2c2c !important; }
.bg-success-dark { background-color: #1b5e20 !important; }
.bg-info-dark { background-color: #01579b !important; }

.stat-card {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 16px;
}
.stat-card:hover { transform: translateY(-8px); }

/* UPDATED: Detail cards with charcoal theme */
.detail-card {
  background: #1e1e1e;
  border: 1px solid #2c2c2c;
  border-radius: 16px;
}

.icon-box {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.25rem;
}

.bg-royal-soft { background-color: rgba(124, 77, 255, 0.15); }
.bg-royal { background-color: #7c4dff !important; color: white; }

.border-dark-muted { border-bottom: 1px solid #2c2c2c; }
.list-group-item:last-child { border-bottom: none; }
</style>