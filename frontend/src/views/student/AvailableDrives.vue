<template>
  <div class="container py-5">
    <div class="header-section mb-5">
      <h1 class="fw-bold text-primary display-5">Explore Career Opportunities</h1>
      <p class="text-secondary">Discover active placement drives and launch your career.</p>
      
      <div class="search-bar-container mt-4 p-3 bg-white rounded-3 shadow-sm d-flex gap-3 align-items-center">
        <i class="bi bi-search text-muted ms-2"></i>
        <input type="text" v-model="searchQuery" class="form-control border-0 shadow-none ps-0" placeholder="Search by company or role...">
        <div class="vr h-50 my-auto mx-1"></div>
        <select v-model="filterEligible" class="form-select border-0 shadow-none w-auto fw-bold text-muted">
          <option value="all">All Vacancies</option>
          <option value="eligible">Only Eligible</option>
        </select>
        <button @click="triggerExport" class="btn btn-primary px-4 fw-bold shadow-sm">
           Export History
        </button>
      </div>
    </div>

    <div class="row g-4">
      <div v-for="d in filteredDrives" :key="d.id" class="col-md-6 col-lg-4">
        <div class="card h-100 border-0 shadow-sm placement-card">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div class="company-tag px-3 py-1 rounded-pill bg-primary-soft text-primary small fw-bold">
                {{ d.company }}
              </div>
              <span v-if="d.is_eligible" class="text-success" title="You are eligible">
                <i class="bi bi-check-circle-fill"></i>
              </span>
            </div>
            
            <h4 class="card-title fw-bold mb-2">{{ d.title }}</h4>
            <div class="d-flex align-items-center text-muted small mb-4">
              <i class="bi bi-geo-alt me-1"></i> {{ d.location || 'Remote' }}
              <span class="mx-2">•</span>
              <i class="bi bi-currency-rupee me-1"></i> {{ d.salary }} LPA
            </div>

            <p v-if="d.description" class="card-text text-secondary small mb-4 line-clamp-3">
               {{ d.description }}
            </p>

            <div v-if="!d.is_eligible" class="eligibility-box error mb-4">
               <i class="bi bi-exclamation-triangle me-2"></i> {{ d.eligibility_reason }}
            </div>
            <div v-else class="eligibility-box success mb-4">
               <i class="bi bi-person-check me-2"></i> Eligible
            </div>

            <div class="d-flex justify-content-between align-items-center mt-auto">
              <div class="deadline small text-muted">
                <i class="bi bi-clock me-1"></i> {{ formatDate(d.deadline) }}
              </div>
              <button 
                @click="apply(d.id)" 
                class="btn btn-sm px-4 fw-bold rounded-3 transition-all" 
                :class="d.is_eligible ? 'btn-primary' : 'btn-light text-muted border'"
                :disabled="!d.is_eligible || d.status !== 'open'">
                {{ d.status === 'open' ? (d.is_eligible ? 'Apply Now' : 'Ineligible') : 'Closed' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredDrives.length === 0" class="col-12 text-center py-5">
         <div class="empty-state">
           <i class="bi bi-search display-3 text-muted opacity-25"></i>
           <p class="mt-3 text-secondary">No drives match your current criteria.</p>
         </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-section { max-width: 800px; }
.search-bar-container { transition: box-shadow 0.2s; }
.search-bar-container:focus-within { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important; }

.placement-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}
.placement-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
}

.bg-primary-soft { background-color: rgba(99, 102, 241, 0.1); }

.eligibility-box {
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 500;
}
.eligibility-box.success { background: #f0fdf4; color: #166534; }
.eligibility-box.error { background: #fef2f2; color: #991b1b; }

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}

.transition-all { transition: all 0.2s; }
</style>

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
    async triggerExport() {
      try {
        await API.post('/student/export-csv');
        alert("Export triggered! You will receive an email with the CSV file shortly.");
      } catch (err) {
        alert("Failed to trigger export.");
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
.header-section { max-width: 800px; }
.search-bar-container { transition: box-shadow 0.2s; }
.search-bar-container:focus-within { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important; }

.placement-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}
.placement-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
}

.bg-primary-soft { background-color: rgba(99, 102, 241, 0.1); }

.eligibility-box {
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 500;
}
.eligibility-box.success { background: #f0fdf4; color: #166534; }
.eligibility-box.error { background: #fef2f2; color: #991b1b; }

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}

.transition-all { transition: all 0.2s; }
</style>