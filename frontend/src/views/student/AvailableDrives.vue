<template>
  <div class="container-fluid py-4">
    <div class="header-section mb-5">
      <h1 class="fw-bold text-royal display-5">Explore Opportunities</h1>
      <p class="text-muted-light">Find and apply to the latest placement drives available for you.</p>
      
      <div class="search-bar-container mt-4 p-3 shadow-lg d-flex gap-3 align-items-center">
        <i class="bi bi-search text-muted ms-2"></i>
        <input type="text" v-model="searchQuery" class="form-control bg-transparent border-0 shadow-none text-white" placeholder="Search by company or role...">
        <div class="vr h-50 my-auto mx-1 border-muted"></div>
        <select v-model="filterEligible" class="form-select bg-transparent border-0 shadow-none w-auto fw-bold text-muted">
          <option value="all">All Vacancies</option>
          <option value="eligible">Only Eligible</option>
        </select>
      </div>
    </div>

    <div class="admin-table-container shadow-lg">
      <div class="table-responsive">
        <table class="table table-dark-custom align-middle mb-0">
          <thead>
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Package (LPA)</th>
              <th>Location</th>
              <th>Deadline</th>
              <th>Status</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in filteredDrives" :key="d.id">
              <td>
                <div class="fw-bold text-white">{{ d.company }}</div>
              </td>
              <td class="text-muted-light">{{ d.title }}</td>
              <td>
                <span class="text-success fw-bold">₹{{ d.salary }}</span>
              </td>
              <td class="text-muted-light">{{ d.location || 'Remote' }}</td>
              <td class="small text-muted-light">
                <i class="bi bi-clock me-1"></i> {{ formatDate(d.deadline) }}
              </td>
              <td>
                <div v-if="!d.is_eligible" class="eligibility-tag error" :title="d.eligibility_reason">
                   Ineligible
                </div>
                <div v-else class="eligibility-tag success">
                   Eligible
                </div>
              </td>
              <td class="text-center">
                <button 
                  @click="apply(d.id)" 
                  class="btn-apply" 
                  :disabled="!d.is_eligible || d.status !== active">
                  {{ d.status === active ? (d.is_eligible ? 'Apply Now' : 'Locked') : 'Closed' }}
                </button>
              </td>
            </tr>
            <tr v-if="filteredDrives.length === 0">
              <td colspan="7" class="text-center py-5 text-muted-light">
                <i class="bi bi-search display-4 d-block mb-3 opacity-25"></i>
                No drives match your current criteria.
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
      drives: [],
      searchQuery: "",
      filterEligible: "all"
    };
  },
  computed: {
  filteredDrives() {
     return this.drives.filter(d => {
        const compMatch = (d.company || '').toLowerCase().includes(this.searchQuery.toLowerCase());
        const titleMatch = (d.title || '').toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesSearch = compMatch || titleMatch;
        
        // If 'all' is selected, show everything. If 'eligible' is selected, filter.
        const matchesFilter = this.filterEligible === 'all' || d.is_eligible;
        return matchesSearch && matchesFilter;
     });
  }
},
  async mounted() {
    this.fetchDrives();
  },
  methods: {
    async fetchDrives() {
      const res = await API.get('/student/drives');
      this.drives = res.data;
    },
    async apply(id) {
      if(!confirm("Are you sure you want to apply?")) return;
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
};
</script>

<style scoped>
.search-bar-container {
  background-color: #1e1e1e !important; /* Force dark background */
  border: 1px solid #2c2c2c;
  border-radius: 12px;
}

.search-bar-container input {
  color: #ffffff !important; /* Force text to be white */
  background-color: transparent !important;
  font-size: 1rem;
}

.search-bar-container input::placeholder {
  color: #a0a0a0; /* Lighter grey for placeholder */
}

/* Ensure the select dropdown text is also visible */
.search-bar-container select {
  color: #ffffff !important;
  background-color: #1e1e1e !important;
}

/* Main Container - Removes White Background */
.admin-table-container {
  background-color: #1e1e1e; /* Dark Charcoal */
  border: 1px solid #2c2c2c;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 2rem;
}

/* Table Body - Dark Styling */
.table-dark-custom {
  color: #f1f5f9;
  background-color: #1e1e1e !important;
  margin-bottom: 0;
}

/* Header Styling - Matches Admin Side */
.table-dark-custom thead th {
  background-color: #252525; /* Dark Slate Header */
  color: #7c4dff; /* Royal Indigo Text */
  border-bottom: 2px solid #2c2c2c;
  padding: 1.1rem 1rem;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}

/* Row Styling */
.table-dark-custom td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid #2c2c2c;
  background-color: #1e1e1e;
  color: #e2e8f0;
}

/* Hover Effect */
.table-dark-custom tbody tr:hover td {
  background-color: rgba(124, 77, 255, 0.05); 
}

/* Custom Badges */
.badge-eligible {
  background: rgba(74, 222, 128, 0.1);
  color: #4ade80;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
}

.badge-ineligible {
  background: rgba(248, 113, 113, 0.1);
  color: #f87171;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
}

/* Button Styling */
.btn-apply {
  background: linear-gradient(135deg, #7c4dff, #6200ea);
  border: none;
  color: white;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 700;
  transition: 0.3s;
}

.btn-apply:disabled {
  background: #2c2c2c;
  color: #64748b;
  cursor: not-allowed;
}

.text-muted-light { color: #94a3b8; }
.text-success { color: #4ade80 !important; }
</style>
