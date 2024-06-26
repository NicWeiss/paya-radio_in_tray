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
    },

    async like(track_id){
      try {
        await Api.post(`/like?track_id=${track_id}`);
      } catch (error) {
        console.log(error);
        return;
      }

      this.$emit('onAction', true)
    },

    async dislike(track_id){
      try {
        await Api.post(`/dislike?track_id=${track_id}`);
      } catch (error) {
        console.log(error);
        return;
      }

      this.$emit('onAction', true)
    }
  },

  created() {
  },
};
