<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-primary fw-bold">Company Partners</h2>
      <div class="input-group w-50">
        <input type="text" class="form-control" placeholder="Search company..." v-model="searchQuery" @keyup.enter="search">
        <button class="btn btn-primary" @click="search">Search</button>
      </div>
    </div>

    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center">
          <thead class="table-dark">
            <tr>
              <th>Company Name</th>
              <th>Industry</th>
              <th>Location</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in companies" :key="c.id">
              <td class="fw-bold">{{ c.company_name }}</td>
              <td>{{ c.industry }}</td>
              <td>{{ c.location }}</td>
              <td>
                <span :class="c.is_blacklisted ? 'badge bg-danger' : statusClass(c.approval_status)" class="badge">
                  {{ c.is_blacklisted ? 'Blacklisted' : formatStatus(c.approval_status) }}
                </span>
              </td>
              <td class="text-nowrap">
                <template v-if="c.approval_status === 'pending'">
                  <button @click="approve(c.id)" class="btn btn-sm btn-success me-1">Approve</button>
                  <button @click="reject(c.id)" class="btn btn-sm btn-danger me-1">Reject</button>
                </template>
                <button @click="toggleBlacklist(c)" class="btn btn-sm me-1" :class="c.is_blacklisted ? 'btn-outline-success' : 'btn-outline-danger'">
  {{ c.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
</button>
                <button @click="editCompany(c)" class="btn btn-sm btn-info me-1">Edit</button>
                <button @click="deleteCompany(c.id)" class="btn btn-sm btn-danger">Delete</button>
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
    return {
      companies: [],
      searchQuery: ""
    }
  },
  async mounted() {
    this.fetchCompanies();
  },
  methods: {
    async fetchCompanies() {
      const res = await API.get("/admin/companies");
      this.companies = res.data;
    },
    async search() {
      const res = await API.get(`/admin/search?role=company&q=${this.searchQuery}`);
      this.companies = res.data;
    },
    async approve(id) {
      await API.put(`/admin/company/${id}/approve`);
      this.fetchCompanies();
    },
    async reject(id) {
      await API.put(`/admin/company/${id}/reject`);
      this.fetchCompanies();
    },
    async toggleBlacklist(c) {
      await API.put(`/admin/user/${c.user_id}/blacklist`);
      alert(`Blacklist status toggled for ${c.company_name}`);
      this.fetchCompanies();
    },
    async editCompany(c) {
      const name = prompt("Company Name:", c.company_name);
      const industry = prompt("Industry:", c.industry);
      const location = prompt("Location:", c.location);
      if (name !== null && industry !== null && location !== null) {
        await API.put(`/admin/company/${c.id}/update`, { company_name: name, industry, location });
        this.fetchCompanies();
      }
    },
    async deleteCompany(id) {
      if (confirm("Delete this company and its user account?")) {
        await API.delete(`/admin/company/${id}/delete`);
        this.fetchCompanies();
      }
    },
    statusClass(status) {
      return status === 'approved' ? 'bg-success' : (status === 'pending' ? 'bg-warning text-dark' : 'bg-danger');
    },
    formatStatus(status) {
      return status.charAt(0).toUpperCase() + status.slice(1);
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