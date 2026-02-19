<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card shadow">
        <div class="card-body">
          <h3>My Profile</h3>
          <form @submit.prevent="uploadResume">
            <div class="mb-3">
              <label class="form-label">Upload Resume (PDF/Docx)</label>
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
      file: null,
      uploading: false
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async uploadResume() {
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