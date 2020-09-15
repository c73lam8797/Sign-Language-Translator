<template>
  <div id="picture">
    <b-card title="Picture Translation" title-tag="h2" sub-title="Upload a file or take a picture with your webcam!">
      <div id="media_wrapper">
        <!-- Upload file -->
        <b-card class="file_cards">
          <b-form-file accept="image/jpeg, image/png" v-model="uploadedFile" :state="Boolean(uploadedFile)"></b-form-file>
          <b-button class="buttons" v-if="Boolean(uploadedFile)" @click="translateUploadedFile" variant="outline-info" style="margin-top: 15px">Translate Uploaded Image</b-button>
          <b-button class="buttons" v-if="Boolean(uploadedFile)" @click="uploadedFile = null" variant="outline-danger" style="margin-top: 15px">Clear Uploaded Image</b-button>
        </b-card>

        <!-- Webcam button group -->
        <b-card class="file_cards">
          <b-button class="buttons" v-if="!webCamOn" @click="showCamera" variant="outline-primary"><font-awesome-icon v-if="!loading" :icon="['fas', 'video']" />
            <b-spinner v-if="loading" small label="Spinning"></b-spinner>  
            <span v-else> Turn On WebCam</span>
          </b-button>
          <b-button class="buttons" v-else @click="hideCamera" variant="outline-primary"><font-awesome-icon v-if="!loading" :icon="['fas', 'video-slash']" />
            <b-spinner v-if="loading" small label="Spinning"></b-spinner>
            <span v-else> Turn Off WebCam</span>
          </b-button>
         <!-- Webcam video stream -->
          <b-card-body class="capture">
            <b-card class="text-center video_cards" title="Video">
              <b-card-text v-if="!webCamOn">
                There is currently no video feed.
              </b-card-text>
              <div v-if="loading" class="loading_container"><b-spinner label="Spinning"></b-spinner></div>
              <video autoplay id="video"></video>
              <b-button class="buttons" v-if="webCamOn" id="takephoto" @click="capture" variant="success"><font-awesome-icon :icon="['fas', 'camera']" />  Capture</b-button>
            </b-card>
            <b-card class="text-center video_cards" title="Capture">
              <b-card-text v-if="!image">
                There is currently no image captured.
              </b-card-text>
              <canvas id="canvas"></canvas>
              <b-button class="buttons" v-if="image" @click="translate" variant="outline-info">Translate Capture</b-button>
              <b-button class="buttons" v-if="image" @click="clearCanvas" variant="outline-danger">Clear Capture</b-button>
            </b-card>
          </b-card-body>
        </b-card>
      </div>
      
      <!-- Predictions and translations -->
      <b-jumbotron>
        <h4>Translated Letters</h4>
        {{ translatedImages.map(x => x.translation).join(", ") }}
        <b-card-text v-if="translatedImages.length === 0">
          There are currently no translated letters.
        </b-card-text>
        <b-row class="justify-content-center" style="marginTop: 20px"> 
          <b-button variant="danger" @click="clear" v-if="translatedImages.length > 0">Clear All Predictions</b-button>
        </b-row>
      </b-jumbotron>
      <b-jumbotron>
        <h4>Predictions</h4>
        <b-card-text v-if="translatedImages.length === 0">
          There are currently no predictions.
        </b-card-text>
        <div id="predictions">
          <b-card v-bind:img-src="im.img" img-top class="predictions" v-for="im in translatedImages" :key="im.img">
            <b-card-text>Translation: {{ im.translation }}</b-card-text>
            <b-card-text>Confidence: {{ im.confidence.toFixed(2) }}%</b-card-text>
          </b-card>
        </div>
      </b-jumbotron>
    </b-card>
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
        uploadedFile: null,
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

        this.clearCanvas();
      },
      clearCanvas: function () {
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
        canvas.height = video.offsetHeight;
        canvas.width = video.offsetWidth;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        this.image = canvas.toDataURL("image/png");
      },
      translate: function() {
        this.predicting = true;
        const formData = new FormData();
        formData.append('b64', this.image);
        const params = { 
          method: "POST",
          body: formData,
          headers: {
            'Access-Control-Allow-Origin': 'http://localhost:5000/api/predict'
          },
        }

        fetch(url + "/api/predict", params)
        .then(res => res.json())
        .then(r => {
          this.translatedImages.push({img: this.image, translation: r.classification, confidence: r.confidence});
        })
        .finally(() => this.predicting = false)
        .catch(() => { });
      },
      clear: function() {
        this.translatedImages = [];
      },
      translateUploadedFile: function() {

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
  width: 100%;
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

.capture {
  display: flex;
  justify-content: space-around;
}

#canvas {
  width: 100%;
  max-width: 100%;
  height: auto;
}

.text-center {
  width: 50%;
  max-width: 50%;
}

.predictions {
  width: 19%;
  margin: 0.5%;
  padding: 0.5%;
  border: solid 1px black;
}

#predictions {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.video_cards {
  margin: 10px;
}

.file_cards {
  width: 100%;
  margin: 10px 0px;
}

#media_wrapper {
  margin: 10px 0px;
}
</style>
