<script>
import api from '@/utils/api';
import Chart from 'chart.js/auto'
export default {
  name: "AdminSummary",

  async mounted() {
    try{ 
      const app = await api.get("/admin_api/app_list");

      let total_app = app.length
      let selected = 0 

      app.forEach(a => {if(a.app_status === "selected"){
        selected++
      }})
      this.renderChart(selected, total_app)

      let applied = 0
      let shortlisted = 0
      let interview_scheduled = 0
      let app_selected = 0
      let app_rejected= 0

      app.forEach(a => {
        if(a.app_status === "applied") applied++
        if(a.app_status === "shortlisted") shortlisted++
        if(a.app_status === "interview scheduled") interview_scheduled++
        if(a.app_status === "selected") app_selected++
        if(a.app_status === "rejected") app_rejected++
      })
      this.renderAppStatusChart(applied, shortlisted, interview_scheduled, app_selected, app_rejected)


      const pd = await api.get("/admin_api/pd_list")
      let pending = 0
      let approved = 0
      let rejected = 0
      pd.forEach(p => {
        if(p.pd_status === "pending") pending++
        if(p.pd_status === "approved") approved++
        if(p.pd_status === "rejected") rejected++
      })
      this.renderPdChart(pending, approved, rejected)
    }
    catch (error) {
      console.error("Failed to load the chart ", error);
    }
  },
  methods: {
    renderChart(selected, total){
      new Chart(this.$refs.app_chart,{
        type: "pie",
        data:{
          labels:["Selected Applications", "Total Applications"],
          datasets:[{
            data:[selected, total]
          }]
        },
      options:{
        responsive:false
      }
      })
    },
    renderAppStatusChart(applied, shortlisted, interview_scheduled, app_selected, app_rejected){
      new Chart(this.$refs.appstatus_chart,{
        type: "bar",
        data:{
          labels:["Applied","Shortlisted", "Interview Scheduled", "Selected", "Rejected"],
          datasets:[{
            label:"Applications",
            data:[applied, shortlisted, interview_scheduled, app_selected, app_rejected]
          }]
        },
      options:{
        responsive:false
      }
      })
    },
    renderPdChart(pending, approved, rejected){
      new Chart(this.$refs.pd_chart,{
        type: "pie",
        data:{
          labels:["Pending", "Approved", "Rejected"],
          datasets:[{
            data:[pending, approved, rejected]
          }]
        },
      options:{
        responsive:false
      }
      })
    },
  }
}
  
</script>

<template>
  <div class="flex-container">
    <div class="row">
      <div class="col-md-4 text center">
        <h6>Selected Applications vs Total Applied Applications</h6>
        <canvas ref="app_chart" width="400" height="400"></canvas>
      </div>
      <div class="col-md-4 text center">
        <h6>Placement Drive Status</h6>
        <canvas ref="pd_chart" width="400" height="400"></canvas>
      </div>
      <div class="col-md-4 text center">
        <h6>Application Status Distribution</h6>
        <canvas ref="appstatus_chart" width="400" height="400"></canvas>
      </div>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: antiquewhite;
}
</style>