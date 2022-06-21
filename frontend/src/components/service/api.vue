<script>
import Auth from "@/components/service/auth";

const API = `http://${window.location.hostname}:7778/api`;

export default {
  get(...params) {
    return this.doRequest("get", ...params);
  },

  put(...params) {
    return this.doRequest("put", ...params);
  },

  post(...params) {
    return this.doRequest("post", ...params);
  },

  delete(...params) {
    return this.doRequest("delete", ...params);
  },

  doRequest(method, url, data = null) {
    let config = {
      method: method,
      url: API + url,
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
      data: data,
      json: true,
    };

    if (Auth.isAuthenticated()) {
      config.headers.session = Auth.getSession();
    }

    axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
    axios.defaults.headers.post["Access-Control-Allow-Headers"] = "*";

    return new Promise(
      function (resolve, reject) {
        axios(config)
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            if (error.data === "TOKEN EXPIRED") {
              console.log("asdas");
              Auth.invalidateSession();
              window.location.replace("/");
            }
            reject(error);
          });
      }.bind(this)
    );
  },
};
</script>
