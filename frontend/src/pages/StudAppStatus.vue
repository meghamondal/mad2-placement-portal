<script>
import api from '@/utils/api';
export default{
  name: "StudAppStatus",

  data() {
    return {
      applications: [],
      appSearch:"",
      errorMsg: ""
    };
  },
  computed: {
    filteredApplications() {
      const text = this.appSearch.toLowerCase()
      if (!text) { return this.applications }
      return this.applications.filter(app => {
        const searchId = String(app.app_id).includes(text)
        const searchJobtitle = app.pd_details.job_title.toLowerCase().includes(text)
        const searchappStatus = app.app_status.toLowerCase().includes(text)
        return searchId || searchJobtitle ||  searchappStatus
      })
    }
  },
  created() {
    this.loadApp();
  },
  methods: {
    async loadApp() {
      this.errorMsg = "";
      try{
        const data = await api.get("/api/stud_apps");
        this.applications = data;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the applications...";
      }
    },
    Search() {

    },
    viewIntw(app) {
      localStorage.setItem("selected_app_id", app.app_id);
      this.$router.push("/intw_details");
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <div class=" d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Applied Applications...</h4>
          <form class="d-flex me-3 input-group input-group-sm" style="max-width: 350px;">
            <input class="form-control me-2" type="search" placeholder="Search" v-model="appSearch">
            <button class="btn btn-outline-success" type="submit"><i class="bi bi-search"></i>Search</button>
          </form>
        </div>
        <div class="card-body">
          <p v-if="applications.length === 0" class="text-center text-muted">No application is applied... </p>
          <table v-else class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
                <th>Application ID</th>
                <th>Pd ID</th>
                <th>Company Name</th>
                <th>Job Title</th>
                <th>Application Status</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, id) in filteredApplications" :key="app.app_id">
                <td>{{  id+1  }}</td>
                <td>{{ app.app_id  }}</td>
                <td>{{ app.pd_id  }}</td>
                <td>{{ app.company_name  }}</td>
                <td>{{ app.pd_details.job_title  }}</td> 
                <td>{{ app.app_status }}</td>
                <button v-if="app.app_status === 'interview scheduled' || app.app_status === 'selected'" class="btn btn-info" @click="viewIntw(app)">View Details</button>
              </tr>
            </tbody>
          </table>
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