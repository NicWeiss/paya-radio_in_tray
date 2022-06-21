import Api from '@/components/service/api'
import Auth from '@/components/service/auth'


export default {
  name: 'Login',

  data() {
    return {
      login: '',
      password: ''
    }
  },

  methods: {
    async check() {
      let response = null

      try {
        response = await Api.get('/client');
        Auth.setSession(response.token);
      } catch (error) {
        console.log('error: ', error);
        Auth.invalidateSession()
        return
      }

      console.log(response);
      this.$router.push('/');
    },

    async logIn() {
      let response = null

      try {
        response = await Api.post(`/auth?user=${this.login}&password=${this.password}`);
        Auth.setSession(response.token);
      } catch (error) {
        console.log('error: ', error);
        Auth.invalidateSession()
        return;
      }

      console.log(response);
      this.$router.push('/');
    }
  },

  created() {
    this.check()
  },
};
