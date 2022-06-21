import Api from '@/components/service/api'
import Auth from '@/components/service/auth'

export default {
  name: 'History',

  props: ['history'],

  data() {
    return {
    }
  },

  methods: {
    close() {
      this.$emit('onClose');
    }
  },

  created() {
  },
};
