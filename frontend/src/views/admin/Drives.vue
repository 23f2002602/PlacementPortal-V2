<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-primary fw-bold">Placement Drives</h2>
      <button @click="fetchDrives" class="btn btn-outline-primary btn-sm">Refresh List</button>
    </div>

    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center">
          <thead class="table-dark">
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Package (LPA)</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td class="fw-bold">{{ d.company }}</td>
              <td>{{ d.job_title }}</td>
              <td><span class="text-success fw-bold">{{ d.package || 'TBD' }}</span></td>
              <td class="small text-muted">{{ formatDate(d.deadline) }}</td>
              <td>
                <span :class="statusClass(d.status)" class="badge">
                  {{ formatStatus(d.status) }}
                </span>
              </td>
              <td class="text-nowrap">
                <template v-if="d.status === 'pending_approval'">
                  <button @click="approve(d.id)" class="btn btn-sm btn-success me-1">Approve</button>
                  <button @click="reject(d.id)" class="btn btn-sm btn-danger me-1">Reject</button>
                </template>
                <button @click="viewDetails(d)" class="btn btn-sm btn-outline-info me-1">Details</button>
                <button @click="editDrive(d)" class="btn btn-sm btn-info me-1">Edit</button>
                <button @click="deleteDrive(d.id)" class="btn btn-sm btn-danger">Delete</button>
              </td>
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
    return { drives: [] };
  },
  async mounted() {
    this.fetchDrives();
  },
  methods: {
    async fetchDrives() {
      const res = await API.get("/admin/drives");
      this.drives = res.data;
    },
    async approve(id) {
      await API.put(`/admin/drive/${id}/approve`);
      this.fetchDrives();
    },
    async reject(id) {
      await API.put(`/admin/drive/${id}/reject`);
      this.fetchDrives();
    },
    viewDetails(d) {
      alert(`Job Title: ${d.job_title}\nCompany: ${d.company}\nStatus: ${this.formatStatus(d.status)}\nPackage: ${d.package || 'TBD'}`);
    },
    async editDrive(d) {
      const title = prompt("Job Title:", d.job_title);
      const pkg = prompt("Package (LPA):", d.package);
      if (title !== null && pkg !== null) {
        await API.put(`/admin/drive/${d.id}/update`, { job_title: title, package: pkg, status: d.status });
        this.fetchDrives();
      }
    },
    async deleteDrive(id) {
      if (confirm("Delete this placement drive?")) {
        await API.delete(`/admin/drive/${id}/delete`);
        this.fetchDrives();
      }
    },
    statusClass(status) {
      const map = { 'open': 'bg-success', 'pending_approval': 'bg-warning text-dark', 'rejected': 'bg-danger', 'closed': 'bg-secondary' };
      return map[status] || 'bg-light text-dark';
    },
    formatStatus(status) {
      return (status || '').replace('_', ' ').toUpperCase();
    },
    formatDate(dateStr) {
      if (!dateStr || dateStr === 'None') return "No Deadline";
      return new Date(dateStr).toLocaleDateString();
    }
  }
}
</script>