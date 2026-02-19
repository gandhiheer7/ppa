<template>
  <div class="admin-dashboard">
    <h2 class="mb-4">Admin Dashboard</h2>

    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card bg-primary text-white shadow">
          <div class="card-body text-center">
            <h5>Total Students</h5>
            <h2>{{ stats.total_students }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-success text-white shadow">
          <div class="card-body text-center">
            <h5>Total Companies</h5>
            <h2>{{ stats.total_companies }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white shadow">
          <div class="card-body text-center">
            <h5>Placement Drives</h5>
            <h2>{{ stats.total_placement_drives }}</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow mb-4">
      <div class="card-header bg-dark text-white">Pending Company Registrations</div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>HR Contact</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in pendingCompanies" :key="company.id">
              <td>{{ company.company_name }}</td>
              <td>{{ company.hr_contact }}</td>
              <td>
                <button @click="approveCompany(company.id)" class="btn btn-sm btn-success me-2">Approve</button>
                <button @click="rejectCompany(company.id)" class="btn btn-sm btn-danger">Reject</button>
              </td>
            </tr>
            <tr v-if="pendingCompanies.length === 0">
              <td colspan="3" class="text-center text-muted">No pending company registrations.</td>
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
      stats: {
        total_students: 0,
        total_companies: 0,
        total_placement_drives: 0
      },
      pendingCompanies: []
    };
  },
  async created() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      try {
        const statsRes = await api.get('/admin/dashboard');
        this.stats = statsRes.data;
        
        // Fetch all companies
        const companyRes = await api.get('/admin/search/companies?q=');
        
        // DEBUG: Print the raw data to the browser console (Press F12 to see it)
        console.log("All Companies Data:", companyRes.data.companies);

        // Robust Filter: Checks for 'approval_status' OR 'status', and ignores case (Pending/pending)
        this.pendingCompanies = companyRes.data.companies.filter(c => {
          const status = c.approval_status || c.status; // Check both possible names
          return status && status.toLowerCase() === 'pending';
        });

      } catch (err) {
        console.error("Error fetching data", err);
      }
    },
    async approveCompany(id) {
      try {
        await api.post(`/admin/companies/${id}/approve`); // [cite: 88]
        alert('Company Approved');
        this.fetchDashboardData();
      } catch (err) {
        alert('Action failed');
      }
    },
    async rejectCompany(id) {
      try {
        await api.post(`/admin/companies/${id}/reject`); // [cite: 88]
        alert('Company Rejected');
        this.fetchDashboardData();
      } catch (err) {
        alert('Action failed');
      }
    }
  }
};
</script>