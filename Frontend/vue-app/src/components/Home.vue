<template>
  <div id="home">
    <b-card title="Home" sub-title="About This Project">
      <b-card-text>
        Some quick example text to build on the
        <em>card title</em> and make up the bulk of the card's
        content.
      </b-card-text>

      <b-card-text>A second paragraph of text in the card.</b-card-text>
      <font-awesome-icon :icon="['fab', 'github']" />
      <a href="#" class="card-link">Project Github</a>
    </b-card>
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
</style>
