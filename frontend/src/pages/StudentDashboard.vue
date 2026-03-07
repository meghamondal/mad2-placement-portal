<script>
import api from '@/utils/api';
export default {
  name: "StudentDashboard",

  data () {
    return {
      student: null,
      studEdit: null,
      isEditing: false
    }
  },
  created() {
    this.loadStudent();
  },
  methods : {
    handleResume(event) {
      const file = event.target.files[0];
      if (!file){
        this.errorMsg = "File doesn't exit...";
        return;
      } 
      if (file.type !== "application/pdf") {
        alert("PDF files are only allowed");
        return;
        }
        this.studEdit.resume_file = file;
    },
    async loadStudent() {
      this.errorMsg = "";
      try {
        const data = await api.get("/api/stud_details");
        console.log("student data: ", data)
        this.student = data;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "Student Details Not Found...";
      }
    },
    editStud(student) {
      // this.selectedStud = null;
      this.studEdit = { ...student };
      if (this.studEdit.dob) {
        const n_date = new Date(this.studEdit.dob);
        this.studEdit.dob = n_date.toISOString().split("T")[0];
      }
      this.isEditing = true;
    },
    async saveEdit() {
      try {
        const formData = new FormData();
        if (this.studEdit.f_name)
        formData.append("f_name", this.studEdit.f_name);
        if (this.studEdit.l_name)
        formData.append("l_name", this.studEdit.l_name);
        if (this.studEdit.dob)
        formData.append("dob", this.studEdit.dob);
        if (this.studEdit.graduation_year)
        formData.append("graduation_year", this.studEdit.graduation_year);
        if (this.studEdit.cgpa)
        formData.append("cgpa", this.studEdit.cgpa);
        if (this.studEdit.resume_file instanceof File)
        formData.append("resume_file", this.studEdit.resume_file);
        const response = await fetch("http://127.0.0.1:5000/api/stud_details",{method: "PATCH",headers: {"Authentication-Token": localStorage.getItem("token")},body: formData});
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || "updation failed...");
        }
        this.student = data;
        this.isEditing = false;
        this.studEdit = null;
      }
      catch (error) {
        this.errorMsg = this.errorMsg = error.response?.data?.message || "updation failed...";
      }
    },
    async csvStud(){
      try {
        const response = await api.post(`/api/export_csv/${this.student.stud_id}`);
        window.location.href = `http://127.0.0.1:5000/api/export_status/${response.task_id}`;
      }
      catch (error) {
        alert("Export Failed!")
      }
    },
    cancel() {
      this.studEdit = null;
      this.isEditing = false;
      this.errorMsg = "";
      console.log("Details closed...")
    }
  }
};
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div v-if="student && !isEditing" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-light text-black d-flex justify-content-between align-items-center">
          <h4 class="mb-0"> Student Details...</h4>
          <button class="btn btn-warning" @click="editStud(student)">Edit</button>
        </div>
        <div class="card-body">
          <p><strong>ID: </strong>{{ student.stud_id }}</p>
          <p><strong>Name: </strong>{{ student.f_name }} {{ student.l_name }}</p>
          <p><strong>Date of Birth: </strong>{{ new Date(student.dob).toLocaleDateString() }}</p>
          <p><strong>Graduation Year: </strong>{{ student.graduation_year }}</p>
          <p><strong>CGPA: </strong>{{ student.cgpa }}</p>
          <a :href="`http://127.0.0.1:5000/${student.resume_file}`" target="_blank">View Resume</a>
          <div class="card mt-4 shadow-sm border-0">
            <button class="btn btn-secondary" @click="csvStud">Download CSV</button>
          </div>        
        </div>
      </div>
      <div v-if="isEditing" class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-light text-black d-flex justify-content-between align-items-center">Edit Company Details</div>
        <div class="card-body">
          <div class="mb-3">
            <label for="f_name" class="form-label">First Name: </label>
            <input type="text" class="form-control"  placeholder="first name" v-model="studEdit.f_name">
          </div>
          <div class="mb-3">
            <label for="f_name" class="form-label">Last Name: </label>
            <input type="text" class="form-control"  placeholder="first name" v-model="studEdit.l_name">
          </div>
          <div class="mb-3">
            <label for="dob" class="form-label">Date of Birth: </label>
            <input type="date" class="form-control"  placeholder="date of birth" v-model="studEdit.dob">
          </div>
          <div class="mb-3">
            <label for="graduation_year" class="form-label">Graduation Year: </label>
            <input type="number" class="form-control"  placeholder="graduation year" v-model="studEdit.graduation_year">
          </div>
          <div class="mb-3">
            <label for="cgpa" class="form-label">CGPA: </label>
            <input type="number" class="form-control"  placeholder="cgpa" v-model="studEdit.cgpa">
          </div>
          <div class="mb-3">
            <label for="doc" class="form-label">Resume File(PDF): </label>
            <input type="file" class="form-control"  placeholder="Your Resume" accept="application/pdf" @change="handleResume">
            <div v-if="studEdit.resume_file" class="mt-2">
              <a :href="studEdit.resume_file" target="_blank" class="text-primary"></a>
            </div>
          </div>
          <div class="mb-3 center">
            <button @click="saveEdit" type="submit" class="btn btn-primary">Save</button>
            <button @click="cancel" class="btn btn-secondary">Cancel</button>
          </div>
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
