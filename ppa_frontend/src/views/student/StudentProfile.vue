<template>
  <div class="row justify-content-center">
    <div class="col-md-5 mb-4">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3>Edit Profile</h3>
          <form @submit.prevent="updateProfile">
            <div class="mb-3">
              <label class="form-label">Branch</label>
              <input v-model="profile.branch" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">CGPA</label>
              <input v-model="profile.cgpa" type="number" step="0.01" min="0" max="10" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Passing Year</label>
              <input v-model="profile.passing_year" type="number" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-success w-100">Save Changes</button>
          </form>
        </div>
      </div>
    </div>

    <div class="col-md-5 mb-4">
      <div class="card shadow h-100">
        <div class="card-body">
          <h3>Upload Resume</h3>
          <form @submit.prevent="uploadResume">
            <div class="mb-3">
              <label class="form-label">Select File (PDF/Docx)</label>
              <input type="file" @change="handleFileUpload" class="form-control" accept=".pdf,.docx" required />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="uploading">
              {{ uploading ? 'Uploading...' : 'Update Resume' }}
            </button>
          </form>
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
      profile: {
        branch: '',
        cgpa: null,
        passing_year: null
      },
      file: null,
      uploading: false
    };
  },
  async created() {
    // We assume there's a route to get current profile info or we infer from stored data
    // For now, we leave fields blank for user to input new values if endpoints require it
    // Or simpler: Just allow overwriting
  },
  methods: {
    async updateProfile() {
      try {
        await api.put('/student/profile', this.profile);
        alert('Profile updated successfully!');
      } catch (err) {
        alert('Update failed');
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async uploadResume() {
      if (!this.file) return;
      const formData = new FormData();
      formData.append('resume', this.file);
      this.uploading = true;
      try {
        await api.post('/student/profile/resume', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        alert('Resume uploaded successfully!');
      } catch (err) {
        alert('Upload failed');
      } finally {
        this.uploading = false;
      }
    }
  }
};
</script>