<script>
import api from '@/utils/api';
export default {
  name: "PendingCompany",

  data() {
    return {
      p_drives: [],
      selectedPd: null,
      errorMsg: ""
    };
  },
  created() {
    this.loadpPd();
  },
  methods: {
    async loadpPd() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/pd_plist");
        this.p_drives = data;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the placement drives...";
      }
    },
    async viewPd(pd_id) {
      this.errorMsg = "";
      try{
        const data = await api.get(`/admin_api/pd_details/${pd_id}`);
        if (Array.isArray(data)){this.selectedPd = data[0];}
        else{this.selectedPd = data;}
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the details...";
      }
    },
    async editStatus(pd) {
      this.errorMsg = "";
      try{
        await api.patch(`/admin_api/pd_status/${pd.pd_id}`,{
          pd_status: pd.pd_status
        }
        )
        this.loadpPd()
      }
      catch (error) {
        this.errorMsg = error.message || "Error in updation...";
      }
    },
    cancel() {
      this.selectedComp = null;
      console.log("Details closed...")
    }
    }
}
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <h4 class="mb-0">Pending Placement drives...</h4>
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
              <tr v-for="(pd, id) in p_drives" :key="pd.pd_id">
                <td>{{  id+1  }}</td>
                <td>{{ pd.pd_id  }}</td>
                <td>{{ pd.c_id  }}</td>
                <td>{{ pd.company_details.c_name  }}</td>
                <td>{{ pd.job_title }}</td>
                <td class="text-center">
                  <button class="btn btn-primary" @click="viewPd(pd.pd_id)">View</button>
                  <select class="form-select form-select-sm d-inline w-auto" aria-label="Default select example" v-model="pd.pd_status" @change="editStatus(pd)">
                    <option selected>Change Status</option>
                    <option value="approved">Approve</option>
                    <option value="rejected">Reject</option>
                    <option value="pending">Pending</option>
                  </select>
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