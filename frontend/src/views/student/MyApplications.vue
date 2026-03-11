<template>
  <div class="container py-4">
    <h2 class="text-primary fw-bold mb-4">My Job Applications</h2>
    
    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Applied On</th>
              <th>Status</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in apps" :key="a.id">
              <td><span class="fw-bold">{{ a.company }}</span></td>
              <td>{{ a.drive }}</td>
              <td>{{ formatDate(a.applied_date) }}</td>
              <td>
                <span :class="getStatusClass(a.status)" class="badge rounded-pill">
                  {{ formatStatus(a.status) }}
                </span>
              </td>
              <td class="text-center">
                <button class="btn btn-sm btn-outline-primary" @click="viewDetails(a)">View Details</button>
              </td>
            </tr>
            <tr v-if="apps.length === 0">
              <td colspan="5" class="text-center py-5 text-muted">
                <i class="bi bi-folder2-open display-4"></i>
                <p class="mt-2">No applications found. Start applying today!</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import API from "@/utils/api"

export default {
  data() {
    return { apps: [] };
  },
  async mounted() {
    const res = await API.get('/student/applications');
    this.apps = res.data;
  },
  methods: {
    getStatusClass(status) {
      const mapping = {
        'applied': 'bg-primary',
        'shortlisted': 'bg-info text-dark',
        'selected': 'bg-success',
        'rejected': 'bg-danger'
      };
      return mapping[status] || 'bg-secondary';
    },
    formatStatus(status) {
      return status.charAt(0).toUpperCase() + status.slice(1);
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString();
    },
    viewDetails(app) {
      alert(`Status Detail for ${app.drive}: ${this.formatStatus(app.status)}`);
    }
  }
};
</script>
<style scoped>
/* Main Container Colors */
.admin-table-container {
  background-color: #1e1e1e; /* Dark Charcoal Panel */
  border: 1px solid #2c2c2c;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 2rem;
}

/* Table Specific Styling */
.table-dark-custom {
  color: #f1f5f9;
  background-color: #1e1e1e !important;
  margin-bottom: 0;
}

/* Header - Matching Admin Slate Header */
.table-dark-custom thead th {
  background-color: #252525; /* Slightly lighter than charcoal */
  color: #7c4dff; /* Royal Indigo */
  border-bottom: 2px solid #2c2c2c;
  padding: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

/* Rows - Removing White Background */
.table-dark-custom td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid #2c2c2c;
  background-color: #1e1e1e;
  color: #e2e8f0;
}

/* Row Hover Effect */
.table-dark-custom tbody tr:hover td {
  background-color: rgba(124, 77, 255, 0.05); /* Very subtle Indigo tint */
}

/* Buttons and Tags within Table */
.text-success {
  color: #4ade80 !important; /* High contrast green for salary */
}

.eligibility-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(124, 77, 255, 0.1);
  color: #7c4dff;
  border: 1px solid rgba(124, 77, 255, 0.2);
}

/* Action Button Matching Login/Admin buttons */
.btn-apply {
  background: linear-gradient(135deg, #7c4dff, #6200ea);
  border: none;
  color: white;
  padding: 8px 20px;
  border-radius: 8px;
  font-weight: 700;
  transition: all 0.3s ease;
}

.btn-apply:disabled {
  background: #2c2c2c;
  color: #64748b;
  cursor: not-allowed;
}
</style>