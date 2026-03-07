<script>
import api from '@/utils/api';
export default{
  name: "OfferLetter",

  data() {
    return {
      offer_letter: "",
      errorMsg: ""
    };
  },
  created() {
    this.loadOffer();
  },
  methods: {
    async loadOffer() {
      try{
        const app_id = localStorage.getItem("selected_app_id");
        const data = await api.get(`/api/stud_offer/${app_id}`);
        this.offer_letter = data.offer_letter;
      }
      catch (error) {
        this.errorMsg = error.response?.data?.message || "Error in loading the offer letter";
      }
    }
  }
}
</script>

<template>
  <div class="container mt-4">
     <div class="shadow-lg p-3 mb-5 bg-body-tertiary rounded">
      <div class="card mt-4 shadow-sm border-0">
        <div class="card-header bg-light text-black d-flex justify-content-between align-items-center">
          <h4 class="mb-0">OFFER LETTER</h4>
        </div>
        <div class="card-body">
          <div class="bg-grey" style="white-space: pre-line;">{{ offer_letter }}</div>
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