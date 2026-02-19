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
            <th>Resume</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.student_username }}</td>
            <td>{{ app.application_date ? new Date(app.application_date).toLocaleDateString() : 'N/A' }}</td>
            <td>
              <a v-if="app.resume_filename" 
                 :href="getResumeUrl(app.resume_filename)" 
                 target="_blank" 
                 class="btn btn-sm btn-info text-white">
                 View Resume
              </a>
              <span v-else class="text-muted small">No Resume</span>
            </td>
            <td>
              <span :class="getStatusClass(app.status)" class="badge">{{ app.status }}</span>
            </td>
            <td>
              <div v-if="app.status === 'Applied'" class="btn-group">
                <button @click="shortlist(app.application_id)" class="btn btn-sm btn-primary">Shortlist</button>
              </div>
              <div v-else-if="app.status === 'Shortlisted'" class="btn-group">
                <button @click="updateStatus(app.application_id, 'Selected')" class="btn btn-sm btn-success">Select</button>
                <button @click="updateStatus(app.application_id, 'Rejected')" class="btn btn-sm btn-danger">Reject</button>
              </div>
              <div v-else-if="app.status === 'Selected'">
                <button @click="generateOffer(app.application_id)" class="btn btn-sm btn-warning text-dark">Offer Letter</button>
              </div>
              <div v-else class="text-muted small">
                Closed
              </div>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="5" class="text-center">No applications received yet.</td>
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
    getResumeUrl(filename) {
      // Points to the static route we added in backend/app.py
      return `http://localhost:5000/uploads/${filename}`;
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
    async generateOffer(appId) {
      try {
        const res = await api.get(`/company/applications/${appId}/offer-letter`);
        // Simple download trigger
        const blob = new Blob([res.data.offer_letter], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `Offer_Letter_${appId}.txt`;
        link.click();
      } catch (err) {
        alert('Failed to generate offer letter');
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