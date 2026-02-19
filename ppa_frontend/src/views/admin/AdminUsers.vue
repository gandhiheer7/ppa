<template>
  <div class="admin-users">
    <h3>User Management</h3>
    
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <select v-model="userType" class="form-select" style="max-width: 150px;">
            <option value="students">Students</option>
            <option value="companies">Companies</option>
          </select>
          <input v-model="query" type="text" class="form-control" placeholder="Search by name..." @input="handleSearch">
        </div>
      </div>
    </div>

    <table class="table table-bordered">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Name/Username</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.user_id || user.company_id">
          <td>{{ user.user_id || user.company_id }}</td>
          <td>{{ user.username || user.company_name }}</td>
          <td>
            <span :class="['badge', user.blacklisted ? 'bg-danger' : 'bg-success']">
              {{ user.blacklisted ? 'Blacklisted' : 'Active' }}
            </span>
          </td>
          <td>
            <button v-if="!user.blacklisted" @click="toggleBlacklist(user.user_id || user.user_id, 'blacklist')" class="btn btn-sm btn-outline-danger">
              Blacklist
            </button>
            <button v-else @click="toggleBlacklist(user.user_id || user.user_id, 'reactivate')" class="btn btn-sm btn-outline-success">
              Reactivate
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '../../services/api';

export default {
  data() {
    return {
      userType: 'students',
      query: '',
      users: []
    };
  },
  watch: {
    userType() { this.handleSearch(); }
  },
  mounted() {
    this.handleSearch();
  },
  methods: {
    async handleSearch() {
      try {
        const endpoint = this.userType === 'students' ? '/admin/search/students' : '/admin/search/companies';
        const res = await api.get(`${endpoint}?q=${this.query}`);
        this.users = this.userType === 'students' ? res.data.students : res.data.companies;
      } catch (err) {
        console.error(err);
      }
    },
    async toggleBlacklist(userId, action) {
      if (!confirm(`Are you sure you want to ${action} this user?`)) return;
      try {
        await api.post(`/admin/users/${userId}/${action}`);
        this.handleSearch(); // Refresh list
      } catch (err) {
        alert('Action failed');
      }
    }
  }
};
</script>