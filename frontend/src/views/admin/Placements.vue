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

<style scoped>
/* UPDATED: Container for tables now uses the Charcoal panel color */
.admin-table-container {
  background-color: #1e1e1e; /* Card/Panel Dark */
  border-radius: 12px;
  border: 1px solid #2c2c2c;
  overflow: hidden;
  margin-top: 20px;
}

/* UPDATED: Table body and text colors */
.table { 
  color: #f1f5f9; 
  margin-bottom: 0;
  background-color: #1e1e1e !important;
}

/* UPDATED: Table Header - Removed white/light background */
.table thead th {
  background-color: #252525; /* Slightly lighter than charcoal for depth */
  color: #7c4dff; /* Royal Indigo */
  border-bottom: 2px solid #2c2c2c;
  text-transform: uppercase;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  padding: 15px;
}

/* UPDATED: Table Rows - Removed white background and borders */
.table td {
  padding: 15px;
  border-bottom: 1px solid #2c2c2c;
  background-color: #1e1e1e;
  vertical-align: middle;
  color: #e2e8f0;
}

/* UPDATED: Hover effect for rows */
.table tbody tr:hover td {
  background-color: rgba(124, 77, 255, 0.05); /* Subtle Royal Indigo tint */
}

/* UPDATED: Action buttons within tables */
.btn-action {
  background: rgba(124, 77, 255, 0.1);
  color: #7c4dff;
  border: 1px solid rgba(124, 77, 255, 0.2);
  transition: all 0.2s;
}

.btn-action:hover {
  background: #7c4dff;
  color: white;
}

/* UPDATED: Status badges within tables */
.status-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}
</style>