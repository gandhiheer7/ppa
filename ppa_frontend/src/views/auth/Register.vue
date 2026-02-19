<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card shadow mt-4">
        <div class="card-body">
          <h3 class="text-center mb-4">Register</h3>
          
          <div class="btn-group w-100 mb-4">
            <button @click="role = 'Student'" :class="['btn', role === 'Student' ? 'btn-primary' : 'btn-outline-primary']">Student</button>
            <button @click="role = 'Company'" :class="['btn', role === 'Company' ? 'btn-primary' : 'btn-outline-primary']">Company</button>
          </div>

          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="form.username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>

            <div v-if="role === 'Student'">
              <div class="mb-3">
                <label class="form-label">Branch</label>
                <input v-model="form.branch" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">CGPA</label>
                <input v-model="form.cgpa" type="number" step="0.01" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Passing Year</label>
                <input v-model="form.passing_year" type="number" class="form-control" required />
              </div>
            </div>

            <div v-if="role === 'Company'">
              <div class="mb-3">
                <label class="form-label">Company Name</label>
                <input v-model="form.company_name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">HR Contact</label>
                <input v-model="form.hr_contact" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Website</label>
                <input v-model="form.website" type="url" class="form-control" />
              </div>
            </div>

            <button type="submit" class="btn btn-success w-100">Register</button>
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
      role: 'Student',
      form: {
        username: '', password: '', branch: '', cgpa: null, 
        passing_year: null, company_name: '', hr_contact: '', website: ''
      }
    };
  },
  methods: {
    async handleRegister() {
      const endpoint = this.role === 'Student' ? '/auth/register/student' : '/auth/register/company';
      try {
        await api.post(endpoint, this.form);
        alert('Registration successful! Please login.');
        this.$router.push('/login');
      } catch (error) {
        alert(error.response?.data?.msg || 'Registration failed');
      }
    }
  }
};
</script>