<template>
  <div class="row justify-content-center">
    <div class="col-md-4">
      <div class="card shadow mt-5">
        <div class="card-body">
          <h3 class="text-center mb-4">Login</h3>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </form>
          <p class="mt-3 text-center">
            Don't have an account? <router-link to="/register">Register here</router-link>
          </p>
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
      username: '',
      password: ''
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await api.post('/auth/login', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('role', response.data.role);
        
        // Redirect based on role
        if (response.data.role === 'Admin') this.$router.push('/admin');
        else if (response.data.role === 'Company') this.$router.push('/company');
        else this.$router.push('/student');
        
        // Force refresh for navbar update
        setTimeout(() => { window.location.reload(); }, 100);
      } catch (error) {
        alert(error.response?.data?.msg || 'Login failed');
      }
    }
  }
};
</script>