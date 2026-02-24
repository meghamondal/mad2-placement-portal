<script>
import api from '@/utils/api';
export default {
  name: "CompanyDashboard",

  data () {
    return {
      pdCount: 0,
      activePdCount: 0,
      appCount: 0,
      shortAppCount: 0,
      company: null,
      compEdit: null,
      isEditing: false,
      job_title: "",
      job_description: "",
      eligible_branch: "",
      min_cgpa: null,
      eligible_year: null,
      application_deadline: "",
      pd_status: "pending",
      isCreating: false,
      errorMsg: ""
    }
  },
  created() {
    this.loadCounts();
    this.loadCompany();
  },
  methods: {
    async loadCounts() {
      this.errorMsg = "";
      try{
        const data = await api.get("/comp_api/comp_counts");
        this.pdCount = data.pd_count;
        this.activePdCount = data.active_pd_count;
        this.appCount = data.app_count;
        this.shortAppCount = data.short_app_count;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the counts...";
      }
    },
    async loadCompany() {
      this.errorMsg = "";
      try {
        const data = await api.get("/comp_api/comp_details");
        console.log("company data: ", data)
        this.company = data;
      }
      catch (error) {
        this.errorMsg = error.message || "Company data not found...";
      }
    },
    editComp(company) {
      // this.selectedComp = null;
      this.compEdit = { ...company };
      this.isEditing = true;
    },
    async saveEdit() {
      try {
        const edit = await api.patch(`/comp_api/comp_details`, this.compEdit);
        this.company = edit;
        this.isEditing = false;
        this.compEdit = null;
      }
      catch (error) {
        this.errorMsg = error.message || "Error in updation...";
      }
    },
    openCform() {
      this.isCreating = true;
    },
    async createPd () {
      this.errorMsg = "";
      if (!this.job_title) {
        this.errorMsg = "Please enter job title...";
        return;
      }
      if (!this.job_description) {
        this.errorMsg = "Please enter job description...";
        return;
      }
      if (!this.eligible_branch) {
        this.errorMsg = "Please enter eligible branch...";
        return;
      }
      if (!this.min_cgpa) {
        this.errorMsg = "Please enter min cgpa...";
        return;
      }
      if (!this.eligible_year) {
        this.errorMsg = "Please enter eligible year...";
        return;
      }
      if (!this.application_deadline) {
        this.errorMsg = "Please enter min application deadline...";
        return;
      }
      try {
        const payload = {
          job_title: this.job_title,
          job_description: this.job_description,
          eligible_branch: this.eligible_branch,
          min_cgpa: this.min_cgpa,
          eligible_year: this.eligible_year,
          application_deadline: this.application_deadline,
          pd_status: "pending"
        };
        const response = await api.post("/comp_api/comp_pdcreate", payload);
        alert("Placement drive created successfully...");
        await this.loadCounts();
        this.isCreating = false;
      }
      catch (error) {
        this.errorMsg = error.message || "Placement Drive creation failed...";
      }
    },
    cancel() {
      this.compEdit = false;
      this.isEditing = false;
      this.isCreating = false;
      this.job_title = "",
      this.job_description = "",
      this.eligible_branch = "",
      this.min_cgpa = "",
      this.eligible_year = "",
      this.application_deadline = "",
      this.isCreating = false

      this.errorMsg = "";
      console.log("Details closed...")
    }
  }
};
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total Placement Drives...</h5>
      <h4 class="fw-bold text-primary">{{ pdCount }}</h4>
    </div>
  </div>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total Active Placement Drives...</h5>
      <h4 class="fw-bold text-primary">{{ activePdCount }}</h4>
    </div>
  </div>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total Application Counts...</h5>
      <h4 class="fw-bold text-primary">{{ appCount }}</h4>
    </div>
  </div>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total Shortlisted Application Counts...</h5>
      <h4 class="fw-bold text-primary">{{ shortAppCount }}</h4>
    </div>
  </div>

<!-- company details -->

 <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div v-if="company && !isEditing" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center"><h4>Company Details</h4>
          <button class="btn btn-warning" @click="editComp(company)">Edit</button>
        </div>
        <div class="card-body">
          <p><strong>ID: </strong>{{ company.c_id }}</p>
          <p><strong>Name: </strong>{{ company.c_name }}</p>
          <p><strong>HR Contact: </strong>{{ company.hr_contact}}</p>
          <p><strong>Website: </strong>{{ company.website }}</p>
          <p><strong>Industry: </strong>{{ company.industry }}</p>
          <p><strong>Approval Status: </strong>{{ company.approval_status }}</p>        
        </div>
      </div>
      <div v-if="isEditing" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Edit Company Details</div>
        <div class="card-body">
          <div class="mb-3">
            <label for="comp_name" class="form-label">Company Name: </label>
            <input type="text" class="form-control" aria-describedby="comp_name" v-model="compEdit.c_name">
           </div>
           <div class="mb-3">
            <label for="hr_contact" class="form-label">HR Contact: </label>
            <input type="text" class="form-control" aria-describedby="hr_contact" v-model="compEdit.hr_contact">
           </div>
           <div class="mb-3">
            <label for="website" class="form-label">Website: </label>
            <input type="text" class="form-control" aria-describedby="website" v-model="compEdit.website">
           </div>
           <div class="mb-3">
            <label for="industry" class="form-label">Industry: </label>
            <input type="text" class="form-control" aria-describedby="industry" v-model="compEdit.industry">
           </div>
           <div class="mb-3 center">
            <button @click="saveEdit" type="submit" class="btn btn-primary">Save</button>
            <button @click="cancel" class="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div> 
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <button class="btn btn-success mt-2" @click="openCform">+Create New Placement Drive</button>
      <div v-if="isCreating" class="card mt-4 shadow-sm border-0">
        <div class="card-body">
          <form @submit.prevent="createPd">
            <div class="mb-3">
              <label for="job_title" class="form-label">Job Title: </label>
              <input type="text" class="form-control"  placeholder="job title" v-model="job_title">
            </div>
            <div class="mb-3">
              <label for="job_description" class="form-label">Job Description: </label>
              <input type="text" class="form-control"  placeholder="job description" v-model="job_description">
            </div>
            <div class="mb-3">
              <label for="eligible_branch" class="form-label">Eligible Branch: </label>
              <input type="text" class="form-control"  placeholder="eligible branch" v-model="eligible_branch">
            </div>
            <div class="mb-3">
              <label for="min_cgpa" class="form-label">Minimum Cgpa: </label>
              <input type="number" class="form-control"  placeholder="minimum cgpa" v-model="min_cgpa">
            </div>
            <div class="mb-3">
              <label for="eligible_year" class="form-label">Eligible Year: </label>
              <input type="number" class="form-control"  placeholder="eligible year" v-model="eligible_year">
            </div>
            <div class="mb-3">
              <label for="application_deadline" class="form-label">Application Deadline: </label>
              <input type="date" class="form-control"  placeholder="application deadline" v-model="application_deadline">
            </div>
            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-primary">Save</button>
              <button @click="cancel" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>