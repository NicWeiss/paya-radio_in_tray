<script>
export default {
  setSession(session) {
    localStorage.setItem("session", session);
  },

  getSession() {
    return localStorage.getItem("session");
  },

  isAuthenticated() {
    return !!localStorage.getItem("session");
  },

  invalidateSession() {
    localStorage.setItem("session", "");
  },
};
</script>
