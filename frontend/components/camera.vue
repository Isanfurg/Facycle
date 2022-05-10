<template>
<div id="el" class="mt-0">
        <video ref="video" id="video" width="100%" height="100%" autoplay></video>
		
       <v-btn  color="#EC994B" width="100%" id="snap" v-on:click="capture()">Tomar Foto</v-btn>

</div>

</template>

<script>
export default {
	data() {
		return {
			el: "#el",
			video: {},
			canvas: {},
			captures: []
		};
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
			this.canvas = this.$refs.canvas;
			var context = this.canvas
				.getContext("2d")
				.drawImage(this.video, 0, 0, 640, 480);
			this.captures.push(canvas.toDataURL("image/png"));
		},
		upload(){

		}
		

	}
};

</script>
