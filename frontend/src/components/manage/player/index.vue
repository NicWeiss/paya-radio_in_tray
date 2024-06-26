<template>
  <div class="player">
    <History
      class="history-wrapper"
      v-if="is_show_history"
      :history="history"
      @onClose="is_show_history = !is_show_history"
      @onAction="onActionInHistory"
    />
    <div class="header">
      <div class="station">On your wave</div>
    </div>
    <div v-if="track">
      <div class="player-body">
        <div class="cover-section">
          <img :src="cover" class="background-cover" />
          <div class="cover-wrapper">
            <img :src="cover" class="cover" />
          </div>
        </div>

        <div class="control-section">
          <div class="track-info">
            <div class="title">{{ track.title }}</div>
            <div class="artists">{{ track.artists.join(", ") }}</div>
          </div>
          <div class="track-control">
            <progress
              id="file"
              max="100"
              :value="playPercent"
              class="progress"
            />
            <div class="controls">
              <button
                class="btn btn-secondary btn-circle"
                v-on:click="get_history"
              >
                <img src="~@/assets/img/history.svg" />
              </button>

              <div>
                <button
                  class="btn btn-circle"
                  :class="
                    track.is_disliked ? 'btn-primary-selected' : 'btn-primary'
                  "
                  v-on:click="dislike"
                >
                  <img
                    src="~@/assets/img/dislike.svg"
                    class="svg-from-yandex svg-big"
                  />
                </button>

                <button
                  v-if="state == 'Playing'"
                  class="btn btn-primary btn-circle-big"
                  v-on:click="pause"
                >
                  <img src="~@/assets/img/pause.svg" class="svg-big" />
                </button>

                <button
                  v-else
                  class="btn btn-primary btn-circle-big"
                  v-on:click="play"
                >
                  <img src="~@/assets/img/play.svg" class="svg-big" />
                </button>

                <button
                  class="btn btn-circle"
                  :class="
                    track.is_liked ? 'btn-primary-selected' : 'btn-primary'
                  "
                  v-on:click="like"
                >
                  <img
                    src="~@/assets/img/like.svg"
                    class="svg-from-yandex svg-big"
                  />
                </button>
              </div>

              <button class="btn btn-primary btn-circle" v-on:click="next">
                <img src="~@/assets/img/next.svg" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script src="./component.js"></script>

<style lang="scss">
body {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: center;
  background-color: black;
  color: white;
  width: 100%;

  #app {
    width: 100%;
  }
}
.svg-big {
  width: 50px;
  height: 50px;
}

.svg-from-yandex {
  position: relative;
  left: -5px;
  top: -5px;
}

.player {
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;

  .history-wrapper {
    position: absolute;
    width: 50%;
    left: 0;
    top: 0;
    backdrop-filter: blur(45px);
    height: 100%;
    z-index: 5;
    background: #00000094;
  }

  .header {
    .station {
      text-align: center;
      font-size: 18px;
    }
  }

  .player-body {
    display: flex;
    max-height: 86vh;
    height: 86vh;
    max-width: 1500px;
    width: 100%;

    .cover-section {
      width: 50%;
      padding: 70px 90px 70px 70px;
      display: flex;
      align-content: center;
      justify-content: center;
      align-items: center;

      .cover-wrapper {
        width: 100%;
        height: 100%;
        z-index: 2;
        display: flex;
        justify-content: center;
        align-items: center;

        .cover {
          max-width: 100%;
          max-height: 100%;
          object-fit: contain;
          box-shadow: 0 0 15px rgb(145, 145, 145);
          z-index: 2;
        }
      }

      .background-cover {
        position: absolute;
        filter: blur(100px);
        z-index: 0;
        height: 80%;
      }
    }

    .control-section {
      padding: 110px 110px 70px 110px;
      width: 50%;
      max-width: 700px;
      display: flex;
      flex-direction: column;
      flex-wrap: nowrap;
      align-content: center;
      justify-content: space-between;
      align-items: center;
      z-index: 2;

      .track-info {
        width: 50vw;
        min-height: 140px;
        max-width: 700px;

        .title {
          text-align: center;
          font-size: 40px;
          font-weight: 600;
          overflow-wrap: break-word;
        }

        .artists {
          text-align: center;
          font-size: 30px;
          font-weight: 200;
          color: #696969;
          overflow-wrap: break-word;
        }
      }

      .track-control {
        width: 100%;
        padding: 0 0 50px 0;
        min-width: 300px;

        .controls {
          display: flex;
          justify-content: space-around;
          align-items: center;
        }
      }
    }
  }

  .progress {
    background-color: #fff;
    border: 0;
    min-height: 18px;
    border-radius: 9px;
    width: 100%;
    animation: progres 4s linear;
    margin: 50px 0;
  }
}

@media (max-width: 760px) {
  .player {
    align-items: center;
    flex-direction: column;

    .history-wrapper {
      width: 100%;
    }

    .header {
      padding-bottom: 20px;
    }

    .player-body {
      align-items: center;
      flex-direction: column;
      height: unset;
      max-height: unset;

      .cover-section {
        width: 70%;
        padding: unset;

        .background-cover {
          height: 50%;
          max-width: 100%;
        }
      }

      .control-section {
        width: 95%;
        padding: 20px 0 10px 0;

        .track-info {
          width: unset;

          .title {
            font-size: 25px;
          }

          .artists {
            font-size: 20px;
          }
        }

        .progress {
          margin: 20px 0;
        }

        .track-control {
          min-width: unset;
          padding: 0px 0 26px 0;
        }
      }
    }
  }
}
</style>
