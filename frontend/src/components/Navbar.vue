<script>
import { useAuthStore } from '@/stores/auth';
export default {
  name: "Navbar",
  data() {
    return {
      searchQuery: "",
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
    Search() { console.log("Search:", this.SearchQuery);},
    logout() {this.auth.logout();
      this.$router.push("/login");
    }
  }
};
</script>

<template>
  <nav class="navbar navbar-dark bg-dark">
    <div class="container-fluid">
    <router-link  class="navbar-brand fw-bold" to="/">Placement Portal</router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item" v-if="isAdmin">
          <router-link class="nav-link active" aria-current="page" to="/admin/dashboard">Admin Dashboard</router-link>
        </li>
        <li class="nav-item" v-if="isStudent">
          <router-link class="nav-link active" aria-current="page" to="/student/dashboard">Student Dashboard</router-link>
        </li>
        <li class="nav-item" v-if="isCompany">
          <router-link class="nav-link active" aria-current="page" to="/company/dashboard">Company Dashboard</router-link>
        </li>
      </ul>
      <form class="d-flex" v-if="isAuthenticated" @submit.prevent="Search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>

      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <router-link class="nav-link active" aria-current="page" to="/login">Login</router-link>
        </li>
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <router-link class="nav-link active" aria-current="page" to="/register">Sign Up</router-link>
        </li>
        <li class="nav-item" v-if="auth.isAuthenticated">
          <button class="btn btn-danger" @click="logout">Logout</button>
        </li>
      </ul>
    </div>
  </div>

  </nav>

</template>

