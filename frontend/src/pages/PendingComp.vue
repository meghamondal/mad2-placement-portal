<script>
import api from '@/utils/api';
export default {
  name: "PendingCompany",

  data() {
    return {
      companies: [],
      selectedComp: null,
      errorMsg: ""
    };
  },
  created() {
    this.loadPCompanies();
  },
  methods: {
    async loadPCompanies() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/comp_plist");
        this.companies = data;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the companies...";
      }
    },
    async viewComp(c_id) {
      this.errorMsg = "";
      try{
        const data = await api.get(`/admin_api/comp_details/${c_id}`);
        if (Array.isArray(data)){this.selectedComp = data[0];}
        else{this.selectedComp = data;}
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "can't fetch the details...";
      }
    },
    async editStatus(company) {
      this.errorMsg = "";
      try{
        await api.patch(`/admin_api/comp_status/${company.c_id}`,{
          approval_status: company.approval_status
        }
        )
        this.loadPCompanies()
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "Error in updation...";
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
        <h4 class="mb-0">Pending Companies...</h4>
        <div class="card-body">
          <table class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
              <th>Company ID</th>
              <th>Name</th>
              <th class="text-center">Status</th>
              <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(company, id) in companies" :key="company.c_id">
                <td>{{  id+1  }}</td>
                <td>{{company.c_id  }}</td>
                <td>{{ company.c_name }}</td>
                <td class="text-center">
                  <select class="form-select form-select-sm d-inline w-auto" aria-label="Default select example" v-model="company.approval_status">
                    <option disabled value="">Change Status</option>
                    <option value="approved">Approve</option>
                    <option value="rejected">Reject</option>
                    <option value="pending">Pending</option>
                  </select>
                  
                </td>
                <td class="button-group">
                  <button class="btn btn-primary" @click="viewComp(company.c_id)">View Details</button>
                  <button class="btn btn-success" @click="editStatus(company)">Update</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <p v-if="companies.length === 0" class="text-center test muted">No Pending Companies are present</p>
      <div v-if ="selectedComp" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Company Details</div>
        <div class="card-body">
          <p><strong>ID: </strong>{{ selectedComp.c_id }}</p>
          <p><strong>Name: </strong>{{ selectedComp.c_name }}</p>
          <p><strong>HR Contact: </strong>{{ selectedComp.hr_contact}}</p>
          <p><strong>Website: </strong>{{ selectedComp.website }}</p>
          <p><strong>Industry: </strong>{{ selectedComp.industry }}</p>
          <p><strong>Approval Status: </strong>{{ selectedComp.approval_status }}</p>
          <button @click="cancel" class="btn btn-secondary">Cancel</button>
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