<script>
import api from '@/utils/api';
export default {
  name: "AdminDashboard",
  
  data() {
    return {
      studentCount: 0,
      companyCount: 0,
      pdCount: 0,
      students: [],
      selectedStud: null,
      companies: [],
      selectedComp: null,
      p_drives: [],
      selectedPd: null,
      applications: [],
      compSearch:"",
      studSearch:"",
      pdSearch:"",
      appSearch:"",
      errorMsg: ""
    };
  },
  computed: {
    filteredCompanies() {
      const text = this.compSearch.toLowerCase()
      if (!text) { return this.companies }
      return this.companies.filter(company => {
        const searchId = String(company.c_id).includes(text)
        const searchName = company.c_name.toLowerCase().includes(text)
        const searchIndustry = company.industry.toLowerCase().includes(text)
        const searchCompstatus = company.approval_status.toLowerCase().includes(text)
        return searchId || searchName || searchIndustry || searchCompstatus
      })
    },
    filteredStudents() {
      const text = this.studSearch.toLowerCase()
      if (!text) { return this.students }
      return this.students.filter(student => {
        const searchId = String(student.stud_id).includes(text)
        const searchFName = student.f_name.toLowerCase().includes(text)
        const searchLName = student.l_name.toLowerCase().includes(text)
        const searchCgpa = String(student.cgpa).includes(text)
        return searchId || searchFName || searchLName || searchCgpa
      })
    },
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
    },
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
    this.loadCounts();
    this.loadStudents();
    this.loadCompanies();
    this.loadPd();
    this.loadApp();
  },
  methods: {
    async loadCounts() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/counts");
        this.studentCount = data.student_count;
        this.companyCount = data.company_count;
        this.pdCount = data.pd_count;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the counts...";
      }
    },
    async loadStudents() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/stud_list");
        this.students = data;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the students...";
      }
    },
    async viewStud(stud_id) {
      this.errorMsg = "";
      try{
        const data = await api.get(`/admin_api/stud_details/${stud_id}`);
        if (Array.isArray(data)){this.selectedStud = data[0]; console.log(this.selectedStud.active);
        }
        else{this.selectedStud = data;}
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the details...";
      }
    },
    async deleteStud(stud_id) {
      const isConfirmed = confirm("Are you sure you want to delete this student?");
      if (!isConfirmed) return;
      this.errorMsg = "";
      try{
        await api.delete(`/admin_api/stud_details/${stud_id}`);
        this.students = this.students.filter(s => s.stud_id !== stud_id);
        if (this.selectedStud?.stud_id === stud_id) {
          this.selectedStud = null;
        }
        alert("Student deleted  successfully...")
      }
      catch (error) {
        this.errorMsg = error.message || "Error in deleting the record...";
      }
    },
    async loadCompanies() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/comp_list");
        this.companies = data;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the companies...";
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
        this.errorMsg = error.message || "can't fetch the details...";
      }
    },
    async deleteComp(c_id) {
      const isConfirmed = confirm("Are you sure you want to delete this company?");
      if (!isConfirmed) return;
      this.errorMsg = "";
      try{
        await api.delete(`/admin_api/comp_details/${c_id}`);
        this.companies = this.companies.filter(c => c.c_id !== c_id);
        if (this.selectedComp?.c_id === c_id) {
          this.selectedComp = null;
        }
        alert("Company deleted  successfully...")
      }
      catch (error) {
        this.errorMsg = error.message || "Error in deleting the record...";
      }
    },
    async loadPd() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/pd_list");
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
        const data = await api.get(`/admin_api/pd_details/${pd_id}`);
        if (Array.isArray(data)){this.selectedPd = data[0];}
        else{this.selectedPd = data;}
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the details...";
      }
    },
    async loadApp() {
      this.errorMsg = "";
      try{
        const data = await api.get("/admin_api/app_list");
        this.applications = data;
      }
      catch (error) {
        this.errorMsg = error.message || "can't fetch the applications...";
      }
    },
    async stud_a_edit(id) {
      try {
        await api.patch(`/admin_api/stud_edit/${id}`);
        this.loadStudents();
        this.viewStud(id);
      }
      catch (error) {
        this.errorMsg = error.message || "Error in updation...";
      }
    },
    async comp_a_edit(id) {
      try {
        await api.patch(`/admin_api/comp_edit/${id}`);
        this.loadCompanies();
        this.viewComp(id);
      }
      catch (error) {
        this.errorMsg = error.message || "Error in updation...";
      }
    },
    Search() {

    },
    cancel() {
      this.selectedStud = null;
      this.selectedComp = null;
      this.selectedPd = null;
      this.errorMsg = "";
      console.log("Details closed...")
    }
  }
};
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total Registered Students...</h5>
      <h4 class="fw-bold text-primary">{{ studentCount }}</h4>
    </div>
  </div>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total Registered Companies...</h5>
      <h4 class="fw-bold text-primary">{{ companyCount }}</h4>
    </div>
  </div>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <h5 class="text-muted">Total created placement drives...</h5>
      <h4 class="fw-bold text-primary">{{ pdCount }}</h4>
    </div>
  </div>
  <!-- student -->
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <div class=" d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Students who have registered...</h4>
          <form class="d-flex me-3 input-group input-group-sm" style="max-width: 350px;">
            <input class="form-control me-2" type="search" placeholder="Search" v-model="studSearch">
            <button class="btn btn-outline-success" type="submit"><i class="bi bi-search"></i>Search</button>
          </form>
        </div>
        <div class="card-body">
          <table class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
              <th>Student ID</th>
              <th>Name</th>
              <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, id) in filteredStudents" :key="student.stud_id">
                <td>{{  id+1  }}</td>
                <td>{{ student.stud_id  }}</td>
                <td>{{ student.f_name }} {{ student.l_name  }}</td>
                <td class="button-group text-center">
                  <button class="btn btn-primary" @click="viewStud(student.stud_id)">View</button>
                  <button class="btn btn-danger" @click="deleteStud(student.stud_id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="selectedStud" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Student Details</div>
        <div class="card-body">
          <p><strong>ID: </strong>{{ selectedStud.stud_id }}</p>
          <p><strong>Name: </strong>{{ selectedStud.f_name }} {{ selectedStud.l_name }}</p>
          <p><strong>Date of Birth: </strong>{{ new Date(selectedStud.dob).toDateString() }}</p>
          <p><strong>Graduation Year: </strong>{{ selectedStud.graduation_year }}</p>
          <p><strong>CGPA: </strong>{{ selectedStud.cgpa }}</p>
          <div class="button-group">
            <a :href="`http://127.0.0.1:5000/${selectedStud.resume_file}`" target="_blank">View Resume</a>
            <button :class="selectedStud.active ? 'btn btn-danger' : 'btn btn-success'" @click="stud_a_edit(selectedStud.stud_id)">{{ selectedStud.active ? "Deactivate" : "Activate" }}</button>
            <button @click="cancel" class="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div> 
<!-- company -->
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <div class=" d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Companies who have registered...</h4>
          <form class="d-flex me-3 input-group input-group-sm" style="max-width: 350px;">
            <input class="form-control me-2" type="search" placeholder="Search" v-model="compSearch">
            <button class="btn btn-outline-success" type="submit"><i class="bi bi-search"></i>Search</button>
          </form>
        </div>
        <div class="card-body">
          <table class="table table-hover table-striped align-middle">
            <thead class="table-ligh">
              <tr>
                <th>S. No</th>
              <th>Company ID</th>
              <th>Name</th>
              <th>Status</th>
              <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(company, id) in filteredCompanies" :key="company.c_id">
                <td>{{  id+1  }}</td>
                <td>{{company.c_id  }}</td>
                <td>{{ company.c_name }}</td>
                <td>{{ company.approval_status }}</td>
                <td class="button-group text-center">
                  <button class="btn btn-primary" @click="viewComp(company.c_id)">View</button>
                  <button class="btn btn-danger" @click="deleteComp(company.c_id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="selectedComp" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">Company Details</div>
        <div class="card-body">
          <p><strong>ID: </strong>{{ selectedComp.c_id }}</p>
          <p><strong>Name: </strong>{{ selectedComp.c_name }}</p>
          <p><strong>HR Contact: </strong>{{ selectedComp.hr_contact}}</p>
          <p><strong>Website: </strong>{{ selectedComp.website }}</p>
          <p><strong>Industry: </strong>{{ selectedComp.industry }}</p>
          <p><strong>Approval Status: </strong>{{ selectedComp.approval_status }}</p>
          <div class="button-group">
            <button :class="selectedComp.active ? 'btn btn-danger' : 'btn btn-success'" @click="comp_a_edit(selectedComp.c_id)">{{ selectedComp.active ? "Deactivate" : "Activate" }}</button>
            <button @click="cancel" class="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div> 
<!-- placement drive -->
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
          <!-- <p><strong>Application Deadline: </strong>{{ selectedPd.application_deadline }}</p> -->
          <p><strong>Application Deadline: </strong>{{ new Date(selectedPd.application_deadline).toLocaleDateString() }}</p>
          <p><strong>Pd Status: </strong>{{ selectedPd.pd_status }}</p>
          <button @click="cancel" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div> 
<!-- applications -->
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