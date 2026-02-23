<script>
import api from '@/utils/api';
export default {
  name: "ScheduleInterview",
  data () {
    return {
      scheduled : "",
      remarks : "",
      errorMsg : "", 
    }
  },

  methods: {
    async scheduleIntw() {
      this.errorMsg = ""
      if (!this.scheduled){
        this.errorMsg = "Please enter the date and time of the interview...";
        return;
      }
      if (!this.remarks){
        this.errorMsg = "Please enter remarks...";
        return;
      }
      try {
        const payload = {
          scheduled : this.scheduled.replace("T", " ")+ ":00",
          remarks : this.remarks
        };
        const app_id = localStorage.getItem("selected_app_id");
        if (!app_id){
          this.errorMsg = "No Application is selected...";
          return;
        }
        const response = await api.post(`/comp_api/intw_schedule/${app_id}`, payload);
        alert("Interview Scheduled...");
        this.$router.push("/short_app_list");
      }
      catch (error) {
        this.errorMsg = error.message ;
      }
    },
    cancel () {
      this.$router.push("/short_app_list");
      this.scheduled = "";
      this.remarks = "";
      this.errorMsg = "";
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card-header bg-light text-black">
        <h4 class="mb-0"> Schedule Interview...</h4>
        <div class="card-body">
          <form @submit.prevent="scheduleIntw">
            <div class="mb-3">
              <label for="scheduled" class="form-label">Interview Date & Time: </label>
              <input type="datetime-local" class="form-control"  placeholder="Interview Date & Time" v-model="scheduled">
            </div>
            <div class="mb-3">
              <label for="remarks" class="form-label">Remarks: </label>
              <input type="text" class="form-control"  placeholder="remarks" v-model="remarks">
            </div>
            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-primary">Save</button>
              <button type="button" @click="cancel" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>