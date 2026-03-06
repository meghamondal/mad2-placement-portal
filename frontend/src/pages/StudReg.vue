<script>
import { useAuthStore } from '@/stores/auth';
import api from '@/utils/api';
export default {
  name: "StudentRegister",

  data() {
    return {
      email: "",
      password: "",
      f_name: "",
      l_name: "",
      resume_file: null,
      dob: "",
      graduation_year: "",
      cgpa: "",
      errorMsg: ""
    };
  },
  methods: {
    handleResume(event) {
      const file = event.target.files[0];
      if (!file){
        this.errorMsg = "File doesn't exist...";
        return;
      } 
      if (file.type !== "application/pdf") {
        alert("PDF files are only allowed");
        return;
        }
        this.resume_file = file;
    },
    async studReg() {
      this.errorMsg = "";
      if(!this.email){
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
      if (this.password.length < 6){
        this.errorMsg = "Password should have atleast 6 characters ...";
        return;
      }
      if (!this.f_name){
        this.errorMsg = "Please enter your first name...";
        return;
      }
      if (!this.l_name){
        this.errorMsg = "Please enter your last name...";
        return;
      }
      if (!this.resume_file){
        this.errorMsg = "Please enter resume file...";
        return;
      }
      if (!this.dob){
        this.errorMsg = "Please enter your date of birth...";
        return;
      }
      if (!this.graduation_year){
        this.errorMsg = "Please enter your graduation year...";
        return;
      }
      if (!this.cgpa){
        this.errorMsg = "Please enter your cgpa...";
        return;
      }
      try {
        const formData = new FormData();
          formData.append("email", this.email);
          formData.append("password", this.password);
          formData.append("f_name", this.f_name);
          formData.append("l_name", this.l_name);
          formData.append("resume_file", this.resume_file)
          formData.append("dob", this.dob);
          formData.append("graduation_year", this.graduation_year);
          formData.append("cgpa", this.cgpa)
        
        const response = await fetch("http://127.0.0.1:5000/api/student/register", {method: "POST", body: formData});
        const data = await response.json();
        if(!response.ok){
          throw new Error(data.message || "Registration failed...");
        }
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
    <p v-if="errorMsg" class="text-danger">{{ errorMsg }}</p>
    <form @submit.prevent="studReg">
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Email: </label>
        <input type="email" class="form-control"  placeholder="name@example.com" v-model="email">
      </div>
      <div class="mb-3">
        <label for="inputPassword" class="form-label">Password: </label>
        <input type="password" class="form-control" placeholder="Your password" v-model="password">
      </div>
      <div class="mb-3">
        <label for="f_name" class="form-label">First Name: </label>
        <input type="f_name" class="form-control"  placeholder="first name" v-model="f_name">
      </div>
      <div class="mb-3">
        <label for="l_name" class="form-label">Last Name: </label>
        <input type="l_name" class="form-control"  placeholder="last name" v-model="l_name">
      </div>
      <div class="mb-3">
        <label for="doc" class="form-label">Resume File(PDF): </label>
        <input type="file" class="form-control"  placeholder="Your Resume" accept="application/pdf" @change="handleResume">
      </div>
      <div class="mb-3">
        <label for="dob" class="form-label">Date of Birth: </label>
        <input type="date" class="form-control"  placeholder="Your date iof Birth" v-model="dob">
      </div>
      <div class="mb-3">
        <label for="graduation_year" class="form-label">Graduation Year: </label>
        <input type="number" class="form-control"  placeholder="Your graduation year" v-model="graduation_year">
      </div>
      <div class="mb-3">
        <label for="cgpa" class="form-label">CGPA: </label>
        <input type="number" step="any" min="0" max="10" class="form-control"  placeholder="Your cgpa" v-model="cgpa">
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

<style>
body {
  background-color: antiquewhite;
}
</style>