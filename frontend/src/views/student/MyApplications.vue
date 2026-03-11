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