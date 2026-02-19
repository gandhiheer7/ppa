<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div class="card shadow">
        <div class="card-body">
          <h3>Create Placement Drive</h3>
          <form @submit.prevent="submitDrive">
            <div class="mb-3">
              <label class="form-label">Job Title</label>
              <input v-model="form.job_title" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Job Description</label>
              <textarea v-model="form.job_description" class="form-control" rows="3" required></textarea>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Min CGPA</label>
                <input v-model="form.eligibility_cgpa" type="number" step="0.1" class="form-control" required />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Application Deadline</label>
                <input v-model="form.application_deadline" type="date" class="form-control" required />
              </div>
            </div>
            <button type="submit" class="btn btn-success w-100">Submit for Approval</button>
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
      form: {
        job_title: '',
        job_description: '',
        eligibility_cgpa: null,
        application_deadline: ''
      }
    };
  },
  methods: {
    async submitDrive() {
      try {
        await api.post('/company/drives', this.form);
        alert('Drive created and sent to Admin for approval.');
        this.$router.push('/company');
      } catch (err) {
        alert(err.response?.data?.msg || 'Failed to create drive');
      }
    }
  }
};
</script>