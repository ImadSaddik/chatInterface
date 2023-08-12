<template>
  <p class="card-text typingEffect javascript">{{ typeLine1 }}</p>
</template>

<script>
export default {
  name: 'TypingEffect',
  props: ['text', 'speed'],
  data() {
    return {
      typeLine1: '',
      animationEnded: false
    }
  },
  mounted() {
    this.typeEffect1()
  },
  methods: {
    typeEffect1() {
      if (this.typeLine1.length < this.text.length && this.speed > 0) {
        this.typeLine1 += this.text.charAt(this.typeLine1.length);
        setTimeout(this.typeEffect1, this.speed)
      } else {
        this.typeLine1 = this.text
        this.animationEnded = true
        this.$emit('animationEnded', this.animationEnded)
      }
    }
  }
}
</script>

<style scoped>
  .typingEffect {
    animation: blink 1s 2;
  }

  @keyframes blink {
    0%, 45% {
      border-color: transparent;
    }
    50%, 100% {
      border-color: white;
    }
  }

  #app {
    color: #353C4E;
    background: #F0F2F4;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
    font-family: 'Roboto', Arial, sans-serif;
    font-size: 1.5rem;
  }

  html, body {
    height: 100%;
    margin: 0;
  }
</style>