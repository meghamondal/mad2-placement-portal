<script>
export default {
  name: "AdminDashboard"
};
</script>

<template>
  <div class="container mt-4">
    <div v-for="(student, index) in students" :key="student.stud_id" class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      
    </div>
  </div> 
</template>