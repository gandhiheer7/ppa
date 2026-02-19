<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Placement Portal</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          
          <li class="nav-item" v-if="!token">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item" v-if="!token">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>

          <li class="nav-item" v-if="role === 'Admin'">
            <router-link class="nav-link" to="/admin">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Admin'">
            <router-link class="nav-link" to="/admin/users">Users</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Admin'">
            <router-link class="nav-link" to="/admin/reports">Reports</router-link>
          </li>

          <li class="nav-item" v-if="role === 'Company'">
            <router-link class="nav-link" to="/company">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Company'">
            <router-link class="nav-link" to="/company/create-drive">Create Drive</router-link>
          </li>

          <li class="nav-item" v-if="role === 'Student'">
            <router-link class="nav-link" to="/student">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Student'">
            <router-link class="nav-link" to="/student/my-applications">My Apps</router-link>
          </li>
          <li class="nav-item" v-if="role === 'Student'">
            <router-link class="nav-link" to="/student/profile">Profile</router-link>
          </li>

          <li class="nav-item" v-if="token">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      token: localStorage.getItem('token'),
      role: localStorage.getItem('role')
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      window.location.href = '/login';
    }
  }
};
</script>