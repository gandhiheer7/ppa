<template>
  <div class="my-applications">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Application History</h2>
      <button @click="exportCSV" class="btn btn-outline-dark">Export to CSV</button>
    </div>

    <div class="table-responsive">
      <table class="table table-striped card shadow-sm">
        <thead class="table-dark">
          <tr>
            <th>Drive</th>
            <th>Date Applied</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.job_title }}</td>
            <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
            <td>
              <span :class="['badge', getStatusClass(app.status)]">{{ app.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      applications: []
    };
  },
  async created() {
    const res = await api.get('/student/applications');
    this.applications = res.data.applications;
  },
  methods: {
    async exportCSV() {
      try {
        await api.post('/student/export-history');
        alert('Export job triggered! Check your terminal/logs for the alert.');
      } catch (err) {
        alert('Export failed');
      }
    },
    getStatusClass(status) {
      if (status === 'Selected') return 'bg-success';
      if (status === 'Rejected') return 'bg-danger';
      if (status === 'Shortlisted') return 'bg-info';
      return 'bg-secondary';
    }
  }
};
</script>