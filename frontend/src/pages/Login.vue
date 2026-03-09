<script>
import { useAuthStore } from '@/stores/auth';
export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      errorMsg: "",
      auth: useAuthStore()
    };
  },
  methods: {
    async userLogin() {
      this.errorMsg = "";

      if (!this.email){
        this.errorMsg = "Please enter your email address...";
        return;
      }
      const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!pattern.test(this.email)){
        this.errorMsg = "Enter valid email address...";
        return;
      }
      if (!this.password){
        this.errorMsg = "Please enter password...";
        return;
      }
      try{
        await this.auth.login({
          email: this.email,
          password: this.password
        });
        if (this.auth.userRole === "admin"){
          this.$router.push("/admin/dashboard");
        }
        else if (this.auth.userRole === "student"){
          this.$router.push("/student/dashboard");
        }
        else if (this.auth.userRole === "company"){
          this.$router.push("/company/dashboard");
        }
      }
      catch (error) {
        this.errorMsg = error.message || "Admin have deactivated this account...";
      }
    }
  }
};
</script>

<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="card shadow p-4" style="width: 380px;">
      <h4 class="text-center mb-4">Login</h4>
    <form @submit.prevent="userLogin">
      <div class="mb-3">
        <label for="email" class="form-label">Email: </label>
        <input type="email" class="form-control"  placeholder="name@example.com" v-model="email">
      </div>
      <div class="mb-3">
        <label for="inputPassword" class="form-label">Password: </label>
        <input type="password" class="form-control" placeholder="Your password" v-model="password">
      </div>
      <div class="d-grid">
        <button type="submit" class="btn btn-primary">Login</button>
      </div>
      <div class="text-center mt-3">
        New user?
        <router-link to="/register">Sign Up</router-link>
      </div>
      <div v-if="errorMsg" class="text-danger small mt-2">{{ errorMsg  }}</div>
    </form>
    </div>
  </div>

</template>

<style>
body {
  background-color: antiquewhite;
}
</style>