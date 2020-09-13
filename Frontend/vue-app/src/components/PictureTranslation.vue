<template>
  <div id="picture">
    <b-card>
      <div id="camera">
        <div>
          <b-button class="buttons" v-if="!webCamOn" @click="showCamera" variant="outline-primary">Turn On WebCam</b-button>
          <b-button class="buttons" v-else @click="hideCamera" variant="outline-primary">Turn Off WebCam</b-button>
          <b-button class="buttons" v-if="webCamOn" id="takephoto" @click="capture" variant="success">Capture</b-button>
        </div>
        <div>
          <div class="loading_container"><b-spinner v-if="loading" label="Spinning"></b-spinner></div>
          <video autoplay id="video"></video>
        </div>
        <div>
          <canvas id="canvas"></canvas>
          <div><b-button class="buttons" v-if="image" @click="translate" variant="outline-info">Translate Image</b-button></div>
        </div>
      </div>
    </b-card>
    <b-jumbotron v-if="translatedImages.length > 0" header="Translated Letters">
      {{ translatedImages.map(x => x.translation) }}
    </b-jumbotron>
    <b-card-group deck >
        <b-card v-bind:img-src="im.img" img-top class="predictions" v-for="im in translatedImages" :key="im.img">
          <b-card-text>
            {{ im.translation }}
          </b-card-text>
        </b-card>
    </b-card-group>

  </div>
</template>
<!-- ---------------------------------------------------------- -->
<!-- ---------------------------------------------------------- -->
<!-- ---------------------------------------------------------- -->
<script>
  const environment = process.env.NODE_ENV;
  const url = (environment === "development") ? "http://localhost:5000" : "";
  const constraints = {
    video: true,
    audio: false
  };

  let s = null;
  export default {
    data() {
      return {
        webCamOn: false,
        loading: false,
        image: "",
        predicting: false,
        translatedImages: [],
      }
    },
    methods: {
      showCamera: function() {
        this.webCamOn = true;
        this.loading = true;

        const video = document.getElementById("video");
        navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
          video.srcObject = stream;
          s = stream;
        })
        .finally(() => this.loading = false);
      },
      hideCamera: function() {
        this.webCamOn = false;
        //stop stream
        const video = document.getElementById("video");
        video.srcObject = null;
        if (s !== null) {
          const tracks = s.getTracks();
          tracks.forEach(x => x.stop());
        }

        //clear canvas and current img
        this.image = "";
        const canvas = document.getElementById("canvas");
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
      },
      capture: function () {
        const canvas = document.getElementById("canvas");
        const context = canvas.getContext('2d');
        const video = document.getElementById("video");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        this.image = canvas.toDataURL("image/png");
      },
      translate: function() {
        this.predicting = true;
        const params = { 
          method: "POST",
          body: JSON.stringify({ img: this.image }),
          headers: {
            'Content-Type': 'application/json',
          },
        }
        
        fetch(url + "/api/predict", params)
        .then(res => res.json())
        .then(r => {
          this.translatedImages.push({img: this.image, translation: r.classification, confidence: r.confidence});
        })
        .finally(() => this.predicting = false)
        .catch(() => { });

      }
    },
    components: {

    },
    beforeDestroy: function() {
      this.hideCamera();
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<!-- ---------------------------------------------------------- -->
<!-- ---------------------------------------------------------- -->
<!-- ---------------------------------------------------------- -->
<style scoped>
.loading_container {
  padding: 15px;
}

#video {
  transform: rotateY(180deg);
  -webkit-transform:rotateY(180deg); /* Safari and Chrome */
  -moz-transform:rotateY(180deg); /* Firefox */

  max-width: 100%;
  height: auto;
}

.buttons {
  margin: 3px;
}

.card-deck {
  margin: 0px;
}

</style>
