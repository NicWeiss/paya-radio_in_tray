<template>
  <div>
    <div class="track-history">
      <div class="track-wrapper" v-for="track in history" :key="track.id">
        <div class="track">
          <div class="cover-section">
            <img class="cover" :src="`data:image/png;base64, ${track.cover}`" />
          </div>

          <div class="control-section">
            <div class="title">{{ track.title }}</div>
            <div class="artists">{{ track.artists.join(", ") }}</div>

            <div class="track-control">
              <button
                class="btn btn-circle"
                :class="
                  track.is_disliked ? 'btn-primary-selected' : 'btn-primary'
                "
                v-on:click="dislike(track.id)"
              >
                <img
                  src="~@/assets/img/dislike.svg"
                  class="svg-from-yandex svg-big"
                />
              </button>

              <button
                class="btn btn-circle"
                :class="track.is_liked ? 'btn-primary-selected' : 'btn-primary'"
                  v-on:click="like(track.id)"
              >
                <img
                  src="~@/assets/img/like.svg"
                  class="svg-from-yandex svg-big"
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="close-wrapper">
      <button class="btn btn-circle close" v-on:click="close">
        <img src="~@/assets/img/close.svg" class="svg" />
      </button>
    </div>
  </div>
</template>

<style lang="scss">
.track-history {
  overflow: overlay;
  max-height: 100%;
  padding: 0 0 70px 0;
  display: flex;
  flex-direction: column;
  align-items: center;

  .track-wrapper {
    width: 100%;
    max-width: 800px;

    .track {
      display: flex;
      padding: 25px 40px;
      transition: 0.5s;

      .cover-section {
        .cover {
          max-width: 100px;
        }
      }

      .control-section {
        padding: 0 0 0 40px;

        .title {
          font-size: 20px;
          font-weight: 600;
        }

        .artists {
          font-size: 15px;
          font-weight: 200;
        }

        .track-control {
          padding: 10px 0 0 0;

          .btn {
            width: 32px;
            height: 32px;

            .svg-from-yandex {
              left: -9px;
              top: -8px;
            }
          }
        }
      }
    }
  }
}

.close-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  position: fixed;
  bottom: 20px;

  .close {
    background: #008000;
    width: 180px;
    height: 50px;
    .svg {
      width: 32px;
      height: 32px;
    }
  }
}

.track:hover {
  background: #0080001f;
  transition: 0.5s;
}
</style>

<script src="./component.js"></script>
