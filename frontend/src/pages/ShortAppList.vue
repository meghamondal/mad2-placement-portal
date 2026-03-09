<script>
import api from '@/utils/api';
export default {
  name: "ShortlistedApplications",

  data () {
    return {
      applications: [],
      errorMsg: ""
    };
  },
  created() {
    this.loadSApp();
  },
  methods: {
    async loadSApp() {
      this.errorMsg = "";
      try{
        const data = await api.get("/comp_api/short_app_list");
        this.applications = data;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the applications...";
      }
    },
    appIntw(app_id) {
      localStorage.setItem("selected_app_id", app_id);
      this.$router.push("/app_intw");
    },
    async intw_pass(app_id) {
      this.errorMsg = "";
      try {
        await api.patch(`/comp_api/intw_pass/${app_id}`);
        alert("Interview Status Marked as pass")
        this.applications = this.applications.filter(
        app => app.app_id !== app_id);
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "Interview is not completed yet";
      }
    },
    async intw_fail(app_id) {
      this.errorMsg = "";
      try {
        await api.patch(`/comp_api/intw_fail/${app_id}`);
        alert("Interview Status Marked as fail")
        this.applications = this.applications.filter(
        app => app.app_id !== app_id);
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "Interview is not completed yet";
      }
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <h4 class="mb-0"> Shortlisted Applications...</h4>
        <div class="card-body">
          <p v-if="errorMsg" class="text-danger">{{ errorMsg }}</p>
          <p v-if="applications.length === 0" class="text-center text-muted">No shortlisted application is present... </p>
          <table v-else class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
                <th>Application ID</th>
                <th>Pd ID</th>
                <th>Job Title</th>
                <th>Student Name</th>
                <th>Application Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, id) in applications" :key="app.app_id">
                <td>{{  id+1  }}</td>
                <td>{{ app.app_id  }}</td>
                <td>{{ app.pd_id  }}</td>
                <td>{{ app.pd_details.job_title  }}</td>
                <td>{{ app.student_details.f_name }} {{ app.student_details.l_name }}</td>
                <td>{{ app.app_status }}</td>
                <td class="button-group">
                  <button v-if="app.app_status == 'shortlisted'" class="btn btn-info" @click="appIntw(app.app_id)">Schedule Interview</button>
                  <button v-if="app.app_status == 'interview scheduled'" class="btn btn-info" @click="intw_pass(app.app_id)">Passed</button>
                  <button v-if="app.app_status == 'interview scheduled'" class="btn btn-info" @click="intw_fail(app.app_id)">Failed</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div> 
</template>

<style scoped>
.button-group button{
  margin: 0 0.5rem;

}

body {
  background-color: antiquewhite;
}
</style>