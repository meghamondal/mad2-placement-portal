<script>
import api from '@/utils/api';
export default{
  name:"InterviewDetails",

  data() {
    return {
      selectedApp: null,
      errorMsg: ""
    };
  },
  created() {
    this.loadIntw();
  },
  methods: {
    async loadIntw() {
      try {
        const app_id = localStorage.getItem("selected_app_id");
        if (!app_id) {
          this.errorMsg = "No application is selected...";
        }
        const data = await api.get("/api/stud_apps");
        this.selectedApp = data.find(item => String(item.app_id) === String(app_id));
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message;
      }
    },
    viewOffer(app) {
      localStorage.setItem("selected_app_id", app.app_id);
      this.$router.push("/offer_letter");
    }
  }
}

</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-light text-black d-flex justify-content-between align-items-center">
          <h4 class="mb-0"> Interview Details...</h4>
        </div>
        <div v-if="selectedApp" class="card-body">
          <p><strong>ApplicationID: </strong>{{ selectedApp.app_id }}</p>
          <p><strong>Job Title </strong>{{ selectedApp.pd_details.job_title }}</p>
          <p><strong>Company Name: </strong>{{ selectedApp.company_name }}</p>
          <p><strong>Scheduled On: </strong>{{ selectedApp.intw_details[0].scheduled.substring(0,16)+ ', '+selectedApp.intw_details[0].scheduled.substring(17,22) }}</p>
          <p><strong>Remarks: </strong>{{ selectedApp.intw_details[0].remarks }}</p>
          <p><strong>Status: </strong>{{ selectedApp.intw_details[0].intw_status }}</p>
          <button v-if="selectedApp.intw_details[0].intw_status === 'passed'" class = "btn btn-success" @click="viewOffer(selectedApp)">View Offer Letter</button>
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