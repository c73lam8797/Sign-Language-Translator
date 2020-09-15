<template>
  <div id="home" class="page_section">
    <b-row class="justify-content-center" no-gutters>
      <b-card title="Home" sub-title="About This Project" id="home_card" title-tag="h2">
        <b-card-text>
          Sign language is a fundamental method of communication for many, such as those with impaired hearing. However, it may be difficult for those who do not know sign language to communicate or understand those who are limited only to sign language as a form of communication.
        </b-card-text>
        <b-card-text>
          This goal of this project is to prototype a solution to facilitate communication with those who are limited to using sign language. This web application applies machine learning with TensorFlow to take sign language inputted by users and predict the translation. Below is a summary of the different sections on the site:
        </b-card-text>
        <b-card-body sub-title="Picture Translation">
          <b-card-text>
            Users have the option of either capturing a picture using their device's webcam, or upload an image themselves. Upon sending, the image is sent to the model, in which it returns a prediction along with a 'confidence scoring' of its classification.
          </b-card-text>
        </b-card-body>
        <b-card-body sub-title="Video Translation">
          <b-card-text>
            This section is under development.
          </b-card-text>
        </b-card-body>
        <b-card-text>
          <em>Please note this project is still a work in progress and is subject to future updates.</em>
        </b-card-text>
        <font-awesome-icon :icon="['fab', 'github']" />
        <a href="https://github.com/c73lam8797/Sign-Language-Translator" class="card-link">Project Github</a>
      </b-card>
    </b-row>
  </div>
</template>

<script>

export default {
  name: "Home"
  // props: {
  //   msg: String
  // }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card-link {
  margin: 5px;
}

#home_card {
  max-width: 60%;
  margin: 30px;
  padding: 30px;
}

@media only screen and (max-width: 1024px) {
  #home_card {
    max-width: 95%;
    margin: 30px 0px;
    padding: 10px;
  }
}
</style>
