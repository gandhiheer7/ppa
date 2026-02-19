<template>
  <div class="drive-applications">
    <h3>Manage Applications</h3>
    <router-link to="/company" class="btn btn-outline-secondary mb-3">Back to Dashboard</router-link>

    <div class="table-responsive shadow-sm">
      <table class="table table-hover">
        <thead class="table-light">
          <tr>
            <th>Student Name</th>
            <th>Applied Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.student_username }}</td>
            <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
            <td>
              <span :class="getStatusClass(app.status)" class="badge">{{ app.status }}</span>
            </td>
            <td>
              <div v-if="app.status === 'Applied'">
                <button @click="shortlist(app.application_id)" class="btn btn-sm btn-primary">Shortlist</button>
              </div>
              <div v-else-if="app.status === 'Shortlisted'">
                <button @click="updateStatus(app.application_id, 'Selected')" class="btn btn-sm btn-success me-1">Select</button>
                <button @click="updateStatus(app.application_id, 'Rejected')" class="btn btn-sm btn-danger">Reject</button>
              </div>
              <div v-else class="text-muted small">
                No actions available
              </div>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="4" class="text-center">No applications received yet.</td>
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
    this.loadApps();
  },
  methods: {
    async loadApps() {
      try {
        const driveId = this.$route.params.drive_id;
        const res = await api.get(`/company/drives/${driveId}/applications`);
        this.applications = res.data.applications;
      } catch (err) {
        alert('Failed to load applications');
      }
    },
    async shortlist(appId) {
      try {
        await api.post(`/company/applications/${appId}/shortlist`);
        this.loadApps();
      } catch (err) {
        alert(err.response?.data?.msg || 'Action failed');
      }
    },
    async updateStatus(appId, status) {
      try {
        await api.put(`/company/applications/${appId}/status`, { status });
        this.loadApps();
      } catch (err) {
        alert('Update failed');
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