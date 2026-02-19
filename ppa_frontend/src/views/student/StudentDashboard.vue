<template>
  <div class="student-dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Available Placement Drives</h2>
      <div class="w-50">
        <input v-model="searchQuery" type="text" class="form-control" placeholder="Search by Job Title..." @input="fetchDrives" />
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-4" v-for="drive in drives" :key="drive.drive_id">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title text-primary">{{ drive.job_title }}</h5>
            <p class="card-text text-truncate">{{ drive.job_description }}</p>
            <ul class="list-unstyled small">
              <li><strong>Min CGPA:</strong> {{ drive.eligibility_cgpa }}</li>
              <li><strong>Branch:</strong> {{ drive.eligibility_branch || 'All' }}</li>
              <li><strong>Deadline:</strong> {{ new Date(drive.application_deadline).toLocaleDateString() }}</li>
            </ul>
            <button @click="apply(drive.drive_id)" class="btn btn-success w-100">Apply Now</button>
          </div>
        </div>
      </div>
      <div v-if="drives.length === 0" class="text-center mt-5 text-muted">
        No approved drives found matching your criteria.
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      drives: [],
      searchQuery: ''
    };
  },
  async created() {
    this.fetchDrives();
  },
  methods: {
    async fetchDrives() {
      try {
        const res = await api.get(`/student/drives?q=${this.searchQuery}`);
        this.drives = res.data.drives;
      } catch (err) {
        console.error("Error loading drives", err);
      }
    },
    async apply(id) {
      try {
        await api.post(`/student/drives/${id}/apply`);
        alert('Application submitted successfully!');
      } catch (err) {
        alert(err.response?.data?.msg || 'Eligibility criteria not met or already applied');
      }
    }
  }
};
</script>