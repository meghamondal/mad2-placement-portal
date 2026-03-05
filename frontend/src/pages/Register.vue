<script>

export default {
  name: "Register",
  data () {
  },
  methods: {
    goToStudReg() {
      this.$router.push('/student/register')
    },
    goToCompReg() {
      this.$router.push('/company/register')
    }

  }
};
</script>

<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="card shadow p-4" style="width: 380px;">
      <h4 class="text-center mb-4">Register As...</h4>
      <div class="row justify-content-center"> 
        <div class="col-auto">
          <button type="button" class="btn btn-outline-primary" @click="goToStudReg"> Student </button>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-outline-primary" @click="goToCompReg"> Company </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
body {
  background-color: antiquewhite;
}
</style>