<template>
  <div id="picture">
    <div id="camera">
      <div>
        <button v-if="!webCamOn" @click="showCamera">Turn On WebCam</button>
        <button v-else @click="hideCamera">Turn Off WebCam</button>
      </div>
      <div>
        <div class="loading_container"><b-spinner v-if="loading" label="Spinning"></b-spinner></div>
        <video autoplay id="video"></video>
      </div>
			
      <!-- <vue-web-cam v-bind:autoplay="false" /> -->
      <div>
        <button v-if="webCamOn" id="takephoto" @click="capture">Capture</button>
      </div>
		</div>
    
    <!-- <canvas id="canvas"></canvas>
    <div id="output">
      <img id="photo" alt="Screen Capture">
    </div>
     -->
  </div>
</template>

<script>
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
        const video = document.getElementById("video");
        video.srcObject = null;
        if (s !== null) {
          const tracks = s.getTracks();
          tracks.forEach(x => x.stop());
        }
      },
      capture: function () {

      }
    },
    components: {

    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.loading_container {
  padding: 15px;
}

#video {
  transform: rotateY(180deg);
  -webkit-transform:rotateY(180deg); /* Safari and Chrome */
  -moz-transform:rotateY(180deg); /* Firefox */
}
</style>
