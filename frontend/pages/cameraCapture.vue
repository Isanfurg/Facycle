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
          <v-subheader min-widht="100%" class="textWhite"> <h1>Registrar Rostro</h1> </v-subheader>
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
          <v-list-item class="my-2 hidden-md-and-up">
            <canvas ref="canvas" id="canvas" width="440" height="300"></canvas>
          </v-list-item>
          <v-list-item>
            
              <v-list-item-avatar v-for="c in captures" :key="c" class="ma-1"> 
                <img v-bind:src="c" height="50" />
            </v-list-item-avatar>
          </v-list-item>
          
          <v-list-item>
            <h4 class="mt-3 ml-3 mb-2">CORREO ELECTRONICO</h4>
          </v-list-item>
          <v-list-item>
            <v-text-field
              v-model="user.email"
              class="ml-2"
              style="max-height: 50px"
              placeholder="juan123@hotmail.com"
              filled
            ></v-text-field>
          </v-list-item>
           <v-list-item>
            <h4 class="mt-3 ml-3 mb-2">Nombre</h4>
          </v-list-item>
          <v-list-item>
            <v-text-field
              v-model="user.name"
              class="ml-2"
              style="max-height: 50px"
              placeholder="Pepito los palotes"
              filled
            ></v-text-field>
          </v-list-item>
          <v-list-item>
            <h4 class="mt-3 ml-3 mb-2">CONTRASEÑA</h4>
          </v-list-item>
          <v-list-item>
            <v-text-field
              v-model="user.password"
              class="ml-2"
              type="password"
              style="max-height: 50px"
              placeholder="********"
              filled
            ></v-text-field>
          </v-list-item>
          
          <v-list-item class="mt-10">
            <v-btn
              elevation="4"
              style="width: 100%; background-color: #EC994B"
              class="textWhite"
              @click="upload()"
              >Registrar</v-btn
            >
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
			captures: []
     
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
      if(this.photos==15){
        return 0;
      }
			this.canvas = this.$refs.canvas;
			var context = this.canvas
				.getContext("2d")
				.drawImage(this.video, 0, 0, 400, 300)
			this.captures.push(canvas.toDataURL("image/png"));
      this.photos = this.photos+1
      console.log(this.photos)
		},
		upload(){
      if(this.photos>5){
        axios.get('http://127.0.0.1:5000/api/addUser/'+this.user.email+'/'+this.user.name+'/'+this.user.password)
    .     then(response => {
      // JSON responses are automatically parsed.
      this.users = response.data
      console.log(this.users)
      })
    .catch(e => {
      this.errors.push(e)
      })
      for (let i = 0; i < this.photos; i++) {
        console.log(this.captures[i])
        let formData = new FormData();
        formData.append('image',this.captures[i])
        //I am posting the data converted to FormData using Axios to Flask.
        axios.post('http://127.0.0.1:5000/api/upload/'+this.user.email+'/'+i, formData).then(function (response) {
        console.log(response)
         })
         .catch(e => {
           this.errors.push(e)
      })
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
