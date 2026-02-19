import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'

// Import Admin Views
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminUsers from '../views/admin/AdminUsers.vue'
import AdminReports from '../views/admin/AdminReports.vue'

// Import Company Views
import CompanyDashboard from '../views/company/CompanyDashboard.vue'
import CreateDrive from '../views/company/CreateDrive.vue'
import DriveApplications from '../views/company/DriveApplications.vue'

// Import Student Views
import StudentDashboard from '../views/student/StudentDashboard.vue'
import StudentProfile from '../views/student/StudentProfile.vue'
import MyApplications from '../views/student/MyApplications.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    
    // Admin Routes
    { 
      path: '/admin', 
      component: AdminDashboard, 
      meta: { requiresAuth: true, role: 'Admin' } 
    },
    { 
      path: '/admin/users', 
      component: AdminUsers, 
      meta: { requiresAuth: true, role: 'Admin' } 
    },
    { 
      path: '/admin/reports', 
      component: AdminReports, 
      meta: { requiresAuth: true, role: 'Admin' } 
    },

    // Company Routes
    { 
      path: '/company', 
      component: CompanyDashboard, 
      meta: { requiresAuth: true, role: 'Company' } 
    },
    { 
      path: '/company/create-drive', 
      component: CreateDrive, 
      meta: { requiresAuth: true, role: 'Company' } 
    },
    { 
      path: '/company/drive/:drive_id/applications', 
      component: DriveApplications, 
      meta: { requiresAuth: true, role: 'Company' } 
    },

    // Student Routes
    { 
      path: '/student', 
      component: StudentDashboard, 
      meta: { requiresAuth: true, role: 'Student' } 
    },
    { 
      path: '/student/profile', 
      component: StudentProfile, 
      meta: { requiresAuth: true, role: 'Student' } 
    },
    { 
      path: '/student/my-applications', 
      component: MyApplications, 
      meta: { requiresAuth: true, role: 'Student' } 
    },
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login');
    } else if (to.meta.role && to.meta.role !== role) {
      alert('Unauthorized Access');
      next('/login'); // Redirect if role doesn't match
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router