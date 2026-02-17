<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      c_name: "",
      hr_contact: "",
      website: "",
      errorMsg: ""
    };
  },
  methods: {
    
  }
}
</script>

<template>
<div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="card shadow p-4" style="width: 380px;">
      <h4 class="text-center mb-4">Sign Up</h4>
    <form @submit.prevent="compReg">
      <div class="mb-3">
        <label for="exampleFormControlInput1" class="form-label">Email: </label>
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