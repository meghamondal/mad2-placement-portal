const BASE_URL = "http://127.0.0.1:5000";
function getToken() {
  return localStorage.getItem("token");
}
async function httpRequest(endpoint, method ="GET", data=null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };
  const token = getToken();
  if (token) {
    options.headers["Authentication-Token"] = token;
  }
  if (data) {
    options.body = JSON.stringify(data);
  }
  const response = await fetch(`${BASE_URL}${endpoint}`, options);

  if (!response.ok){
    console.error("Status code: ", response.status);
    if (response.status === 401) {
      throw new Error("Invalid credentials...");
    }
    if (response.status === 500) {
      throw new Error("Internal server error...");
    }
    throw new Error("Not able to complete the request");
  }
  return response.status === 204 ? null : response.json();
}

export default {
  get(endpoint) {
    return httpRequest(endpoint);
  },
  post(endpoint, data){
    return httpRequest(endpoint, "POST", data);
  },
  patch(endpoint, data) {
    return httpRequest(endpoint, "PATCH", data);
  },
  delete(endpoint) {
    return httpRequest(endpoint, "DELETE");
  }
};