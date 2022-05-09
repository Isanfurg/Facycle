<template>
  <div>
        <PhotoCapture v-model="imageBase64" />
        <VideoCapture uploadUrl="localhost:3000" v-model="videoUrl" />
    </div>
  </v-card>
</template>

<script>
import {PhotoCapture, VideoCapture} from 'vue-media-recorder'

export default {
  name: 'IndexPage',
  components:{
       PhotoCapture,
        VideoCapture
    },
  data() {
    return {
       imageBase64: '',
            videoUrl: '',
    }
  },
}
</script>
