<script>
import api from '@/utils/api';
export default {
  data() {
    return {
      email: "",
      password: "",
      c_name: "",
      hr_contact: "",
      website: "",
      industry: "",
      errorMsg: ""
    };
  },
  methods: {
    async compReg() {
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
      if (!this.c_name){
        this.errorMsg = "Please enter your company name...";
        return;
      }
      if (!this.hr_contact){
        this.errorMsg = "Please enter hr contact...";
        return;
      }
      if (!this.website){
        this.errorMsg = "Please enter you website link...";
        return;
      }
      if (!this.industry){
        this.errorMsg = "Please enter industry...";
        return;
      }
      try{
        const payload = {
          email: this.email,
          password: this.password,
          role: "company",
          c_name: this.c_name,
          hr_contact: this.hr_contact,
          website: this.website,
          industry: this.industry
        };
        const response = await api.post("/api/company/register", payload);
        alert("Registration successful...");
        this.$router.push("/login");
      }
      catch (error) {
        this.errorMsg = error.message || "Registration failed...";
      }
    }
  }
}
</script>

<template>
<div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="card shadow p-4" style="width: 380px;">
      <h4 class="text-center mb-4">Sign Up</h4>
    <form @submit.prevent="compReg">
      <div class="mb-3">
        <label for="email" class="form-label">Email: </label>
        <input type="email" class="form-control"  placeholder="name@example.com" v-model="email">
      </div>
      <div class="mb-3">
        <label for="inputPassword" class="form-label">Password: </label>
        <input type="password" class="form-control" placeholder="Your password" v-model="password">
      </div>
      <div class="mb-3">
        <label for="c_name" class="form-label">Company Name: </label>
        <input type="c_name" class="form-control"  placeholder="company name" v-model="c_name">
      </div>
      <div class="mb-3">
        <label for="hr_contact" class="form-label">HR Contact: </label>
        <input type="hr_contact" class="form-control"  placeholder="hr_contact" v-model="hr_contact">
      </div>
      <div class="mb-3">
        <label for="website" class="form-label">Website: </label>
        <input type="website" class="form-control"  placeholder="website" v-model="website">
      </div>
      <div class="mb-3">
        <label for="industry" class="form-label">Industry: </label>
        <input type="industry" class="form-control"  placeholder="industry" v-model="industry">
      </div>
      
      <div class="d-grid">
        <button type="submit" class="btn btn-primary">Sign Up</button>
      </div>
      <div class="text-center mt-3">
        Already registered?
        <router-link to="/login">Login</router-link>
      </div>
      <div v-if="errorMsg" class="text-danger small mt-2">{{ errorMsg  }}</div>
    </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: antiquewhite;
}
</style>