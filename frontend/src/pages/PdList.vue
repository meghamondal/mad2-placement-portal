<script>
import api from '@/utils/api';
export default {
  name: "PlacementDriveList",
  
  data() {
    return {
      p_drives: [],
      selectedPd: null,
      pdSearch:"",
      pdEdit: null,
      isEditing: false,
      errorMsg: ""
    };
  },
  computed: {
    filteredP_drives() {
      const text = this.pdSearch.toLowerCase()
      if (!text) { return this.p_drives }
      return this.p_drives.filter(pd => {
        const searchId = String(pd.pd_id).includes(text)
        const searchCName = pd.company_details.c_name.toLowerCase().includes(text)
        const searchJobtitle = pd.job_title.toLowerCase().includes(text)
        const searchPdstatus = pd.pd_status.toLowerCase().includes(text)
        const searchBranch = pd.eligible_branch.toLowerCase().includes(text)
        return searchId || searchCName || searchJobtitle || searchBranch || searchPdstatus
      })
    }
  },
  created() {
    this.loadPd();
  },
  methods: {
    async loadPd() {
      this.errorMsg = "";
      try{
        const data = await api.get("/comp_api/comp_pdlist");
        this.p_drives = data;
        console.log(data);
        
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the placement derives...";
      }
    },
    async viewPd(pd_id) {
      this.errorMsg = "";
      try{
        const data = await api.get(`/comp_api/comp_pd_details/${pd_id}`);
        if (Array.isArray(data)){this.selectedPd = data[0];}
        else{this.selectedPd = data;}
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the details...";
      }
    },
    editPd(pd) {
      this.selectedPd = null;
      // this.pdEdit = { ...pd };
      const newpd = { ...pd };
      if (newpd.application_deadline){
        newpd.application_deadline = new Date(newpd.application_deadline).toISOString().slice(0,16);
      }
      // let app_date = new Date(this.pdEdit.application_deadline)
      // this.pdEdit.application_deadline = app_date
      this.pdEdit = newpd

      this.isEditing = true;
    },
    async saveEdit() {
      try {
        const payload = { ...this.pdEdit };
        if (payload.application_deadline){
          // payload.application_deadline = new Date(payload.application_deadline).toISOString().split("T")[0];
          payload.application_deadline = payload.application_deadline.slice(0, 10);
        }
        await api.patch(`/comp_api/comp_pdedit/${payload.pd_id}`, payload);
        await this.loadPd();
        this.isEditing = false;
        this.pdEdit = null;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "Error in updation..." 
      }
    },
    appPd(pd_id) {
      localStorage.setItem("selected_pd_id", pd_id);
      this.$router.push("/app_list");
    },
    cancel() {
      this.selectedPd = null;
      this.pdEdit = null;
      this.isEditing = false;
      this.errorMsg = "";
    }
  }
}
</script>
<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <div class=" d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Created Placement drives...</h4>
          <form class="d-flex me-3 input-group input-group-sm" style="max-width: 350px;">
            <input class="form-control me-2" type="search" placeholder="Search" v-model="pdSearch">
            <button class="btn btn-outline-success" type="submit"><i class="bi bi-search"></i>Search</button>
          </form>
        </div>
        <div class="card-body">
          <table class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
              <th>Pd ID</th>
              <th>Company ID</th>
              <th>Company Name</th>
              <th>Job Title</th>
              <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(pd, id) in filteredP_drives" :key="pd.pd_id">
                <td>{{  id+1  }}</td>
                <td>{{ pd.pd_id  }}</td>
                <td>{{ pd.c_id  }}</td>
                <td>{{ pd.company_details.c_name  }}</td>
                <td>{{ pd.job_title }}</td>
                <td class="d-flex gap-2">
                  <button class="btn btn-primary" @click="viewPd(pd.pd_id)">View</button>
                  <button class="btn btn-warning" @click="editPd(pd)">Edit</button>
                  <button class="btn btn-info" @click="appPd(pd.pd_id)">Applications</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="selectedPd && !isEditing" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Placement Drive Details</div>
        <div class="card-body">
          <p><strong>Pd ID: </strong>{{ selectedPd.pd_id }}</p>
          <p><strong>Company ID: </strong>{{ selectedPd.c_id}}</p>
          <p><strong>Company Name: </strong>{{ selectedPd.job_title }}</p>
          <p><strong>Job Description: </strong>{{ selectedPd.job_description }}</p>
          <p><strong>Eligible Branch: </strong>{{ selectedPd.eligible_branch }}</p>
          <p><strong>Min Cgpa: </strong>{{ selectedPd.min_cgpa }}</p>
          <p><strong>Eligible Year: </strong>{{ selectedPd.eligible_year }}</p>
          <p><strong>Application Deadline: </strong>{{ new Date(selectedPd.application_deadline).toLocaleDateString() }}</p>
          <p><strong>Pd Status: </strong>{{ selectedPd.pd_status }}</p>
          <button @click="cancel" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div> 
  <div v-if="isEditing" class="card mt-4 shadow-sm border-0">
    <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Edit Placement Drive Details</div>
    <div class="card-body">
      <div class="mb-3">
        <label for="job_title" class="form-label">Job Title: </label>
        <input type="text" class="form-control" aria-describedby="job_title" v-model="pdEdit.job_title">
      </div>
      <div class="mb-3">
        <label for="job_description" class="form-label">Job Description: </label>
        <input type="text" class="form-control" aria-describedby="job_description" v-model="pdEdit.job_description">
      </div>
      <div class="mb-3">
        <label for="eligible_branch" class="form-label">Eligible Branch: </label>
        <input type="text" class="form-control" aria-describedby="eligible_branch" v-model="pdEdit.eligible_branch">
      </div>
      <div class="mb-3">
        <label for="min_cgpa" class="form-label">Minimum Cgpa: </label>
        <input type="number" class="form-control" aria-describedby="min_cgpa" v-model="pdEdit.min_cgpa">
      </div>
      <div class="mb-3">
        <label for="eligible_year" class="form-label">Eligible Branch: </label>
        <input type="number" class="form-control" aria-describedby="eligible_year" v-model="pdEdit.eligible_year">
      </div>
      <div class="mb-3">
        <label for="application_deadline" class="form-label">Application Deadline: </label>
        <input type="datetime-local" class="form-control" aria-describedby="application_deadline" v-model="pdEdit.application_deadline">
      </div>
      <div class="d-flex gap-2">
        <button @click="saveEdit" type="submit" class="btn btn-primary">Save</button>
        <button @click="cancel" class="btn btn-secondary">Cancel</button>
      </div>
    </div>
  </div>
</template>

<style>
body {
  background-color: antiquewhite;
}
</style>