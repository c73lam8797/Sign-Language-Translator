<template>
  <div id="picture">
    <b-card id="picture_card" class="page_section" title="Picture Translation" title-tag="h2" sub-title="Upload a file or take a picture with your webcam!">
      <a href="#translations_predictions" id="scrollToPredictionsWrapper"><b-button variant="dark" id="scrollToPredictions">↓</b-button></a>
      <div id="media_wrapper">
        <!-- Upload file -->
        <b-card class="file_cards" title="Upload Image">
          <b-form-file accept="image/jpeg, image/png" v-model="uploadedFile" :state="Boolean(uploadedFile)"></b-form-file>
          <b-button class="buttons" v-if="Boolean(uploadedFile)" @click="translateUploadedFile" variant="outline-info" style="margin-top: 15px">Translate Uploaded Image</b-button>
          <b-button class="buttons" v-if="Boolean(uploadedFile)" @click="uploadedFile = null" variant="outline-danger" style="margin-top: 15px">Clear Uploaded Image</b-button>
        </b-card>
        <!-- Webcam button group -->
        <b-card class="file_cards" title="Use WebCam">
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
      <b-card title="Translations + Predictions" id="translations_predictions">
        <b-card-body>
          <b-jumbotron>
            <!-- <h4>Translated Letters</h4> -->
            {{ translatedImages.map(x => x.translation).join(", ") }}
            <b-card-text v-if="translatedImages.length === 0">
              There are currently no translated letters.
            </b-card-text>
            <b-row class="justify-content-center" style="marginTop: 20px"> 
              <b-button variant="danger" @click="clear" v-if="translatedImages.length > 0">Clear All Predictions</b-button>
            </b-row>
          </b-jumbotron>
          <b-jumbotron>
            <!-- <h4>Predictions</h4> -->
            <b-card-text v-if="translatedImages.length === 0">
              There are currently no predictions.
            </b-card-text>
            <div id="predictions">
              <b-card v-bind:img-src="im.img" img-top class="prediction_cards" v-for="im in translatedImages" :key="im.img">
                <b-card-text>Translation: {{ im.translation }}</b-card-text>
                <b-card-text>Confidence: {{ im.confidence.toFixed(2) }}%</b-card-text>
              </b-card>
            </div>
          </b-jumbotron>
        </b-card-body>
      </b-card>
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

  const send_request = (b64_img) => {
    const formData = new FormData();
    formData.append('b64', b64_img);
    const params = { 
      method: "POST",
      body: formData,
      headers: {
        'Access-Control-Allow-Origin': 'http://localhost:5000/api/predict'
      },
    }

    return fetch(url + "/api/predict", params)
            .then(res => res.json());
  }

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
        send_request(this.image)
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
        const reader = new FileReader();
        //this even listener only gets called when you start reading the file
        reader.addEventListener('load', () => {
          const base64 = reader.result;
          if (base64) {
            send_request(base64)
            .then(r => {
              this.translatedImages.push({img: base64, translation: r.classification, confidence: r.confidence});
            })
            .finally(() => this.predicting = false)
            .catch(() => { });
          }
        }, false);
        reader.readAsDataURL(this.uploadedFile);
   
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

.prediction_cards {
  min-width: 19%;
  max-width: 19%;
  margin: 0.5%;
  padding: 0.5%;
  background-color: rgba(66,66,66,0.5);
  color: white;
}

#predictions {
  overflow-x: auto;
  display: flex;
}


.video_cards {
  margin: 10px;
  box-shadow: 3px 3px 2px 3px #888888;
}

.file_cards {
  width: 100%;
  margin: 30px 0px;
}

#media_wrapper {
  margin: 10px 0px;
}

#scrollToPredictionsWrapper {
  color: white;
}
#scrollToPredictions:hover {
  transform: translateY(-5px);
}

#picture_card {
  /* background-color: transparent; */
}

</style>
