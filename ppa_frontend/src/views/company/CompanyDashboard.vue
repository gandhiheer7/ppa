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
                <router-link :to="'/company/drive/' + drive.drive_id + '/applications'" class="btn btn-sm btn-info me-2">
                  Applicants
                </router-link>
                
                <button v-if="drive.status === 'Pending'" @click="openEditModal(drive)" class="btn btn-sm btn-warning me-2">Edit</button>
                <button v-if="drive.status === 'Pending'" @click="deleteDrive(drive.drive_id)" class="btn btn-sm btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Drive</h5>
            <button @click="showModal = false" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateDrive">
              <div class="mb-2">
                <label>Job Title</label>
                <input v-model="editForm.job_title" class="form-control" required />
              </div>
              <div class="mb-2">
                <label>Deadline</label>
                <input v-model="editForm.application_deadline" type="date" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-primary w-100 mt-3">Save Changes</button>
            </form>
          </div>
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
      drives: [],
      showModal: false,
      editForm: { drive_id: null, job_title: '', application_deadline: '' }
    };
  },
  async created() {
    this.fetchDrives();
  },
  methods: {
    async fetchDrives() {
      try {
        const res = await api.get('/company/drives');
        this.drives = res.data.drives;
      } catch (err) {
        console.error(err);
      }
    },
    async deleteDrive(id) {
      if(!confirm("Are you sure?")) return;
      try {
        await api.delete(`/company/drives/${id}`);
        this.fetchDrives();
      } catch (err) {
        alert('Delete failed');
      }
    },
    openEditModal(drive) {
      this.editForm = { ...drive };
      // Format date for input field
      this.editForm.application_deadline = new Date(drive.application_deadline).toISOString().split('T')[0];
      this.showModal = true;
    },
    async updateDrive() {
      try {
        await api.put(`/company/drives/${this.editForm.drive_id}`, this.editForm);
        this.showModal = false;
        this.fetchDrives();
      } catch (err) {
        alert('Update failed');
      }
    }
  }
};
</script>