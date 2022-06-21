import Api from '@/components/service/api';
import Auth from '@/components/service/auth';
import History from '@/components/manage/history/index'


export default {
  name: "Player",

  components: {
    History
  },

  methods: {
    async check() {
      let response = null;

      try {
        response = await Api.get('/client');
        Auth.setSession(response.token);
      } catch (error) {
        console.log('error: ', error);
        Auth.invalidateSession();
        this.$router.push('/login');
        return
      }
    },

    async dislike() {
      try {
        await Api.post('/dislike');
      } catch (error) {
        return;
      }

      this.get_track(true);
    },

    async pause() {
      try {
        await Api.post('/pause');
      } catch (error) {
        return;
      }

      if (this.state == 'Paused') {
        this.state = 'Playing';
      } else {
        this.state = 'Paused';
      }
    },

    async play() {
      try {
        await Api.post('/play');
      } catch (error) {
        return;
      }

      this.state = 'Playing';
      this.get_track();
    },

    async like() {
      try {
        await Api.post('/like');
      } catch (error) {
        return;
      }

      this.get_track();
    },

    async next() {
      try {
        await Api.post('/next');
      } catch (error) {
        return;
      }

      this.get_track(true);
    },

    async get_track(isNext = false) {
      let response = null;

      try {
        response = await Api.get('/track');
      } catch (error) {
        return;
      }

      this.track = response.track;
      this.cover = `data:image/png;base64, ${this.track.cover}`;

      if (isNext) {
        this.playPercent = 0;
      }
    },

    async get_history() {
      let response = null;

      try {
        response = await Api.get('/history');
      } catch (error) {
        return;
      }

      console.log(response);

      this.history = response.history;
      this.is_show_history = true;
    },

    async get_player() {
      let response = null;

      try {
        response = await Api.get('/player_state');
      } catch (error) {
        return;
      }

      this.player = response.player_state;
      this.duration = this.player.track_duration;
      this.playInkrement = 0.5 / ((this.duration / 100) * 0.001);
      this.playPercent = Number((this.player.current_time * (100 / this.player.track_duration)).toFixed(2));
      this.state = this.player.state;

      if (!this.track || (this.track.id != this.player.playing_track_id)) {
        this.get_track();
      }
    },

    async inkrement_progressbar() {
      if (this.state != 'Playing') {
        return;
      }

      this.playPercent = Number((Number(this.playPercent) + Number(this.playInkrement)).toFixed(2));

      if (this.playPercent > 100.2) {
        let is_loaded = false;
        const old_track_id = this.track.id

        while (is_loaded == false) {
          await this.get_track();

          if (old_track_id != this.track.id) { is_loaded = true }
          setTimeout(() => { }, 500);
        }

        await this.get_player();
        this.playPercent = 0;
      }
    },
  },

  created() {
    this.playPercent = 0;
    this.state = '';
    this.cover = '';
    this.is_show_history = false;
    this.check();
    this.get_track();
    this.get_player();

    let timerId = setInterval(() => this.get_player(), 15000);
    let timerId2 = setInterval(() => this.inkrement_progressbar(), 500);
  },

  data() {
    return {
      track: this.track,
      state: this.state,
      cover: this.cover,
      playPercent: this.playPercent,
      is_show_history: this.is_show_history,
      history: this.history,
    };
  },
};
