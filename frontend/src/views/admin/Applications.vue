<template>
  <div class="container py-4">
    <h2 class="text-primary fw-bold mb-4">All Applications</h2>
    
    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Company</th>
              <th>Drive</th>
              <th>Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in apps" :key="a.id">
              <td>#{{ a.id }}</td>
              <td class="fw-bold">{{ a.student }}</td>
              <td><span class="badge bg-light text-dark border">{{ a.company }}</span></td>
              <td>{{ a.drive }}</td>
              <td class="text-muted small">{{ a.applied_date }}</td>
              <td>
                <span :class="getStatusClass(a.status)" class="badge rounded-pill">
                  {{ a.status.toUpperCase() }}
                </span>
              </td>
              <td>
                <button @click="deleteApp(a.id)" class="btn btn-sm btn-outline-danger">Delete</button>
              </td>
            </tr>
            <tr v-if="apps.length === 0">
              <td colspan="7" class="text-center py-5 text-muted">No applications found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import API from "../../utils/api.js"

export default {
  data() {
    return { apps: [] };
  },
  async mounted() {
    this.fetchApps();
  },
  methods: {
    async fetchApps() {
      const res = await API.get("/admin/applications");
      this.apps = res.data;
    },
    async deleteApp(id) {
      if (confirm("Delete this application record?")) {
        await API.delete(`/admin/application/${id}/delete`); // We'll add this endpoint too
        this.fetchApps();
      }
    },
    getStatusClass(status) {
      const map = { 'applied': 'bg-primary', 'selected': 'bg-success', 'rejected': 'bg-danger' };
      return map[status] || 'bg-secondary';
    }
  }
}
</script>
