<script>
import api from '@/utils/api';
export default {
  name: "StudPlacementDrive",
  data() {
    return {
      p_drives: [],
      applications: [],
      pdSearch:"",
      selectedPd: null,
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
        return searchId || searchCName || searchJobtitle 
      })
    },
    applied_pds() {
      return this.applications.map(application => application.pd_id
      )
    }
  },
  created() {
    this.loadPd();
    this.loadApp();
  },
  methods: {
    async loadPd() {
      this.errorMsg = "";
      try{
        const data = await api.get("/api/stud_pdlist");
        console.log("placement drive", data )
        this.p_drives = data;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the placement drives...";
      }
    },
    async loadApp() {
      this.errorMsg = "";
      try{
        const data = await api.get("/api/stud_apps");
        console.log("applications: ", data )
        this.applications = data;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the applications...";
      }
    },
    
    async viewPd(pd_id) {
      this.errorMsg = "";
      try{
        const data = await api.get(`/api/stud_pddetails/${pd_id}`);
        if (Array.isArray(data)){this.selectedPd = data[0];}
        else{this.selectedPd = data;}

      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the details...";
      }
    },
    async studAppply(pd_id) {
      this.errorMsg = "";
      try {
        const response = await api.post(`/api/stud_apply/${pd_id}`);
        alert("Application Submission Successful...")
        this.loadPd();
        this.loadApp();
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message;
      }
    },
    cancel() {
      this.selectedPd = null;
    },
    checkApplied(selectedPd) {
      console.log(this.applications);
      
      return this.applied_pds.includes(selectedPd.pd_id)
    },
    checkDeadline(application_deadline) {
      const today = new Date();
      const appDate = new Date(application_deadline);
      return today > appDate
    }
  },

}
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <div class=" d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Placement drives...</h4>
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
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
                <tr v-for="(pd, id) in filteredP_drives" :key="pd.pd_id">
                <td>{{  id+1  }}</td>
                <td>{{ pd.pd_id  }}</td>
                <td>{{ pd.c_id  }}</td>
                <td>{{ pd.company_details.c_name  }}</td>
                <td>{{ pd.job_title }}</td>
                <button class="btn btn-primary" @click="viewPd(pd.pd_id)">View Details</button>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="selectedPd" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Placement Drive Details</div>
        <div class="card-body">
          <p><strong>Pd ID: </strong>{{ selectedPd.pd_id }}</p>
          <p><strong>Company ID: </strong>{{ selectedPd.c_id}}</p>
          <p><strong>Company Name: </strong>{{ selectedPd.company_details.c_name }}</p>
          <p><strong>Job Role: </strong>{{ selectedPd.job_title }}</p>
          <p><strong>Job Description: </strong>{{ selectedPd.job_description }}</p>
          <p><strong>Eligible Branch: </strong>{{ selectedPd.eligible_branch }}</p>
          <p><strong>Min Cgpa: </strong>{{ selectedPd.min_cgpa }}</p>
          <p><strong>Eligible Year: </strong>{{ selectedPd.eligible_year }}</p>
          <p><strong>Application Deadline: </strong>{{ selectedPd.application_deadline }}</p>
          <div class="button-group">
            <button @click="cancel" class="btn btn-secondary">Cancel</button>
            <button v-if="checkDeadline(selectedPd.application_deadline)" class="btn btn-danger" disabled>Closed</button>
            <button v-else-if="!checkApplied(selectedPd)" class="btn btn-success" @click="studAppply(selectedPd.pd_id)">Apply</button>
            <button v-else class="btn btn-secondary" disabled>Applied</button>
          </div>
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
