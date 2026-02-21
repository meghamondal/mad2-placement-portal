<script>
import api from '@/utils/api';
export default {
  name: "AdminDashboard",
  
  data() {
    return {
      p_drives: [],
      selectedPd: null,
      pdSearch:"",
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
        this.errorMsg = error.message || "can't fetch the placement derives...";
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
        this.errorMsg = error.message || "can't fetch the details...";
      }
    },
    cancel() {
      this.selectedPd = null;
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
                <td class="text-center">
                  <button class="btn btn-primary" @click="viewPd(pd.pd_id)">View</button>
                  <!-- <button class="btn btn-warning" @click="editPd(pd)">View</button> -->
                </td>
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
          <p><strong>Company Name: </strong>{{ selectedPd.job_title }}</p>
          <p><strong>Job Description: </strong>{{ selectedPd.job_description }}</p>
          <p><strong>Eligible Branch: </strong>{{ selectedPd.eligible_branch }}</p>
          <p><strong>Min Cgpa: </strong>{{ selectedPd.min_cgpa }}</p>
          <p><strong>Eligible Year: </strong>{{ selectedPd.eligible_year }}</p>
          <p><strong>Application Deadline: </strong>{{ selectedPd.application_deadline }}</p>
          <p><strong>Pd Status: </strong>{{ selectedPd.pd_status }}</p>
          <button @click="cancel" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div> 
</template>