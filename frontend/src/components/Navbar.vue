<script>
import { useAuthStore } from '@/stores/auth';
export default {
  name: "Navbar",
  data() {
    return {
      // searchQuery: "",
      auth: useAuthStore()
    };
  },
  computed: {
    isAdmin() { return this.auth.userRole === "admin";},
    isStudent() { return this.auth.userRole === "student";},
    isCompany() { return this.auth.userRole === "company";},
    isAuthenticated() { return this.auth.isAuthenticated;}
  },
  methods: {
    // Search() { console.log("Search:", this.searchQuery);},
    logout() {this.auth.logout();
      this.$router.push("/");
    },
  }
};
</script>
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <router-link  class="navbar-brand fw-bold" to="/">Placement Portal</router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item" v-if="isAdmin">
          <router-link class="nav-link" to="/admin/dashboard">Admin Dashboard</router-link>
        </li>
        <li class="nav-item" v-if="isAdmin">
          <router-link class="nav-link" to="/pendingComp">Pending Companies</router-link>
        </li>
        <li class="nav-item" v-if="isAdmin">
          <router-link class="nav-link" to="/pendingPd">Pending Placement Drives</router-link>
        </li>
        <li class="nav-item" v-if="isStudent">
          <router-link class="nav-link" to="/student/dashboard">Student Dashboard</router-link>
        </li>
        <li class="nav-item" v-if="isCompany">
          <router-link class="nav-link" to="/company/dashboard">Company Dashboard</router-link>
        </li>
        <li class="nav-item" v-if="isCompany">
          <router-link class="nav-link" to="/pd_list">Placement Drive List</router-link>
        </li>
        <!-- <li class="nav-item" v-if="isCompany">
          <router-link class="nav-link" to="/app_list">Applications List</router-link>
        </li> -->
      </ul>
      <!-- <form class="d-flex me-3" v-if="isAuthenticated" @submit.prevent="Search">
      <input class="form-control me-2" type="search" placeholder="Search" v-model="searchQuery">
      <button class="btn btn-outline-success" type="submit">Search</button>
      </form> -->
      <span class="navbar-text text-light ms-4 me-3" v-if="isAuthenticated">
        Welcome {{ auth.user?.email}}
      </span>
      <ul class="navbar-nav mb-2 mb-lg-0">
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <router-link class="nav-link" to="/register">Sign Up</router-link>
        </li>
        <li class="nav-item" v-if="auth.isAuthenticated">
          <a href="/" @click="logout">Logout</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
</template>
