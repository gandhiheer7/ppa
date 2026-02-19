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

    <div class="row mb-4">
      <div class="col-md-6 offset-md-3">
        <div class="card shadow">
          <div class="card-header">Statistics Overview</div>
          <div class="card-body">
            <Bar v-if="chartData.labels" :data="chartData" :options="chartOptions" />
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow mb-4">
      <div class="card-header bg-warning text-dark">Pending Placement Drives</div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Company</th>
              <th>Date Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in pendingDrives" :key="drive.drive_id">
              <td>{{ drive.job_title }}</td>
              <td>{{ drive.company_name || 'Unknown' }}</td>
              <td>{{ new Date().toLocaleDateString() }}</td>
              <td>
                <button @click="approveDrive(drive.drive_id)" class="btn btn-sm btn-success me-2">Approve</button>
                <button @click="rejectDrive(drive.drive_id)" class="btn btn-sm btn-danger">Reject</button>
              </td>
            </tr>
            <tr v-if="pendingDrives.length === 0">
              <td colspan="4" class="text-center text-muted">No pending drives.</td>
            </tr>
          </tbody>
        </table>
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
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  components: { Bar },
  data() {
    return {
      stats: { total_students: 0, total_companies: 0, total_placement_drives: 0 },
      pendingCompanies: [],
      pendingDrives: [],
      chartData: {},
      chartOptions: { responsive: true }
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
        
        // Chart Data
        this.chartData = {
          labels: ['Students', 'Companies', 'Drives'],
          datasets: [{
            label: 'Total Count',
            backgroundColor: '#42A5F5',
            data: [this.stats.total_students, this.stats.total_companies, this.stats.total_placement_drives]
          }]
        };

        // Fetch Companies
        const companyRes = await api.get('/admin/search/companies?q=');
        this.pendingCompanies = companyRes.data.companies.filter(c => {
          const status = c.approval_status || c.status;
          return status && status.toLowerCase() === 'pending';
        });

        // Fetch Drives (New)
        const driveRes = await api.get('/admin/search/drives?q=');
        // Filter locally for 'Pending' since the search returns all
        this.pendingDrives = driveRes.data.drives.filter(d => d.status === 'Pending');

      } catch (err) {
        console.error("Error fetching data", err);
      }
    },
    async approveCompany(id) {
      await api.post(`/admin/companies/${id}/approve`);
      this.fetchDashboardData();
    },
    async rejectCompany(id) {
      await api.post(`/admin/companies/${id}/reject`);
      this.fetchDashboardData();
    },
    async approveDrive(id) {
      await api.post(`/admin/drives/${id}/approve`);
      alert('Drive Approved');
      this.fetchDashboardData();
    },
    async rejectDrive(id) {
      await api.post(`/admin/drives/${id}/reject`);
      this.fetchDashboardData();
    }
  }
};
</script>