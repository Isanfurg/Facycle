<template>
  <v-row class="custom-content ma-0 pa-0" align="top" justify="center">
    <v-col class="px-12" cols="12">
      <v-card
        class="mx-auto"
        color="#EC994B"
        style="padding: 5px"
        min-width="50%"
        width="300px"
      >
        <v-list color="#73777B">
          <v-subheader min-widht="100%" class="textWhite"> <h1>Abrir candado</h1> </v-subheader>
          <hr />
          <v-list-item>
            <h4 class="mt-3 ml-3 mb-2">CAPTURA TU ROSTRO</h4>
          </v-list-item>
           <v-list-item>
              <video ref="video" id="video" width="440" height="300" autoplay></video>
          </v-list-item>
          
          <v-list-item>
            <v-btn  color="#EC994B" width="100%" id="snap" v-on:click="capture()">Tomar Foto</v-btn>
          </v-list-item>
           <v-list-item v-show="this.disable">
            <v-btn  color="red" width="100%" id="snap" >Coincidencia no encontrada, intente denuevo</v-btn>
          </v-list-item>
          <v-list-item class="my-2 ">
            <canvas ref="canvas" id="canvas" width="440" height="300" class="hidden-sm-and-up"></canvas>
          </v-list-item>
         
         
        </v-list>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import axios from "axios";

export default {

  data () {
    return {
      user:{
        name: '',
        password : '',
        email: ''
      },
      photos: 0,
      el: "#el",
			video: {},
			canvas: {},
			captures: [],
      response: '',
      disable: false

    }
  },
  mounted(){
		this.video = this.$refs.video;
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(stream => {
				console.log(stream);
				video.srcObject = stream;
				this.video.play();
			});
		}
	},
	methods: {
		capture() {
      if(this.photos==1){
        return 0;
      }
			this.canvas = this.$refs.canvas;
			var context = this.canvas
				.getContext("2d")
				.drawImage(this.video, 0, 0, 400, 300)
			this.captures.push(canvas.toDataURL("image/png"));
      this.photos = this.photos+1
      console.log(this.photos)
      this.upload()
		},
		upload(){
      if(this.photos==1){
        
      for (let i = 0; i < this.photos; i++) {
        console.log(this.captures[i])
        let formData = new FormData();
        formData.append('image',this.captures[i])
        //I am posting the data converted to FormData using Axios to Flask.
        axios.post('http://127.0.0.1:5000/api/recognize', formData).then(response => {
      // JSON responses are automatically parsed.
          this.response = response.data
          if(this.response.response === 'ok'){
            this.$router.push('/open') 
           
          }
          })
         .catch(e => {
           this.disable=true
            this.captures=[]
            this.photos=0
              
           this.errors.push(e)
           
      })
         this.$router.push('/') 
      }
      

      }
      else{
        console.log("Fotos insuficientes")
      }

      
      this.$router.push('/') 
		}
    
		

	}
}
</script>
<style scoped>
.custom-content {
  background-color: #F1EEE9;
  margin: 0 0 0 0;
  height: 100%;
}
hr {
  font-size: 54px;
  width: 100%;
  border-color: #EC994B;
}
.textBlack{
  color: #000;
}
.textWhite{
  color: #fff;
}
.textPrimary{
  color: #EC994B;
}
</style>
