<template>
  <div class="container py-5">
    <div class="header-section mb-5 d-flex justify-content-between align-items-end">
      <div>
        <h1 class="fw-bold text-primary display-5">Recruitment Hub</h1>
        <p class="text-secondary mb-0" v-if="profile">Managing talent acquisition for <strong>{{ profile.company_name }}</strong></p>
      </div>
      <div class="action-buttons">
        <router-link to="/company/profile/edit" class="btn btn-outline-primary me-2 px-4 fw-bold">Edit Profile</router-link>
        <router-link to="/company/drives/create" class="btn btn-primary px-4 fw-bold shadow-sm">Launch New Drive</router-link>
      </div>
    </div>

    <div class="row g-4 mb-5" v-if="profile">
      <!-- Profile Insight Cards -->
      <div class="col-md-3">
        <div class="insight-card p-3 rounded-4 shadow-sm bg-white border h-100">
          <h6 class="text-uppercase small text-muted fw-bold mb-2">Industry</h6>
          <p class="h5 fw-bold mb-0 text-dark">{{ profile.industry || 'General' }}</p>
        </div>
      </div>
      <div class="col-md-3">
        <div class="insight-card p-3 rounded-4 shadow-sm bg-white border h-100">
          <h6 class="text-uppercase small text-muted fw-bold mb-2">Base Location</h6>
          <p class="h5 fw-bold mb-0 text-dark">{{ profile.location || 'Flexible' }}</p>
        </div>
      </div>
      <div class="col-md-3">
        <div class="insight-card p-3 rounded-4 shadow-sm bg-white border h-100">
          <h6 class="text-uppercase small text-muted fw-bold mb-2">HR Lead</h6>
          <p class="h5 fw-bold mb-0 text-dark">{{ profile.hr_contact || 'Pending' }}</p>
        </div>
      </div>
      <div class="col-md-3">
        <div class="insight-card p-3 rounded-4 shadow-sm border h-100" :class="profile.approval_status === 'approved' ? 'bg-success-soft' : 'bg-warning-soft'">
          <h6 class="text-uppercase small fw-bold mb-2" :class="profile.approval_status === 'approved' ? 'text-success' : 'text-warning'">Account Status</h6>
          <p class="h5 fw-bold mb-0" :class="profile.approval_status === 'approved' ? 'text-success' : 'text-warning text-dark'">{{ profile.approval_status.toUpperCase() }}</p>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
      <div class="card-header bg-white border-bottom py-4 px-4 overflow-hidden">
        <h4 class="mb-0 fw-bold text-dark">Active Placement Drives</h4>
      </div>
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center custom-table">
          <thead class="bg-light">
            <tr>
              <th class="ps-4 text-start">Position</th>
              <th>Status</th>
              <th>Applicants</th>
              <th>Deadline</th>
              <th class="pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td class="ps-4 text-start">
                <div class="fw-bold text-dark">{{ d.title }}</div>
                <div class="text-muted small">UID: #DRV-{{ d.id }}</div>
              </td>
              <td>
                <span :class="getStatusClass(d.status)" class="badge rounded-pill px-3 py-2">
                  {{ d.status.replace('_', ' ').toUpperCase() }}
                </span>
              </td>
              <td>
                <div class="d-flex align-items-center justify-content-center">
                   <div class="applicant-bubble bg-info-soft text-info fw-bold me-2">
                      {{ d.applicant_count }}
                   </div>
                   <span class="small text-muted">Candidates</span>
                </div>
              </td>
              <td class="text-muted small">{{ formatDate(d.deadline) }}</td>
              <td class="pe-4 text-nowrap">
                <router-link :to="`/company/drive/${d.id}/applicants`" class="btn btn-sm btn-action btn-outline-primary me-2">
                   Engagement
                </router-link>
                <router-link :to="`/company/drive/${d.id}/edit`" class="btn btn-sm btn-action btn-outline-dark me-2">
                   Update
                </router-link>
                <button @click="deleteDrive(d.id)" class="btn btn-sm btn-action btn-outline-danger">
                   Retract
                </button>
              </td>
            </tr>
            <tr v-if="drives.length === 0">
              <td colspan="5" class="py-5 text-center">
                <div class="empty-state py-4 text-muted">
                  <i class="bi bi-briefcase display-4 opacity-25"></i>
                  <p class="mt-3">Ready to hire? Launch your first placement drive now.</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-section { border-bottom: 2px solid #f8fafc; padding-bottom: 20px; }
.insight-card { transition: transform 0.2s; }
.insight-card:hover { transform: translateY(-5px); }

.bg-success-soft { background: #f0fdf4; }
.bg-warning-soft { background: #fffbeb; }
.bg-info-soft { background: #f0f9ff; }

.custom-table thead th {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 700;
  color: #64748b;
  padding: 16px;
}

.custom-table tbody td {
  padding: 20px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.applicant-bubble {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.btn-action {
  border-radius: 8px;
  font-weight: 600;
  padding: 6px 12px;
  transition: all 0.2s;
}

.btn-action:hover {
  transform: scale(1.05);
}
</style>

<script>
import API from "../../utils/api.js"

export default {
  data() {
    return {
      profile: null,
      drives: []
    }
  },
  async mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [profRes, driveRes] = await Promise.all([
          API.get("/company/profile"),
          API.get("/company/drives")
        ]);
        this.profile = profRes.data;
        this.drives = driveRes.data;
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      }
    },
    getStatusClass(status) {
      const map = { active: 'bg-success', 'pending_approval': 'bg-warning text-dark', 'rejected': 'bg-danger', 'closed': 'bg-secondary' };
      return map[status] || 'bg-light text-dark';
    },
    async deleteDrive(id) {
      if (confirm("Are you sure you want to delete this placement drive? This action cannot be undone.")) {
        try {
          await API.delete(`/company/drive/${id}/delete`);
          this.fetchData();
        } catch (err) {
          alert("Failed to delete drive");
        }
      }
    },
    formatDate(dateStr) {
      if (!dateStr || dateStr === 'None') return "No Deadline";
      return new Date(dateStr).toLocaleDateString();
    }
  }
}
</script>
