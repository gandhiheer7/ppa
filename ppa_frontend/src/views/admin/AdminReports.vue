<template>
  <div class="admin-reports">
    <h3>Placement Reports & Statistics</h3>
    
    <div class="alert alert-info mt-3">
      <strong>Note:</strong> Detailed monthly reports are automatically emailed to the admin on the 1st of every month via the backend scheduler.
    </div>

    <div class="card mt-4 shadow-sm">
      <div class="card-header bg-secondary text-white">System Overview</div>
      <div class="card-body">
        <ul class="list-group list-group-flush">
          <li class="list-group-item d-flex justify-content-between align-items-center">
            Total Students Registered
            <span class="badge bg-primary rounded-pill">{{ stats.total_students }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            Total Companies Registered
            <span class="badge bg-primary rounded-pill">{{ stats.total_companies }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            Total Placement Drives
            <span class="badge bg-primary rounded-pill">{{ stats.total_placement_drives }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      stats: {}
    };
  },
  async created() {
    const res = await api.get('/admin/dashboard');
    this.stats = res.data;
  }
};
</script>