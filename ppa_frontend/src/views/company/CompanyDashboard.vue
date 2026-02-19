<template>
  <div class="company-dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Company Dashboard</h2>
      <router-link to="/company/create-drive" class="btn btn-primary">Create New Drive</router-link>
    </div>

    <div class="card shadow">
      <div class="card-header bg-dark text-white">Your Placement Drives</div>
      <div class="card-body">
        <table class="table">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Applicants</th>
              <th>Status</th>
              <th>Deadline</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in drives" :key="drive.drive_id">
              <td>{{ drive.job_title }}</td>
              <td><span class="badge bg-secondary">{{ drive.applicant_count }}</span></td>
              <td>
                <span :class="['badge', drive.status === 'Approved' ? 'bg-success' : 'bg-warning']">
                  {{ drive.status }}
                </span>
              </td>
              <td>{{ new Date(drive.application_deadline).toLocaleDateString() }}</td>
              <td>
                <router-link :to="'/company/drive/' + drive.drive_id + '/applications'" class="btn btn-sm btn-outline-primary">
                  View Applicants
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      drives: []
    };
  },
  async created() {
    try {
      const res = await api.get('/company/drives');
      this.drives = res.data.drives;
    } catch (err) {
      console.error("Failed to load drives", err);
    }
  }
};
</script>