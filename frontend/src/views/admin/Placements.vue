<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-primary fw-bold">Placements History</h2>
      <button @click="fetchPlacements" class="btn btn-outline-primary btn-sm">Refresh</button>
    </div>

    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Student</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Package (LPA)</th>
              <th>Placed On</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in placements" :key="p.id">
              <td>#{{ p.id }}</td>
              <td class="fw-bold">{{ p.student }}</td>
              <td><span class="badge bg-light text-dark border">{{ p.company }}</span></td>
              <td>{{ p.job_title }}</td>
              <td><span class="text-success fw-bold">{{ p.package || 'N/A' }}</span></td>
              <td class="text-muted small">{{ formatDate(p.placed_on) }}</td>
              <td>
                <button @click="editPlacement(p)" class="btn btn-sm btn-info me-1">Edit</button>
                <button @click="deletePlacement(p.id)" class="btn btn-sm btn-danger">Delete</button>
              </td>
            </tr>
            <tr v-if="placements.length === 0">
              <td colspan="6" class="text-center py-5 text-muted">No placement records found.</td>
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
    return { placements: [] };
  },
  async mounted() {
    this.fetchPlacements();
  },
  methods: {
    async fetchPlacements() {
      const res = await API.get("/admin/placements");
      this.placements = res.data;
    },
    async editPlacement(p) {
      const title = prompt("Job Title:", p.job_title);
      const pkg = prompt("Package (LPA):", p.package);
      if (title !== null && pkg !== null) {
        await API.put(`/admin/placement/${p.id}/update`, { job_title: title, salary: pkg });
        this.fetchPlacements();
      }
    },
    async deletePlacement(id) {
      if (confirm("Delete this placement record?")) {
        await API.delete(`/admin/placement/${id}/delete`);
        this.fetchPlacements();
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      return new Date(dateStr).toLocaleDateString();
    }
  }
}
</script>