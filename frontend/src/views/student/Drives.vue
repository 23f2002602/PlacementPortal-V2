<template>
  <div class="container-fluid py-4">
    <div class="header-section mb-4">
      <h1 class="fw-bold text-royal display-5">Placement Drives</h1>
      <p class="text-muted-light">Manage and track your recruitment journey.</p>
      
      <div class="search-bar-container mt-4 p-3 shadow-lg d-flex gap-3 align-items-center">
        <i class="bi bi-search text-muted ms-2"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          class="form-control search-input border-0 shadow-none" 
          placeholder="Search by company or role..."
        >
      </div>
    </div>

    <ul class="nav nav-pills mb-4 gap-2">
      <li class="nav-item" v-for="tab in ['available', 'upcoming', 'completed']" :key="tab">
        <button 
          class="nav-link text-capitalize" 
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </li>
    </ul>

    <div class="admin-table-container shadow-lg">
      <div class="table-responsive">
        <table class="table table-dark-custom align-middle mb-0">
          <thead>
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Package (LPA)</th>
              <th>Deadline</th>
              <th>Eligibility</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in filteredDrives" :key="d.id">
              <td><div class="fw-bold text-white">{{ d.company }}</div></td>
              <td class="text-muted-light">{{ d.title }}</td>
              <td><span class="text-success fw-bold">₹{{ d.salary }}</span></td>
              <td class="small text-muted-light">{{ formatDate(d.deadline) }}</td>
              <td>
                <span :class="d.is_eligible ? 'eligibility-tag success' : 'eligibility-tag error'">
                   {{ d.is_eligible ? 'Eligible' : 'Ineligible' }}
                </span>
              </td>
              <td class="text-center">
                <button 
                  v-if="activeTab === 'available'"
                  @click="apply(d.id)" 
                  class="btn-royal-sm" 
                  :disabled="!d.is_eligible || d.status !== 'active'">
                  {{ d.is_eligible ? 'Apply Now' : 'Locked' }}
                </button>
                <span v-else class="text-muted-light small text-uppercase fw-bold">{{ activeTab }}</span>
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
      activeTab: 'available',
      allDrives: [],
      searchQuery: ""
    };
  },
  computed: {
    filteredDrives() {
      const now = new Date();
      return this.allDrives.filter(d => {
        const deadline = new Date(d.deadline);
        const matchesSearch = d.company.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
                             d.title.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        let matchesTab = false;
        if (this.activeTab === 'available') matchesTab = d.status === 'active' && deadline >= now;
        if (this.activeTab === 'upcoming') matchesTab = d.status === 'pending_approval';
        if (this.activeTab === 'completed') matchesTab = d.status === 'closed' || deadline < now;
        
        return matchesSearch && matchesTab;
      });
    }
  },
  async mounted() {
    this.fetchDrives();
  },
  methods: {
    async fetchDrives() {
      const res = await API.get('/student/drives');
      this.allDrives = res.data;
    },
    async apply(id) {
      if(!confirm("Apply for this drive?")) return;
      try {
        await API.post(`/student/apply/${id}`);
        alert("Applied successfully!");
        this.fetchDrives();
      } catch (err) {
        alert(err.response?.data?.error || "Error applying");
      }
    },
    formatDate(dateStr) {
      if(!dateStr || dateStr === 'None') return "N/A";
      return new Date(dateStr).toLocaleDateString();
    }
  }
}
</script>

<style scoped>
/* Search Input Visibility */
.search-input { background-color: transparent !important; color: #ffffff !important; }
.search-input::placeholder { color: #64748b !important; }
.search-bar-container { background-color: #1e1e1e; border-radius: 12px; border: 1px solid #2c2c2c; }

/* Admin-style Table Colors */
.admin-table-container { background-color: #1e1e1e; border-radius: 16px; border: 1px solid #2c2c2c; overflow: hidden; }
.table-dark-custom thead th { 
  background-color: #252525; 
  color: #7c4dff; 
  padding: 1rem; 
  text-transform: uppercase; 
  font-size: 0.8rem; 
  border-bottom: 2px solid #2c2c2c;
}
.table-dark-custom td { padding: 1.25rem 1rem; border-bottom: 1px solid #2c2c2c; color: #f1f5f9; background-color: #1e1e1e; }

/* Buttons and Tags */
.btn-royal-sm { background: linear-gradient(135deg, #7c4dff, #6200ea); color: white; border: none; padding: 6px 16px; border-radius: 6px; font-weight: 600; }
.nav-pills .nav-link { color: #a0a0a0; background: #1e1e1e; border: 1px solid #2c2c2c; }
.nav-pills .nav-link.active { background: #7c4dff; color: white; }
.text-royal { color: #7c4dff !important; }
.text-muted-light { color: #a0a0a0; }
</style>