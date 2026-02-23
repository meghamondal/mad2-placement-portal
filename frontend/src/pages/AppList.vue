<script>
import api from '@/utils/api';
export default {
  name: "ApplicationList",

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
        const searchFname = app.student_details.f_name.toLowerCase().includes(text)
        const searchLname = app.student_details.l_name.toLowerCase().includes(text)
        const searchappStatus = app.app_status.toLowerCase().includes(text)
        return searchId || searchJobtitle || searchFname || searchLname || searchappStatus
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
        const pd_id = localStorage.getItem("selected_pd_id");
        if (!pd_id){
          this.errorMsg = "No Placement Drive selected...";
          return;
        }
        const data = await api.get(`/comp_api/comp_applist/${pd_id}`);
        this.applications = data;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the applications...";
      }
    },
     Search() {

    },
    async editStatus(app) {
      this.errorMsg = "";
      try{
        await api.patch(`/comp_api/comp_editastatus/${app.app_id}`,{
          app_status: app.app_status
        }
        );
        this.loadApp()
      }
      catch (error) {
        this.errorMsg = error.message || "Error in updation...";
      }
    },
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
          <table class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
                <th>Application ID</th>
                <th>Pd ID</th>
                <th>Job Title</th>
                <th>Student Name</th>
                <th>Application Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, id) in filteredApplications" :key="app.app_id">
                <td>{{  id+1  }}</td>
                <td>{{ app.app_id  }}</td>
                <td>{{ app.pd_id  }}</td>
                <td>{{ app.pd_details.job_title  }}</td>
                <td>{{ app.student_details.f_name }} {{ app.student_details.l_name }}</td>
                <td>{{ app.app_status }}</td>
                <td class="text-center">
                  <select class="form-select form-select-sm d-inline w-auto" aria-label="Default select example" v-model="app.app_status">
                    <option disabled value="">Change Status</option>
                    <option value="applied">applied</option>
                    <option value="shortlisted">shortlisted</option>
                    <option value="selected">selected</option>
                    <option value="rejected">rejected</option>
                  </select>
                </td>
                <td class="button-group">
                  <button class="btn btn-success" @click="editStatus(app)">Update</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div> 
</template>