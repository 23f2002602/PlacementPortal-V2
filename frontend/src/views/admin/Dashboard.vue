<template>
  <div class="container py-5">
    <div class="header-section mb-5">
      <h1 class="fw-bold text-primary display-5">Admin Overview</h1>
      <p class="text-secondary">Track institutional placement progress and management.</p>
    </div>
    
    <div class="row g-4 mb-5">
      <!-- Core Counts -->
      <div v-for="(stat, key) in primaryStats" :key="key" class="col-md-3">
        <div class="card border-0 shadow-sm h-100 stat-card" :class="'bg-' + stat.color">
          <div class="card-body p-4 text-white">
            <h6 class="text-uppercase small fw-bold opacity-75 mb-3">{{ stat.label }}</h6>
            <h2 class="display-5 fw-bold mb-0">{{ stat.value }}</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <!-- Detail Breakdowns -->
      <div class="col-md-6">
        <div class="card border-0 shadow-sm h-100 detail-card">
          <div class="card-body p-4">
            <div class="d-flex align-items-center mb-4">
              <div class="icon-box bg-success-soft text-success me-3">
                <i class="bi bi-building"></i>
              </div>
              <h5 class="card-title fw-bold mb-0">Company Pipeline</h5>
            </div>
            <div class="list-group list-group-flush">
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                <span class="text-secondary">Approved Partners</span>
                <span class="badge bg-success rounded-pill px-3">{{ stats.approved_companies }}</span>
              </div>
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                <span class="text-secondary">Pending Review</span>
                <span class="badge bg-warning text-dark rounded-pill px-3">{{ stats.pending_companies }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card border-0 shadow-sm h-100 detail-card">
          <div class="card-body p-4">
            <div class="d-flex align-items-center mb-4">
              <div class="icon-box bg-primary-soft text-primary me-3">
                <i class="bi bi-briefcase"></i>
              </div>
              <h5 class="card-title fw-bold mb-0">Placement Progress</h5>
            </div>
            <div class="list-group list-group-flush">
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                <span class="text-secondary">Total Job Applications</span>
                <span class="badge bg-primary rounded-pill px-3">{{ stats.total_applications }}</span>
              </div>
              <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0">
                <span class="text-secondary">Confirmed Selections</span>
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
        { label: 'Total Students', value: this.stats.total_students, color: 'primary' },
        { label: 'Selections', value: this.stats.selected_count, color: 'success' },
        { label: 'Total Companies', value: this.stats.total_companies, color: 'dark' },
        { label: 'Active Drives', value: this.stats.total_drives, color: 'info' }
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
.container {
  max-width: 1200px;
}
.stat-card {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.stat-card:hover {
  transform: translateY(-8px);
}
.detail-card {
  border: 1px solid rgba(226, 232, 240, 0.8);
  background: white;
}
.icon-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}
.bg-primary-soft { background-color: rgba(99, 102, 241, 0.1); }
.bg-success-soft { background-color: rgba(34, 197, 94, 0.1); }
.list-group-item { border-bottom-style: dashed; }
.list-group-item:last-child { border-bottom: none; }
</style>