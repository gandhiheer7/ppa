<template>
  <div class="container my-applications">
    <div class="d-flex justify-content-between align-items-center mb-4 mt-3">
      <h2 class="h3 text-primary"><i class="bi bi-clock-history me-2"></i>Application History</h2>
      <button 
        @click="exportCSV" 
        class="btn btn-outline-dark btn-sm d-flex align-items-center"
        :disabled="exporting">
        <span v-if="exporting" class="spinner-border spinner-border-sm me-2"></span>
        {{ exporting ? 'Generating...' : 'Export to CSV' }}
      </button>
    </div>

    <div v-if="exports.length > 0" class="alert alert-info shadow-sm d-flex flex-column">
      <div class="d-flex align-items-center mb-2">
        <i class="bi bi-file-earmark-arrow-down-fill fs-4 me-2"></i>
        <strong>Your Reports are Ready:</strong>
      </div>
      <div class="d-flex flex-wrap gap-2">
        <a v-for="file in exports" 
           :key="file" 
           :href="getDownloadUrl(file)" 
           target="_blank" 
           class="btn btn-sm btn-light border text-primary">
           <i class="bi bi-download me-1"></i> {{ file }}
        </a>
      </div>
    </div>

    <div class="card shadow-sm border-0">
      <div class="card-header bg-white py-3">
        <h5 class="mb-0 text-secondary">My Applications</h5>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-secondary">
              <tr>
                <th class="ps-4">Job Role</th>
                <th>Company</th>
                <th>Date Applied</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.application_id">
                <td class="ps-4 fw-bold text-dark">{{ app.job_title }}</td>
                <td class="text-muted">{{ app.company_name || 'View Details' }}</td>
                <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
                <td>
                  <span :class="['badge rounded-pill px-3 py-2', getStatusClass(app.status)]">
                    {{ app.status }}
                  </span>
                </td>
              </tr>
              
              <tr v-if="applications.length === 0">
                <td colspan="4" class="text-center py-5 text-muted">
                  <i class="bi bi-inbox fs-1 d-block mb-3"></i>
                  You haven't applied to any drives yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      applications: [],
      exports: [],
      exporting: false
    };
  },
  async created() {
    this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const appRes = await api.get('/student/applications');
        this.applications = appRes.data.applications;
        
        // Fetch available exports
        const exportRes = await api.get('/student/exports');
        this.exports = exportRes.data.files;
      } catch(err) {
        console.error(err);
      }
    },
    async exportCSV() {
      this.exporting = true;
      try {
        await api.post('/student/export-history');
        alert('Export job triggered! Refresh page in a few seconds to see the download link.');
        // Auto-refresh the list after 5 seconds
        setTimeout(() => {
          this.loadData();
          this.exporting = false;
        }, 5000);
      } catch (err) {
        alert('Export failed');
        this.exporting = false;
      }
    },
    getDownloadUrl(filename) {
      return `http://localhost:5000/uploads/${filename}`;
    },
    getStatusClass(status) {
      switch(status) {
        case 'Selected': return 'bg-success';
        case 'Shortlisted': return 'bg-info text-dark';
        case 'Rejected': return 'bg-danger';
        case 'Applied': return 'bg-secondary';
        default: return 'bg-light text-dark border';
      }
    }
  }
};
</script>

<style scoped>
/* Optional: Add some spacing for better visual hierarchy */
.container {
  max-width: 1000px;
}
.card {
  border-radius: 10px;
  overflow: hidden; /* Ensures table corners follow card radius */
}
</style>